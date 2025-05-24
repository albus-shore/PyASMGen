from types import FunctionType,MethodType
from functools import wraps
from ..instructions.C8051 import C8051

### ================================= Basic Class ================================= ###
class Block(C8051):
    '''The class is defined to work with a branch of ASM codes.'''
    def __init__(self,label:str=None,org:str=None):
        '''The method is defined to initialize Block class.
        Args:
            label: A string indicates the label of the instruction.
            org: A string indicates the strat address of including codes.
        '''
        # Get input arguments
        self.label = label
        self.org = org
        # Overwrite original ASM instructions
        instructions = dir(C8051)
        for name in instructions:
            if name.startswith('_'):
                continue
            object = getattr(self,name)
            if not isinstance(object,FunctionType):
                continue
            func = self._catchable_instruction(object)
            setattr(self,name,func)
        # Define instructions attribute
        self._instructions =[]

    def __enter__(self) -> "Block":
        '''The method is defined to enter content manager.'''
        return self

    def __exit__(self,type,instance,traceback):
        '''The method is defined to exite content manager.'''
        pass

    def _catchable_instruction(self,func:FunctionType) -> MethodType:
        '''This is a decorator to catch ASM instruction functions' return.'''
        @wraps(func)
        def warpped_func(*args,**kwargs):
            instruction = func(*args,**kwargs)
            self._instructions.append(instruction)
        return warpped_func