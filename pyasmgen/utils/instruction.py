from dataclasses import dataclass

@dataclass
class Instruction:
    asm: str
    label: str
    comment: str
    cycle: int
    length: int
    flag:list

class OperandError(Exception):
    def __init__(self, message:str='Invalid operand.'):
        super().__init__(message)

class SourceOperandError(OperandError):
    def __init__(self):
        message = 'Invalid source operand.'
        super().__init__(message)

class DestinationOperandError(OperandError):
    def __init__(self):
        message = 'Invalid destination operand.'
        super().__init__(message)