from types import MethodType,FunctionType
from functools import wraps
from .blocks import Block
from ..pseudo import Pseudo

class ASMCode(Pseudo):
    '''The class is defined to work with ASM instruction blocks and pseudos.'''
    ### ============================== Magic Method ============================== ###
    def __init__(self):
        '''The method is defined to initialize ASMCode class.'''
        # Overwrite original ASM pseudos
        pseudos = dir(Pseudo)
        for name in pseudos:
            if name.startswith('_'):
                continue
            object = getattr(self,name)
            if not isinstance(object,FunctionType):
                continue
            func = self._catchable_pseudo(object)
            setattr(self,name,func)
        # Define asm attribute
        self._asm = []

    def __enter__(self) -> "ASMCode":
        '''The method is defined to enter content manager.'''
        # Overwrite original Block __exit__ method
        self._orgin_block_exit = Block.__exit__
        Block.__exit__ = self._catchable_block(Block.__exit__)
        return self

    def __exit__(self,type,instance,traceback):
        '''The method is defined to exite content manager.'''
        # Restore original Block __exit__ method
        Block.__exit__ = self._orgin_block_exit

    ### ============================== Normal Method ============================== ###
    def encode(self) -> str:
        '''The method is defined to encode Python codes to ASM codes.
        Returns:
            A string indicates the valid ASM codes.
        '''
        # Make indent
        label_numbers = []
        asm_numbers = []
        for object in self._asm:
            if type(object) == str:
                asm_number = len(object)
                asm_numbers.append(asm_number)
            else:
                for instruction in object._instructions:
                    asm:str = instruction.asm
                    label:str = instruction.label
                    if label != None:
                        label_number = len(label)
                    else:
                        label_number = 0
                    label_numbers.append(label_number)
                    asm_number = len(asm)
                    asm_numbers.append(asm_number)
        pre_label_indent = max(label_numbers) + 1
        pre_asm_indent = max(asm_numbers)
        label_indent = (4 - (pre_label_indent % 4)) + pre_label_indent
        asm_indent = (4 - (pre_asm_indent % 4)) + pre_asm_indent
        pre_comment_indent = label_indent + asm_indent
        # Make ASM code string
        asm_code = ''
        for object in self._asm:
            if type(object) == str:
                asm_code += f'{' ':<{label_indent}}{object}\n'
            else:
                for instruction in object._instructions:
                    asm = instruction.asm
                    label:str = instruction.label
                    comment = instruction.comment
                    if label != None:
                        pre_asm = f'{f'{label}:':<{label_indent}}{asm}'
                    else:
                        pre_asm = f'{' ':<{label_indent}}{asm}'
                    if comment != None:
                        asm_code += f'{pre_asm:<{pre_comment_indent}};{comment}\n'
                    else:
                        asm_code += f'{pre_asm:<{pre_comment_indent}}\n'
        # Return ASM code string
        return asm_code

    ### ============================= Class Decorator ============================= ###
    def _catchable_block(self,func:MethodType) -> MethodType:
        '''This is a decorator to catch instruction block instance.'''
        @wraps(func)
        def wrapped_method(object,*args,**kwargs):
            self._asm.append(object)
            return func(object,*args,**kwargs)
        return wrapped_method

    def _catchable_pseudo(self,func:FunctionType) -> MethodType:
        '''This is a decorator to catch ASM pseudo functions' return.'''
        @wraps(func)
        def wrapped_func(*args,**kwargs):
            pseudo = func(*args,**kwargs)
            self._asm.append(pseudo)
        return wrapped_func