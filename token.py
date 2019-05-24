from enum import Enum, auto


class TokenTypes(Enum):
    def __init__(self):
        Programm = auto()
        BasicBlock = auto()
        Assignment = auto()
        Var = auto()
        Constant = auto()
        Jump = auto()
        Expr = auto()
        Label = auto()
        Op = auto()


class Token:
    def __init__(self, token_type: TokenTypes, name: str):
        self.type = token_type
        self.name = name
        self.value = None

    def set_value(self, value):
        self.value = value
