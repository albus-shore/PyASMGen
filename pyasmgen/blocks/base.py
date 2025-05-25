from types import FunctionType,MethodType
from functools import wraps
from ..utils.block import catchable_block
from ..utils.instruction import Instruction
from ..instructions import C8051

### ================================= Basic Class ================================= ###
class Block(C8051):
    '''The class is defined to work with a branch of ASM codes.'''
    def __init__(self,label:str=None):
        '''The method is defined to initialize Block class.
        Args:
            label: A string indicates the label of the instruction.
        '''
        # Get input arguments
        self.label = label
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
        self._codes = []
        self._instructions =[]

    def __enter__(self) -> "Block":
        '''The method is defined to enter content manager.'''
        # Overwrite original Block __exit__ method
        self._orgin_block_exit = Block.__exit__
        Block.__exit__ = catchable_block(self._codes)(Block.__exit__.__wrapped__)
        return self

    def __exit__(self,type,instance,traceback):
        '''The method is defined to exite content manager.'''
        # Restore original Block __exit__ method
        Block.__exit__ = self._orgin_block_exit
        # Extract nest blocks' instructions
        for object in self._codes:
            if isinstance(object,Instruction):
                self._instructions.append(object)
            elif isinstance(object,Block):
                # Rewirte first instruction's label if necessary
                if object.label:
                    object._instructions[0].label = object.label
                # Extend the block's instruction attribute
                self._instructions.extend(object._instructions)

    def _catchable_instruction(self,func:FunctionType) -> MethodType:
        '''This is a decorator to catch ASM instruction functions' return.'''
        @wraps(func)
        def warpped_func(*args,**kwargs):
            instruction = func(*args,**kwargs)
            self._codes.append(instruction)
        return warpped_func