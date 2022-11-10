from . import *
from enum import Enum, auto


class TokenType(Enum):
    """Enumerates the possible types of tokens"""
    COLON = auto()
    ARROW = auto()
    SPACE = auto()
    NEW_LINE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    DIV = auto()
    MOD = auto()

    PIPE = auto()
    QUESTION = auto()

    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    TRUE = auto()
    FALSE = auto()

    EOF = auto()

class ErrorType(Enum):
    SyntaxError = 'SyntaxError'
