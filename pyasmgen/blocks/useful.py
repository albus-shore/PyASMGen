from typing import Literal
from .base import Block

### =============================== Jump Need Block =============================== ###
class Initial(Block):
    '''The class is defined to work with initial codes.'''
    name = 'Initial'
    def __init__(self,label='INITIAL',org = '30H'):
        '''The method is defined to initialize Initial class.
        Args:
            label: A string indicates the label of the instruction.
        '''
        super().__init__(label,org)

class Ext0(Block):
    '''The class is defined to work with INT0 codes.'''
    name = 'EXT0'
    def __init__(self,ret_label=None,
                 label='EXT0P',org=None):
        self.ret_label = ret_label
        super().__init__(label,org)

    def _additional_codes(self):
        self.reti(self.ret_label)

class Ext1(Block):
    '''The class is defined to work with INT1 codes.'''
    name = 'EXT1'
    def __init__(self,ret_label=None,
                 label='EXT1P',org=None):
        self.ret_label = ret_label
        super().__init__(label,org)

    def _additional_codes(self):
        self.reti(self.ret_label)

class Int0(Block):
    '''The class is defined to work with TF0 codes.'''
    name = 'INT0'
    def __init__(self,ret_label=None,
                 label='INT0P',org=None):
        self.ret_label = ret_label
        super().__init__(label,org)

    def _additional_codes(self):
        self.reti(self.ret_label)

class Int1(Block):
    '''The class is defined to work with TF1 codes.'''
    name = 'INT1'
    def __init__(self,ret_label=None,
                 label='INT1P',org=None):
        self.ret_label = ret_label
        super().__init__(label,org)

    def _additional_codes(self):
        self.reti(self.ret_label)

class Int2(Block):
    '''The class is defined to work with TF2/EXF2 codes.'''
    name = 'INT2'
    def __init__(self,type:Literal['TF2','EXF2','both'],ret_label=None,
                 label='INT2P',org=None):
        self.type = type
        self.ret_label = ret_label
        super().__init__(label,org)

    def _additional_codes(self):
        if self.type == 'TF2':
            self.clr('TF2',label=self.ret_label)
        elif self.type == 'EXF2':
            self.clr('EXF2',label=self.ret_label)
        elif self.type == 'both':
            self.clr('TF2',label=self.ret_label)
            self.clr('EXF2')
        else:
            raise TypeError('Invalid TF2 work method.')    
        self.reti()

class Serial(Block):
    '''The class is defined to work with serial communication codes.'''
    name = 'Serial'
    def __init__(self,type:Literal['TI','RI','both'],ret_label=None,
                 label='SERIAL',org=None):
        self.type = type
        self.ret_label = ret_label
        super().__init__(label,org)

    def _additional_codes(self):
        if self.type == 'TI':
            self.clr('TI',label=self.ret_label)
        elif self.type == 'RI':
            self.clr('RI',label=self.ret_label)
        elif self.type == 'both':
            self.clr('RI',label=self.ret_label)
            self.clr('TI')    
        else:
            raise TypeError('Invalid serial communication work method.')
        self.reti()

### ============================= Non-Jump Need Block ============================= ###
class Main(Block):
    '''The class is defined to work with mian codes.'''
    name = 'Main'
    def __init__(self,label:str='MAIN',org=None):
        '''The method is defined to initialize Main class.
        Args:
            label: A string indicates the label of the instruction.
        '''
        super().__init__(label,org)

    def _additional_codes(self):
        self.sjmp('$')      