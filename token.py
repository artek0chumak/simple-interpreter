from enum import Enum, auto


class TokenTypeError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TokenTypes(Enum):
    def __init__(self):
        Program = auto()
        BasicBlock = auto()
        Assignment = auto()
        Var = auto()
        Constant = auto()
        Jump = auto()
        Expr = auto()
        Label = auto()
        Op = auto()
        Return = auto()


class Token:
    def __init__(self, token_type: TokenTypes, value=None):
        self.type = token_type
        self.value = value

    def set_value(self, value) -> None:
        self.value = value
