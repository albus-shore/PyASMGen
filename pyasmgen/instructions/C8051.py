from ..instructions import Instruction, SourceOperandError, DestinationOperandError, OperandError
from typing import Literal, get_args

### ============================= Operand Type Defination ============================= ###
Register = Literal['R0','R1','R2','R3','R4','R5','R6','R7']

RegisterIndirect = Literal['@R0','@R1']

SFR = Literal[
    'P0','SP','DPL','DPH','PCON','TCON','TMOD',
    'TL0','TL1','TH0','TH1','AUXR','P1','SCON','SBUF','P2',
    'AUXR1','WDTRST','IE','P3','IP','PSW','Acc','B',
    'T2CON','T2MOD','RCAP2L','RCAP2H','TL2','TH2']

A = Literal['A']

C = Literal['C']

SFRBit = Literal[
    'P0.0','P0.1','P0.2','P0.3','P0.4','P0.5','P0.6','P0.7',
    'TF1','TF0','IE1','IT1','IE0','IT0',
    'P1.0','P1.1','P1.2','P1.3','P1.4','P1.5','P1.6','P1.7',
    'TI','RI',
    'P2.0','P2.1','P2.2','P2.3','P2.4','P2.5','P2.6','P2.7',
    'EA','ET2','ES','ET1','EX1','ET0','EX0',
    'P3.0','P3.1','P3.2','P3.3','P3.4','P3.5','P3.6','P3.7',
    'PT2','PS','PT1','PX1','PT0','PX0',
    'C','Ac','F0','RS1','RS0','OV','P',
    'Acc.0','Acc.1','Acc.2','Acc.3','Acc.4','Acc.5','Acc.6','Acc.7',
    'B.1','B.2','B.3','B.4','B.5','B.6','B.7',
    'TF2','EXF2','RCLK','TCLK','EXEN2','TR2'
    ]

ReverseSFRBit = Literal[
    '/P0.0','/P0.1','/P0.2','/P0.3','/P0.4','/P0.5','/P0.6','/P0.7',
    '/TF1','/TF0','/IE1','/IT1','/IE0','/IT0',
    '/P1.0','/P1.1','/P1.2','/P1.3','/P1.4','/P1.5','/P1.6','/P1.7',
    '/TI','/RI',
    '/P2.0','/P2.1','/P2.2','/P2.3','/P2.4','/P2.5','/P2.6','/P2.7',
    '/EA','/ET2','/ES','/ET1','/EX1','/ET0','/EX0',
    '/P3.0','/P3.1','/P3.2','/P3.3','/P3.4','/P3.5','/P3.6','/P3.7',
    '/PT2','/PS','/PT1','/PX1','/PT0','/PX0',
    '/C','/Ac','/F0','/RS1','/RS0','/OV','/P',
    '/Acc.0','/Acc.1','/Acc.2','/Acc.3','/Acc.4','/Acc.5','/Acc.6','/Acc.7',
    '/B.1','/B.2','/B.3','/B.4','/B.5','/B.6','/B.7',
    '/TF2','/EXF2','/RCLK','/TCLK','/EXEN2','/TR2'
    ]

### ============================= Operand Check Functions ============================= ###
def _register_check(operand:str) -> bool:
    '''The function is defined for check whether register address is valid.
    Args:
        operand: A string indicates the operand to check.
    Returns:
        A boolean indicates whether the operand is vaild register address.
    '''
    if operand in get_args(Register):
        return True
    else:
        return False
    
def _register_indirect_check(operand:str) -> bool:
    '''The function is defined for check whether register indirect address is valid.
    Args:
        operand: A string indicates the operand to check.
    Returns:
        A boolean indicates whether the operand is vaild register indirect address.
    '''
    if operand in get_args(RegisterIndirect):
        return True
    else:
        return False
    
def _direct_address_check(operand:str) -> bool:
    '''The function is defined for check whether direct address is valid.
    Args:
        operand: A string indicates the operand to check.
    Returns:
        A boolean indicates whether the operand is vaild direct address.
    '''
    if (operand[0].isnumeric()
        and operand.endswith('H')
        and len(operand) in (3,4)
        ):
        return True
    else:
        return False
    
def _immediate_check(operand:str) -> bool:
    '''The function is defined for check whether immediate is valid.
    Args:
        operand: A string indicates the operand to check.
    Returns:
        A boolean indicates whether the operand is vaild immediate.    
    '''
    if(operand.startswith('#') 
       and operand[1].isnumeric()
       and operand.endswith('H') 
       and len(operand) in (4,5)
       ):
        return True
    else:
        return False

