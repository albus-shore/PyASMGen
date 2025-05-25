from warnings import warn
from .utils.pseudo import Indication

### ============================== Args Check Functions ============================== ###
def _address_check(address:str) -> bool:
    '''The function is defined for check whether address is valid.
    Args: 
        address: A string indicates the address to check.
    Returns:
        A boolean indicates whether the address is vaild.
    '''
    if address[0].isnumeric() and address.endswith('H'):
        return True
    else:
        return False

### ============================ Expose Pseudo Functions ============================ ###
class Pseudo:
    '''The class is defined to work with pseudos.'''

    @staticmethod
    def org(address:str) -> Indication:
        '''The function is defined for working with 'ORG' pseudo.
        Args:
            address: A string indicates the strat address of following codes.
        Returns:
            An Indication instance indicates the valid 'ORG' pseudo.    
        '''
        if not _address_check(address):
            warn('Abnormal ROM address.',UserWarning)
        asm = f'ORG {address}'
        return Indication(asm)

    @staticmethod
    def end() -> Indication:
        '''The function is defined for working with 'END' pseudo.
        Returns:
            An Indication instance indicates the valid 'END' pseudo.    
        '''
        asm = 'END'
        return Indication(asm)

    @staticmethod
    def equ(label:str,address:str) -> Indication:
        '''The function is defined for working with 'EQU' pseudo.
        Args:
            label: A string indicates the label to define.
            address: A string indicates the strat address of following codes.
        Returns:
            An Indication instance indicates the valid 'EQU' pseudo.    
        '''
        if not _address_check(address):
            warn('Abnormal ROM address.',UserWarning)
        asm = f'{label} EQU {address}'
        return Indication(asm)

    @staticmethod
    def db(*values) -> Indication:
        '''The function is defined for working with 'DB' pseudo.
        Args:
            values: Some values indicates the values to define in ROM.
        Returns:
            An Indication instance indicates the valid 'DB' pseudo.    
        '''
        seperated_values = ','.join(str(value) for value in values)
        asm = f'DB {seperated_values}'
        return Indication(asm)

    @staticmethod
    def dw(*values) -> Indication:
        '''The function is defined for working with 'DW' pseudo.
        Args:
            values: Some values indicates the values to define in ROM.
        Returns:
            An Indication instance indicates the valid 'DW' pseudo.    
        '''
        seperated_values = ','.join(str(value) for value in values)
        asm = f'DW {seperated_values}'
        return Indication(asm)

    @staticmethod
    def ds(byte:str) -> Indication:
        '''The function is defined for working with 'DS' pseudo.
        Args:
            byte: A string indicates the number of bytes to keep.
        Returns:
            An Indication instance indicates the valid 'DS' pseudo.    
        '''
        asm = f'DS {byte}'
        return Indication(asm)

    @staticmethod
    def bit(label:str,bit:str) -> Indication:
        '''The function is defined for working with 'BIT' pseudo.
        Args:
            label: A string indicates the label to define.
            bit: A string indicates the bit signed to the label.
        Returns:
            An Indication instance indicates the valid 'BIT' pseudo.    
        '''
        asm = f'{label} BIT {bit}'
        return Indication(asm)