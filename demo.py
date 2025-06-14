from pyasmgen import ASMCode, Block
from pyasmgen.blocks.useful import Main,Initial,Main,Int0,Int2,Ext0,Ext1

with ASMCode() as asm:
    asm.equ('T2CON','0C8H')
    asm.equ('RCAP2L','0CAH')
    asm.equ('RCAP2H','0CBH')
    asm.equ('TL2','0CCH')
    asm.equ('TH2','0CDH')
    asm.equ('T2MOD','0C9H')
    asm.bit('ET2','0ADH')
    asm.bit('TR2','0CAH')
    asm.bit('TF2','0CFH')

    with Initial() as init:
        init.setb('P2.1',comment='ADC0832 CS')
        init.clr('P2.0',comment='LED CONTROL')
        init.clr('F0',comment='MEASURED MARK')
        init.clr('P2.5',comment='MODE MARK')
        init.setb('P1.1',comment='HUMAN ON CONTROL')
        init.mov('R0','#00H',comment='MEASURE RESULT REGISTER')
        init.mov('R1','#00H',comment='USER CONTROL REGISTER')
        init.mov('R2','#00H',comment='SEG CHOOSE')
        init.mov('R3','#2FH',comment='DH CONVERT COUNTER REGISTER')
        init.mov('DPTR','#1000H',comment='DPTR PIN')
        init.mov('SP','#60H')

        init.mov('TMOD','#22H')
        init.mov('TCON','#05H')
        with Block() as tf0:
            tf0.mov('TH0','#00H')
            tf0.mov('TL0','#0FFH')
        with Block() as tf1:
            tf1.mov('TH1','#00H')
            tf1.mov('TL1','#00H')

        with Block() as tf2:
            tf2.mov('T2MOD','#00H')
            tf2.mov('T2CON','#02H')
            tf2.mov('RCAP2H','#0FFH')
            tf2.mov('RCAP2L','#0FFH')
            tf2.mov('TH2','#0FFH')
            tf2.mov('TL2','#0FFH')

        with Block() as ea:
            ea.setb('ET0')
            ea.setb('PT0')
            ea.setb('ET2')
            ea.setb('EX0')
            ea.setb('EX1')
            ea.setb('EA')

        init.setb('TR0')
        init.setb('TR2')

    with Main() as main:
        main.jnb('F0','$')
        main.clr('F0',comment='RESET MEASURED MARK')
        main.clr('TR0')
        main.push('P0')
        main.mov('P0','#0FFH')
        main.jnb('P1.1','$')
        main.pop('P0')
        main.jb('P2.5','USERP')
        with Block(label='AUTOP') as auto:
            auto.mov('TL1','R0',comment='SET OFF TIME')
            auto.mov('TH1','R0')
            auto.ljmp('LIGHTLED')
        with Block(label='USERP') as user:
            user.mov('TL1','R1')
            user.mov('TH1','R1')
        with Block(label='LIGHTLED') as off_led:
            off_led.setb('P2.0',comment='LIGHT LED')
            off_led.setb('TR1')
            off_led.jnb('TF1','$')
            off_led.clr('TF1')
            off_led.clr('TR1')
            off_led.clr('P2.0',comment='OFF LED')
        with Block(label='SEGP') as seg:
            seg.mov('A','TH1')
            seg.cpl('A')
            seg.clr('C')
            with Block(label='HUNDREDC') as hundred:
                hundred.mov('32H','#00H',comment='HUNDRED INDICATION')
                with Block(label='HUNDREDCS') as hundreds:
                    hundreds.clr('C')
                    hundreds.subb('A','#64H')
                    hundreds.jc('TENC')
                    hundreds.inc('32H')
                    hundreds.ljmp('HUNDREDCS')
            with Block(label='TENC') as ten:
                ten.mov('31H','#00H',comment='TEN INDICATION')
                ten.clr('C')
                ten.mov('A','32H')
                ten.jz('ETENLOOP')
                ten.mov('R3','32H')
                ten.mov('A','TH1')
                ten.cpl('A')
                with Block(label='TENLOOP') as tenloop:
                    tenloop.subb('A','#64H')
                    tenloop.djnz('R3','TENLOOP')
                    tenloop.push('Acc')
                    tenloop.ljmp('TENCS')
                with Block(label='ETENLOOP') as etenloop:
                    etenloop.mov('A','TH1')
                    etenloop.cpl('A')
                    etenloop.push('Acc')
                with Block(label='TENCS') as tens:
                    tens.clr('C')
                    tens.subb('A','#0AH')
                    tens.jc('ONEC')
                    tens.inc('31H')
                    tens.ljmp('TENCS')
            with Block(label='ONEC') as one:
                one.mov('30H','#00H',comment='ONE INDICATION')
                one.clr('C')
                one.mov('A','31H')
                one.jz('EONELOOP')
                one.mov('R3','31H')
                one.pop('Acc')
                with Block(label='ONELOOP') as oneloop:
                    oneloop.subb('A','#0AH')
                    oneloop.djnz('R3','ONELOOP')
                    oneloop.ljmp('ONECS')
                with Block(label='EONELOOP') as eoneloop:
                    eoneloop.pop('Acc')
                with Block(label='ONECS') as ones:
                    one.clr('C')
                    ones.subb('A','#01H')
                    ones.jc('CHOOSEP')
                    ones.inc('30H')
                    ones.ljmp('ONECS')
            with Block(label='CHOOSEP') as choose:
                choose.cjne('R2','#00H','SSEGP')
                with Block(label='FSEGP') as fseg:
                    fseg.inc('R2')
                    fseg.mov('A','30H')
                    fseg.setb('P2.2',comment='CHOOSE FIRST SEG')
                    fseg.clr('P2.3')
                    fseg.clr('P2.4')
                    fseg.ljmp('DISPLAYP')
                with Block(label='SSEGP') as sseg:
                    sseg.cjne('R2','#01H','TSEGP')
                    sseg.inc('R2')
                    sseg.mov('A','31H')
                    sseg.clr('P2.2',comment='CHOOSE SECOND SEG')
                    sseg.setb('P2.3')
                    sseg.clr('P2.4')
                    sseg.ljmp('DISPLAYP')
                with Block(label='TSEGP') as tseg:
                    tseg.mov('R2','#00H')
                    tseg.mov('A','32H')
                    tseg.clr('P2.2',comment='CHOOSE THIRD SEG')
                    tseg.clr('P2.3')
                    tseg.setb('P2.4')
            with Block(label='DISPLAYP') as display:
                display.movc('A','@A+DPTR')
                display.mov('P0','A')
        main.setb('TR0')
        main.ljmp('MAIN')

    with Ext0(ret_label='EXT0PR') as ext0:
        ext0.dec('R1',comment='DEC USER CONTROL REGISTER')
    
    with Ext1(ret_label='EXT1PR') as ext1:
        ext1.inc('R1',comment='INC USER CONTROL REGISTER')

    with Int0() as int0:
        int0.clr('P2.1',comment='ENABLE ADC0832')
        int0.mov('SCON','#00H')
        int0.mov('SBUF','#07H',comment='SET ADC0832')
        with Block(label='TIP') as tip:
            tip.jnb('TI','$')
            tip.clr('TI')
        int0.setb('REN')
        with Block(label='RIFP') as rifp:
            rifp.jnb('RI','$')
            rifp.mov('A','SBUF')
            rifp.rr('A')
            rifp.rr('A')
            rifp.rr('A')
            rifp.anl('A','#1FH')
            rifp.mov('B','A')
            rifp.clr('RI')
        with Block(label='RISP') as risp:
            risp.jnb('RI','$')
            risp.mov('A','SBUF')
            risp.rl('A')
            risp.swap('A')
            risp.anl('A','#0E0H')
            risp.add('A','B')
            risp.clr('RI')
        int0.clr('REN')
        int0.mov('R0','A')
        int0.setb('P2.1',comment='DISABLE ADC0832')
        int0.setb('F0',comment='MEASURED INDICATION')

    with Int2('TF2',ret_label='TF2PR') as int2:
        int2.cpl('P2.5',comment='MODE CHANGE')

    asm.org('1000H')
    asm.db('03H','9FH','25H','0DH','99H','49H','41H','1FH','01H','09H')

print(asm.encode())