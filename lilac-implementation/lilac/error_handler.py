from enum import Enum

class ErrorType(Enum):
    """Enumerates possible error types"""
    SyntaxError = 'SyntaxError'
    NameUndefinedError = 'NameUndefinedError'

class ErrorHandler:
    @staticmethod
    def error(err_type: ErrorType, line:int=-1,  msg: str=''):
        """Throws an error"""
        if line == -1:
            err_message = f'{err_type}: {msg}'
        else:
            err_message = f'{err_type} at {line}: {msg}'
        
        Lilac.hadError = True

        if Lilac.interactive:
            print(f'<e> {err_message}')
            return
        else:
            print(err_message)
            exit(65)
