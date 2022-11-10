"""Tokens for representing source code"""

from . import *


class Token:
    """Token class which is used to represent a token in source code"""

    def __init__(self, 
                 type: TokenType, 
                 lexeme: str, 
                 line: int, 
                 literal=None) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f'({self.type}: {self.lexeme}, {self.line})'