def _SFR_check(operand:str) -> bool:
    '''The function is defined for check whether SFR is valid.\n
        'A' not included.
    Args:
        operand: A string indicates the operand to check.
    Returns:
        A boolean indicates whether the operand is vaild SFR.
    '''
    SFRs = get_args(SFR)
    if operand in SFRs:
        return True
    else:
        return False    

def _bit_check(operand:str) -> bool:
    '''The function is defined for check whether bit address is valid.
    Args:
        operand: A string indicates the operand to check.
    Returns:
        A boolean indicates whether the operand is vaild SFR.
    '''
    bitable_SFR = ('P0','TCON','P1','SCON','P2','IE','P3',
                   'IP','PSW','Acc','B','T2CON')
    bitable_address = ('20H','21H','22H','23H','24H','25H','26H','27H',
                       '28H','29H','2AH','2BH','2CH','2DH','2EH','2FH',
                       '80H','88H','90H','98H','0A0H','0A8H','0B0H','0B8H',
                       '0D0H','0E0H','0F0H','0C8H')
    valid_number = ('0','1','2','3','4','5','6','7',
                    '8','9','A','B','C','D','E','F')
    if operand in get_args(SFRBit):
        return True
    elif '.' in operand:
        dot_index = operand.index('.')
        byte_address = operand[:dot_index-1]
        bit_address = operand[dot_index+1:]
        if ((byte_address in bitable_SFR 
            or byte_address in bitable_address) 
            and bit_address in range(8)):
            return True
        else:
            return False
    elif (
        (operand.endswith('H') 
          and operand[-2] in valid_number)
          and ((len(operand) == 3
                and operand[0] in valid_number[:9])
               or (len(operand) == 4 
                and operand.startswith('0') 
                and operand[1] in valid_number[10:]))
                ):
        return True
    else:
        return False

