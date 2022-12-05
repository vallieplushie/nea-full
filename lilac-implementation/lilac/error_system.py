from . import *
from sys import exit
from datetime import datetime


class ErrorType():
    SyntaxError = 'SyntaxError'
    NameUndefinedError = 'NameUndefinedError'
    NameRedefinitionError = 'NameRedefinitionError'
    OperatorUseError = 'OperatorUseError'
    OperandError = 'OperandError'
    TypeError = 'TypeError'

class StatusHandler:
    @staticmethod
    def logging(target_level):
        """Decorator which handles logging, can be used in front of any function"""
        def decorator(func):
            def wrapper(*args):
                if LICONF.LOG_TABLE[target_level] >= LICONF.LOG_TABLE[LICONF.LOG_LEVEL]:
                    log_msg = f'[{target_level}][{datetime.now().strftime("%H:%M:%S:%f")}] {func.__module__}.{func.__name__}'
                    if LICONF.LOG_LEVEL == 'TRACE':
                        log_msg += f' {PrettyPrinter.print_args(*args)}'
                    if LICONF.LOG_TYPE == 'CONSOLE':
                        print(log_msg)
                    elif LICONF.LOG_TYPE == 'FILE':
                        with open(LICONF.LOG_PATH, 'a') as file:
                            file.write(log_msg+'\n')
                output = func(*args)
                return output
            return wrapper
        return decorator

    @staticmethod 
    def checkerror(func):
        """Decorator which checks if there has been an error."""
        def wrapper(*args):
            if LICONF.HAD_ERROR:
                return
            else:
                out = func(*args)
                return out
        return wrapper

    @staticmethod
    @logging('ERROR')
    def throw(type: ErrorType, line: int, message: str=''):
        """Called when an error is detected"""
        output = f'[Line {line}] {type}: {message}'

        if LICONF.INTERACTIVE_MODE: 
            output = '<e> ' + output
            LICONF.HAD_ERROR = True 
            print(output)
            return
        else:
            print(output)
            exit(64)

