# from . import *
from enum import Enum, auto

class TokenType(Enum):
    """Enumerates the possible types of tokens"""
    COLON = auto()
    ARROW = auto()
    SPACE = auto()
    SEMI_COLON = auto()
    NEW_LINE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    DIV = auto()
    MOD = auto()

    OR = auto()
    AND = auto()
    NOT = auto()
    EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    NOT_EQUAL = auto()

    PIPE = auto()
    QUESTION = auto()

    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    TRUE = auto()
    FALSE = auto()
    IN = auto()

    EOF = auto()

