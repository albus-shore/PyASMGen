from warnings import warn

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
    def org(address:str) -> str:
        '''The function is defined for working with 'ORG' pseudo.
        Args:
            address: A string indicates the strat address of following codes.
        Returns:
            A string indicate the valid 'ORG' pseudo.    
        '''
        if not _address_check(address):
            warn('Abnormal ROM address.',UserWarning)
        return f'ORG {address}'
    
    @staticmethod
    def end() -> str:
        '''The function is defined for working with 'END' pseudo.
        Returns:
            A string indicate the valid 'END' pseudo.    
        '''
        return 'END'

    @staticmethod
    def equ(label:str,address:str) -> str:
        '''The function is defined for working with 'EQU' pseudo.
        Args:
            label: A string indicates the label to define.
            address: A string indicates the strat address of following codes.
        Returns:
            A string indicate the valid 'EQU' pseudo.    
        '''
        if not _address_check(address):
            warn('Abnormal ROM address.',UserWarning)
        return f'{label} EQU {address}'

    @staticmethod
    def db(*values) -> str:
        '''The function is defined for working with 'DB' pseudo.
        Args:
            values: Some values indicates the values to define in ROM.
        Returns:
            A string indicate the valid 'DB' pseudo.    
        '''
        seperated_values = ','.join(str(value) for value in values)
        return f'DB {seperated_values}'

    @staticmethod
    def dw(*values) -> str:
        '''The function is defined for working with 'DW' pseudo.
        Args:
            values: Some values indicates the values to define in ROM.
        Returns:
            A string indicate the valid 'DW' pseudo.    
        '''
        seperated_values = ','.join(str(value) for value in values)
        return f'DW {seperated_values}'

    @staticmethod
    def ds(byte:str) -> str:
        '''The function is defined for working with 'DS' pseudo.
        Args:
            byte: A string indicates the number of bytes to keep.
        Returns:
            A string indicate the valid 'DS' pseudo.    
        '''
        return f'DS {byte}'

    @staticmethod
    def bit(label:str,bit:str) -> str:
        '''The function is defined for working with 'BIT' pseudo.
        Args:
            label: A string indicates the label to define.
            bit: A string indicates the bit signed to the label.
        Returns:
            A string indicate the valid 'BIT' pseudo.    
        '''
        return f'{label} BIT {bit}'