### ============================ Expose Instruction Class ============================ ###
class C8051:
    '''The class id defind work with 8051 ASM instructions.'''
    ## ========================== Data Transport Instruction ========================== ##
    @staticmethod
    def mov(dest:A|Register|str|SFR|RegisterIndirect|Literal['DPTR']|C|SFRBit,
            src:Register|str|SFR|RegisterIndirect|A|C|SFRBit,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'MOV' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            elif _immediate_check(src):
                cycle = 1
                length = 2      
            else:
                raise SourceOperandError()
            flag = ['P']
        elif _register_check(dest):
            if src in get_args(A):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 2
                length = 2
            elif _immediate_check(src):
                cycle = 1
                length = 2    
            else:
                raise SourceOperandError()
            flag = []
        elif _direct_address_check(dest) or _SFR_check(dest):
            if src in get_args(A):
                cycle = 1
                length = 2
            elif _register_check(src):
                cycle = 2
                length = 2
            elif _direct_address_check(src) or _SFR_check(dest):
                cycle = 2
                length = 3
            elif _register_indirect_check(src):
                cycle = 2
                length = 2
            elif _immediate_check(src):
                cycle = 2
                length = 3
            else:
                raise SourceOperandError()
            flag = []
        elif _register_indirect_check(dest):
            if src in get_args(A):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 2
                length = 2
            elif _immediate_check(src):
                cycle = 1
                length = 2
            else:
                raise SourceOperandError()
            flag = []
        elif dest == 'DPTR':
            if (src.startswith('#')
                    and src[1].isnumeric()
                    and src.endswith('H') 
                    and len(src) in (6,7)
                    ):
                cycle = 2
                length = 3
            else:
                raise SourceOperandError()
            flag = []
        elif dest in get_args(C):
            if _bit_check(src):
                cycle = 2
                length = 2
            else:
                raise SourceOperandError()
            flag = ['Cy']
        elif _bit_check(dest):
            if src in get_args(C):
                cycle = 2
                length = 2
            else:
                raise SourceOperandError()
            flag = []
        else:
            raise DestinationOperandError()
        asm = f'MOV {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)   
    
    @staticmethod     
    def push(src:str|SFR,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'PUSH' instruction.
        Args:
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if _direct_address_check(src) or _SFR_check(src):
            cycle = 2
            length = 2
            flag = []
        else:
            raise SourceOperandError()
        asm = f'PUSH {src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod   
    def pop(dest:str|SFR,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'POP' instruction.
        Args:
            dest: An operand indicates the destination register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if _direct_address_check(dest) or _SFR_check(dest):
            cycle = 2
            length = 2
            flag = []
        else:
            raise DestinationOperandError()
        asm = f'POP {dest}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod 
    def movx(dest:A|RegisterIndirect|Literal['@DPTR'],
            src:RegisterIndirect|Literal['@DPTR']|A,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'MOVX' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if src == '@DPTR':
                cycle = 2
                length = 1
            elif _register_indirect_check(src):
                cycle = 2
                length = 1
            else:
                raise SourceOperandError()
            flag = ['P']
        elif dest == '@DPTR':
            if src in get_args(A):
                cycle = 2
                length = 1
            else:
                raise SourceOperandError()
            flag = []
        elif _register_indirect_check(dest):
            if src in get_args(A):
                cycle = 2
                length = 1
            else:
                raise SourceOperandError()
            flag = []
        else:
            raise DestinationOperandError()
        asm = f'MOVX {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def movc(dest:A,src:Literal['@A+PC','@A+DPTR'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'MOVC' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if src == '@A+PC':
                cycle = 2
                length = 1
            elif src == '@A+DPTR':
                cycle = 2
                length = 1
            else:
                raise SourceOperandError()
            flag = ['P']
        else:
            raise DestinationOperandError()
        asm = f'MOVC {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def xch(dest:A,src:Register|str|SFR|RegisterIndirect,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'XCH' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            else:
                raise SourceOperandError()
            flag = ['P']
        else:
            raise DestinationOperandError()
        asm = f'XCH {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def xchd(dest:A,src:RegisterIndirect,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'XCHD' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if _register_indirect_check(src):
                cycle = 1
                length = 1
            else:
                raise SourceOperandError()
            flag = ['P']
        else:
            raise DestinationOperandError()
        asm = f'XCHD {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def swap(operand:A,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'SWAP' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = ['P']
        else:
            raise OperandError()
        asm = f'SWAP {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    ## ========================== Math Calculate Instruction ========================== ##
    @staticmethod
    def add(dest:A,src:Register|str|SFR|RegisterIndirect,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'ADD' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            elif _immediate_check(src):
                cycle = 1
                length = 2
            else:
                raise SourceOperandError()
            flag = ['Cy','Ac','OV','P']
        else:
            raise DestinationOperandError()
        asm =f'ADD {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def addc(dest:A,src:Register|str|SFR|RegisterIndirect,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'ADDC' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            elif _immediate_check(src):
                cycle = 1
                length = 2
            else:
                raise SourceOperandError()
            flag = ['Cy','Ac','OV','P']
        else:
            raise DestinationOperandError()
        asm = f'ADDC {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def subb(dest:A,src:Register|str|SFR|RegisterIndirect,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'SUBB' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            elif _immediate_check(src):
                cycle = 1
                length = 2
            else:
                raise SourceOperandError()
            flag = ['Cy','Ac','OV','P']
        else:
            raise DestinationOperandError()
        asm = f'SUBB {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def inc(operand:A|Register|str|SFR|RegisterIndirect|Literal['DPTR'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'INC' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = ['P']
        elif _register_check(operand):
            cycle = 1
            length = 1
            flag = []
        elif _direct_address_check(operand) or _SFR_check(operand):
            cycle = 1
            length = 2
            flag = []
        elif _register_indirect_check(operand):
            cycle = 1
            length = 1
            flag = []
        elif operand == 'DPTR':
            cycle = 2
            length = 1
            flag = []
        else:
            raise OperandError()
        asm = f'INC {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def dec(operand:A|Register|str|SFR|RegisterIndirect,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'DEC' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = ['P']
        elif _register_check(operand):
            cycle = 1
            length = 1
            flag = []
        elif _direct_address_check(operand) or _SFR_check(operand):
            cycle = 1
            length = 2
            flag = []
        elif _register_indirect_check(operand):
            cycle = 1
            length = 1
            flag = []
        else:
            raise OperandError()
        asm = f'DEC {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def mul(operand:Literal['AB'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'MUL' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand == 'AB':
            cycle = 4
            length = 1
            flag = ['OV','Cy','P']
        else:
            raise OperandError()
        asm = 'MUL AB'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def div(operand:Literal['AB'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'DIV' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand == 'AB':
            cycle = 4
            length = 1
            flag = ['OV','Cy','P']
        else:
            raise OperandError()
        asm = 'DIV AB'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def da(operand:A,
        label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'DA' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = ['Cy','Ac']
        else:
            raise OperandError()
        asm = f'DA {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    ## ========================= Logic Operation Instruction ========================= ## 
    @staticmethod
    def anl(dest:A|str|SFR|C,
            src:Register|str|SFR|RegisterIndirect|A|SFRBit|ReverseSFRBit,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'ANL' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        ''' 
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            elif _immediate_check(src):
                cycle = 1
                length = 2
            else: 
                raise SourceOperandError()
            flag = ['P']
        elif _direct_address_check(dest) or _SFR_check(dest):
            if src in get_args(A):
                cycle = 1
                length = 2
            elif _immediate_check(src):
                cycle = 1
                length = 3
            else:
                raise SourceOperandError()
            flag = []
        elif dest in get_args(C):
            test_src = src.strip('/')
            if _bit_check(test_src):
                cycle = 2
                length = 2
            else:
                raise SourceOperandError()
            flag = ['Cy']
        else:
            raise DestinationOperandError()
        asm = f'ANL {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def orl(dest:A|str|SFR|C,
            src:Register|str|SFR|RegisterIndirect|A|SFRBit|ReverseSFRBit,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'ORL' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        ''' 
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            elif _register_indirect_check(src):
                cycle = 1
                length = 2
            else:
                raise SourceOperandError()
            flag = ['P']
        elif _direct_address_check(dest) or _SFR_check(dest):
            if src in get_args(A):
                cycle = 2
                length = 2
            elif _immediate_check(src):
                cycle = 2
                length = 3
            else:
                raise SourceOperandError()
            flag = []
        elif dest in get_args(C):
            test_src = src.strip('/')
            if _bit_check(test_src):
                cycle = 2
                length = 2
            else:
                raise SourceOperandError()
            flag = ['Cy']
        else:
            raise DestinationOperandError()
        asm = f'ORL {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def xrl(dest:A|str|SFR,src:Register|str|SFR|RegisterIndirect|A,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'XRL' instruction.
        Args:
            dest: An operand indicates the destination register.
            src: An operand indicates the source register.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if dest in get_args(A):
            if _register_check(src):
                cycle = 1
                length = 1
            elif _direct_address_check(src) or _SFR_check(src):
                cycle = 1
                length = 2
            elif _register_indirect_check(src):
                cycle = 1
                length = 1
            elif _immediate_check(src):
                cycle = 1
                length = 2
            else:
                raise SourceOperandError()
            flag = ['P']
        elif  _direct_address_check(dest) or _SFR_check(dest):
            if src in get_args(A):
                cycle = 1
                length = 2
            elif _immediate_check(src):
                cycle = 2
                length = 3
            else:
                raise SourceOperandError()
            flag = []
        else:
            raise DestinationOperandError()
        asm = f'XRL {dest},{src}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def clr(operand:A|C|str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'CLR' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = ['P']
        elif operand in get_args(C):
            cycle = 1
            length = 1
            flag = ['Cy']
        elif _bit_check(operand):
            cycle = 1
            length = 2
            flag = []
        else:
            raise OperandError()
        asm = f'CLR {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def cpl(operand:A|C|str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'CPL' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = []
        elif operand in get_args(C):
            cycle = 1
            length = 1
            flag = ['Cy']
        elif _bit_check(operand):
            cycle = 1
            length = 2
            flag = []
        else:
            raise OperandError()
        asm = f'CPL {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)  

    @staticmethod
    def rl(operand:A,
        label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'RL' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = []
        else:
            raise OperandError()
        asm = f'RL {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def rlc(operand:A,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'RLC' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = ['Cy','P']
        else:
            raise OperandError()
        asm = f'RLC {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def rr(operand:A,
        label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'RR' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = []
        else:
            raise OperandError()
        asm = f'RR {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def rrc(operand:A,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'RRC' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(A):
            cycle = 1
            length = 1
            flag = ['Cy','P']
        else:
            raise OperandError()
        asm = f'RRC {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    ## ========================= Transfer Control Instruction ========================= ##
    @staticmethod
    def acall(destination:str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'ACALL' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 2
        flag = []
        asm = f'ACALL {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def lcall(destination:str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'LCALL' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 3
        flag = []
        asm = f'LCALL {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def ret(label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'RET' instruction.
        Args:
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 1
        flag = []
        asm = 'RET'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def reti(label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'RETI' instruction.
        Args:
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 1
        flag = []
        asm = 'RETI'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def ajmp(destination:str|Literal['$'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'AJMP' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 2
        flag = []
        asm = f'AJMP {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def ljmp(destination:str|Literal['$'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'LJMP' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 3
        flag = []
        asm = f'LJMP {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def sjmp(destination:str|Literal['$'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'SJMP' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 2
        flag = []
        asm = f'SJMP {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def jmp(operand:Literal['@A+DPTR'],
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'JMP' instruction.
        Args:
            operand: An operand indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand == '@A+DPTR':
            cycle = 2
            length = 1
            flag = []
        else:
            raise OperandError()
        asm = f'JMP {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def jz(destination:str,
        label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'JZ' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 2
        flag =[]
        asm = f'JZ {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def jnz(destination:str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'JNZ' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 2
        flag = []
        asm = f'JNZ {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def cjne(operand_1:A|Register|RegisterIndirect,operand_2:str|SFR,
            destination:str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'CJNE' instruction.
        Args:
            operand_1: An operand indicates the first operand of the instruction.
            operand_2: An operand indicates the second operand of the instrucetion.
            destination: An address indicates destination of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand_1 in get_args(A):
            if _direct_address_check(operand_2) or _SFR_check(operand_2):
                cycle = 2
                length = 3
            elif _immediate_check(operand_2):
                cycle = 2
                length = 3
            else:
                raise OperandError('Invalid operand in second operand.')
        elif _register_check(operand_1):
            if _immediate_check(operand_2):
                cycle = 2
                length = 3
            else:
                raise OperandError('Invalid operand in second operand.')
        elif _register_indirect_check(operand_1):
            if _immediate_check(operand_2):
                cycle = 2
                length = 3
            else:
                raise OperandError('Invalid operand in second operand.')
        else:
            raise OperandError('Invalid operand in first operand.')
        flag = ['Cy']
        asm = f'CJNE {operand_1},{operand_2},{destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def djnz(operand:Register|str|SFR,destination:str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'DJNZ' instruction.
        Args:
            operand: An operand for the operation.
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if _register_check(operand):
            cycle = 2
            length = 2
        elif _direct_address_check(operand) or _SFR_check(operand):
            cycle = 2
            length = 3
        else:
            raise OperandError()
        flag = []
        asm = f'DJNZ {operand},{destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def nop(label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'NOP' instruction.
        Args:
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 1
        length = 1
        flag = []
        asm = 'NOP'
        return Instruction(asm,label,comment,cycle,length,flag)

    ## ========================== Bit Operation Instruction ========================== ## 
    @staticmethod
    def setb(operand:C|str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'SETB' instruction.
        Args:
            operand: An operand for the operation.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if operand in get_args(C):
            cycle = 1
            length = 1
            flag = ['Cy']
        elif _bit_check(operand):
            cycle = 1
            length = 2
            flag = []
        else:
            raise OperandError()
        asm = f'SETB {operand}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def jc(destination:str,
        label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'JC' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 2
        flag = []
        asm = f'JC {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def jnc(destination:str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'JNC' instruction.
        Args:
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        cycle = 2
        length = 2
        flag = []
        asm = f'JNC {destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def jb(operand:str|SFRBit,destination:str,
        label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'JB' instruction.
        Args:
            operand: An operand for the operation.
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if _bit_check(operand):
            cycle = 2
            length = 3
        else:
            raise OperandError()
        flag = []
        asm = f'JB {operand},{destination}'
        return Instruction(asm,label,comment,cycle,length,flag)    

    @staticmethod
    def jnb(operand:str|SFRBit,destination:str,
            label:str=None,comment:str=None) -> Instruction:
        '''The function is defined for working with 'JNB' instruction.
        Args:
            operand: An operand for the operation.
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if _bit_check(operand):
            cycle = 2
            length = 3
        else:
            raise OperandError()
        flag = []
        asm = f'JNB {operand},{destination}'
        return Instruction(asm,label,comment,cycle,length,flag)

    @staticmethod
    def jbc(operand:str|SFRBit,destination:str,
            label:str=None,comment:str=None) -> Instruction:    
        '''The function is defined for working with 'JBC' instruction.
        Args:
            operand: An operand for the operation.
            destination: An address indicates destination of the instruction.
            label: A string indicates the label of the instruction.
        Returns:
            Instruction: A object indicates the instruction string and its parameters.
        '''
        if _bit_check(operand):
            cycle = 2
            length = 3
        else:
            raise OperandError()
        if operand in get_args(C):
            flag = ['Cy']
        else:
            flag = []
        asm = f'JBC {operand},{destination}'
        return Instruction(asm,label,comment,cycle,length,flag)