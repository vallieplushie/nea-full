from . import *
from sys import exit
from enum import Enum, auto

class ErrorType:
    SyntaxError = 'SyntaxError'
    NameUndefinedError = 'NameUndefinedError'
    OperatorUseError = 'OperatorUseError'

class Error:
    @staticmethod
    def throw(type: ErrorType, line: int, message: str=None):
        output = ''
        output += f'[Line {line}] {type}: '

        if message is None:
            output += ''
        else:
            output += message

        if LICONF.INTERACTIVE_MODE: 
            output = '<e> ' + output
            LICONF.HAD_ERROR = True 
            print(output)
            return
        else:
            print(output)
            exit(64)


