from types import MethodType,FunctionType
from functools import wraps
from .utils.block import catchable_block
from .utils.pseudo import Indication
from .utils.instruction import Instruction
from .blocks import Block
from .pseudos import Pseudo

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
        self._codes = []
        self._asm = []

    def __enter__(self) -> "ASMCode":
        '''The method is defined to enter content manager.'''
        # Overwrite original Block __exit__ method
        self._orgin_block_exit = Block.__exit__
        Block.__exit__ = catchable_block(self._codes)(Block.__exit__)
        return self

    def __exit__(self,type,instance,traceback):
        '''The method is defined to exite content manager.'''
        # Restore original Block __exit__ method
        Block.__exit__ = self._orgin_block_exit
        # Append END pseudo
        self.end()
        # Jump need block support
        term = [0,0,0,0,0,0]
        # Extract blocks' instructions
        for object in self._codes:
            if isinstance(object,Indication):
                self._asm.append(object)
            elif isinstance(object,Block):
                # Append org pseudo if necessary
                if object.org:
                    org = super().org(object.org)
                    self._asm.append(org)
                # Rewirte first instruction's label if necessary
                if object.label:
                    object._instructions[0].label = object.label
                # Extend the block's instruction attribute
                self._asm.extend(object._instructions)
                match object.name:
                    case 'Initial':
                        self._asm.insert(0,Block.ljmp(object.label))
                        self._asm.insert(0,super().org('00H'))
                        term[0] = 1
                    case 'EXT0':
                        index = term[:1].count(1)*2
                        self._asm.insert(index,Block.ljmp(object.label))
                        self._asm.insert(index,super().org('03H'))
                        term[1] = 1
                    case 'INT0':
                        index = term[:2].count(1)*2
                        self._asm.insert(index,Block.ljmp(object.label))
                        self._asm.insert(index,super().org('0BH'))
                        term[2] = 1
                    case 'EXT1':
                        index = term[:3].count(1)*2
                        self._asm.insert(index,Block.ljmp(object.label))
                        self._asm.insert(index,super().org('13H'))
                        term[3] = 1
                    case 'INT1':
                        index = term[:4].count(1)*2
                        self._asm.insert(index,Block.ljmp(object.label))
                        self._asm.insert(index,super().org('1BH'))
                        term[4] = 1
                    case 'Serial':
                        index = term[:5].count(1)*2
                        self._asm.insert(index,Block.ljmp(object.label))
                        self._asm.insert(index,super().org('23H'))
                        term[5] = 1
                    case 'INT2':
                        index = term[:6].count(1)*2
                        self._asm.insert(index,Block.ljmp(object.label))
                        self._asm.insert(index,super().org('2BH'))

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
            if isinstance(object,Indication):
                asm_number = len(object.asm)
                asm_numbers.append(asm_number)
            elif isinstance(object,Instruction):
                if object.label != None:
                    label_number = len(object.label)
                else:
                    label_number = 0
                label_numbers.append(label_number)
                asm_number = len(object.asm)
                asm_numbers.append(asm_number)
            else:
                raise RuntimeError("Invalid object in '_instructions' attribute.")        
        pre_label_indent = max(label_numbers) + 1
        pre_asm_indent = max(asm_numbers)
        label_indent = (4 - (pre_label_indent % 4)) + pre_label_indent
        asm_indent = (4 - (pre_asm_indent % 4)) + pre_asm_indent
        pre_comment_indent = label_indent + asm_indent
        # Make ASM code string
        asm_code = ''
        for object in self._asm:
            if isinstance(object,Indication):
                asm_code += f'{' ':<{label_indent}}{object.asm}\n'
            elif isinstance(object,Instruction):
                if object.label != None:
                    pre_asm = f'{f'{object.label}:':<{label_indent}}'
                    pre_asm += f'{object.asm}'
                else:
                    pre_asm = f'{' ':<{label_indent}}{object.asm}'
                if object.comment != None:
                    pre_asm_code = f'{pre_asm:<{pre_comment_indent}};'
                    pre_asm_code += f'{object.comment}\n'
                    asm_code += pre_asm_code
                else:
                    asm_code += f'{pre_asm:<{pre_comment_indent}}\n'
        # Return ASM code string
        return asm_code

    ### ============================= Class Decorator ============================= ###
    def _catchable_pseudo(self,func:FunctionType) -> MethodType:
        '''This is a decorator to catch ASM pseudo functions' return.'''
        @wraps(func)
        def wrapped_func(*args,**kwargs):
            pseudo = func(*args,**kwargs)
            self._codes.append(pseudo)
        return wrapped_func