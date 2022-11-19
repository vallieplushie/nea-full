from . import *

class Action:
    """
    Default action class, exports 3 methods:
        check :: Action -> bool
        run :: Action -> Environment -> Environment
        name :: Action -> str
    """

    def __init__(self) -> None:
        self.left: Tree = None
        self.right: Tree = None

    def check(self, *args) -> bool:
        return False 

    @StatusHandler.checkerror
    def run(self, glob: Environment) -> Environment:
        return glob

    def name(self) -> str:
        return f'Action'


class AssignAction(Action):
    def __init__(self) -> None:
        super().__init__()
    
    def check(self) -> bool:
        if self.left.data.type is TokenType.IDENTIFIER:
            return True
        else:
            StatusHandler.throw(ErrorType.OperandError, self.left.data.line, 
                                f'Cannot assign to something that is not an identifier.')
            return False

    @StatusHandler.checkerror
    def run(self, glob: Environment) -> Environment:
        if not self.check():
            pass
        else:
            newenv = EnvMonad(glob)
            self.left.action.context = 'DEFINITION'
            newenv >> self.left.action
            glob = newenv.env
            glob.stackmonad >> Stack.pop()
            id = glob.stackmonad.out[-1]
            # if the right is an explicit function, should wrap in a scope
            if self.right.data.type is TokenType.ARROW:
                newenv = EnvMonad(glob)
                newenv >> self.right.action
                glob = newenv.env
                glob.stackmonad >> Stack.pop() 
                scope = glob.stackmonad.out[-1]
                glob.table[id] = scope
            else:
                glob.table[id] = self.right
            glob.stackmonad >> Stack.push(Token(TokenType.IDENTIFIER, 'assigned', 1))

        return glob


class LiteralAction(Action):
    def __init__(self, value: Token) -> None:
        self.value = value
        super().__init__()

    @StatusHandler.logging('INFO')
    def run(self, glob: Environment) -> Environment:
        glob.stackmonad >> Stack.push(self.value)
        return EnvMonad(glob)

    def name(self):
        return f'Literal Action, literal is {self.value}'


class IdentifierAction(Action):
    def __init__(self, name: Token) -> None:
        self.id = name
        self.context = 'REFERENCE'
        super().__init__()
    
    # 'REFERENCE' or 'DEFINITION'
    def run(self, glob):
        if self.context == 'REFERENCE':
            if glob.table.get(self.id.lexeme) is None:
                StatusHandler.throw(ErrorType.NameUndefinedError, self.id.line,
                                    f'The name {self.id.lexeme} does not exist in the current scope.') 
            else:
                # glob.stackmonad >> Stack.push(self.id.lexeme)
                newenv = EnvMonad(glob)
                newenv >> glob.table.get(self.id.lexeme).action
                glob = newenv.env

        elif self.context == 'DEFINITION':
            if glob.table.get(self.id.lexeme) is not None:
                StatusHandler.throw(ErrorType.NameRedefinitionError, self.id.line,
                                    f'Trying to redefine {self.id.lexeme} even though it is already defined.') 
            else:
                glob.stackmonad >> Stack.push(self.id.lexeme)

    def name(self):
        return f'Identifier Action, identifier is {self.id}'


class ArithmeticAction(Action):
    def __init__(self) -> None:
        self.left_val = None
        self.right_val = None
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def check(self, glob: Environment, left: Token, right: Token) -> bool: 
        if left.type is TokenType.IDENTIFIER:
            if glob.table.get(left.lexeme) is None:
                StatusHandler.throw(ErrorType.NameUndefinedError, left.line,
                                    f'The name {left.lexeme} does not exist in the current scope.') 
                return False

            elif not isinstance(glob.table.get(left.lexeme), int):
                StatusHandler.throw(ErrorType.TypeError, left.line,
                                    f'The identifier {left.lexeme} does not return.')
                return False

            else:
                self.left_val = glob.table.get(left.lexeme)
        elif left.type is TokenType.NUMBER:
            self.left_val = left.literal

        if right.type is TokenType.IDENTIFIER:
            if glob.table.get(right.literal) is None:
                print(f'Name Undefined Error')
                return False

            elif not isinstance(glob.table.get(right.lexeme), int):
                print(f'Wrong type')
                return False
            else:
                self.right_val = glob.table.get(right.lexeme)
        elif right.type is TokenType.NUMBER:
            self.right_val = right.literal

        return True


class AdditionAction(ArithmeticAction):
    def __init__(self) -> None:
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def run(self, glob: Environment) -> Environment:
        # Do the left and right actions
        newenv = EnvMonad(glob)
        newenv >> self.left.action
        newenv >> self.right.action
        
        # Extract the environment, then get the arguments
        glob = newenv.env
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        left_op = glob.stackmonad.out[-1]
        right_op = glob.stackmonad.out[-2]

        is_allowed = self.check(glob, left_op, right_op)

        if is_allowed:
            result = self.left_val + self.right_val
            glob.stackmonad >> Stack.push(Token(TokenType.NUMBER, str(result), left_op.line, result))
        else:
            print(f'type error')

    def name(self) -> str:
        return f'AdditionAction with {self.left_val} and {self.right_val}'

class SubtractionAction(ArithmeticAction):
    def __init__(self) -> None:
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def run(self, glob: Environment) -> Environment:
        # Do the left and right actions
        newenv = EnvMonad(glob)
        newenv >> self.left.action
        newenv >> self.right.action
        
        # Extract the environment, then get the arguments
        glob = newenv.env
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        left_op = glob.stackmonad.out[-1]
        right_op = glob.stackmonad.out[-2]

        is_allowed = self.check(glob, left_op, right_op)

        if is_allowed:
            result = self.left_val - self.right_val
            glob.stackmonad >> Stack.push(Token(TokenType.NUMBER, str(result), left_op.line, result))
        else:
            print(f'type error')

    def name(self) -> str:
        return f'SubtractionAction with {self.left_val} and {self.right_val}'

class MultiplicationAction(ArithmeticAction):
    def __init__(self) -> None:
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def run(self, glob: Environment) -> Environment:
        # Do the left and right actions
        newenv = EnvMonad(glob)
        newenv >> self.left.action
        newenv >> self.right.action
        
        # Extract the environment, then get the arguments
        glob = newenv.env
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        left_op = glob.stackmonad.out[-1]
        right_op = glob.stackmonad.out[-2]

        is_allowed = self.check(glob, left_op, right_op)

        if is_allowed:
            result = self.left_val * self.right_val
            glob.stackmonad >> Stack.push(Token(TokenType.NUMBER, str(result), left_op.line, result))
        else:
            print(f'type error')

    def name(self) -> str:
        return f'MultiplicationAction with {self.left_val} and {self.right_val}'

class DivisionAction(ArithmeticAction):
    def __init__(self) -> None:
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def run(self, glob: Environment) -> Environment:
        # Do the left and right actions
        newenv = EnvMonad(glob)
        newenv >> self.left.action
        newenv >> self.right.action
        
        # Extract the environment, then get the arguments
        glob = newenv.env
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        left_op = glob.stackmonad.out[-1]
        right_op = glob.stackmonad.out[-2]

        is_allowed = self.check(glob, left_op, right_op)

        if is_allowed:
            result = self.left_val / self.right_val
            glob.stackmonad >> Stack.push(Token(TokenType.NUMBER, str(result), left_op.line, result))
        else:
            print(f'type error')

    def name(self) -> str:
        return f'DivisionAction with {self.left_val} and {self.right_val}'
            

class BooleanAction(Action):
    def __init__(self) -> None:
        self.left_val = None
        self.right_val = None
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def check(self, glob: Environment, left: Token, right: Token) -> bool: 
        if left.type is TokenType.IDENTIFIER:
            if glob.table.get(left.lexeme) is None:
                StatusHandler.throw(ErrorType.NameUndefinedError, left.line,
                                    f'The name {left.lexeme} does not exist in the current scope.') 
                return False

            elif not isinstance(glob.table.get(left.lexeme), int):
                StatusHandler.throw(ErrorType.TypeError, left.line,
                                    f'The identifier {left.lexeme} does not return.')
                return False

            else:
                self.left_val = glob.table.get(left.lexeme)
        elif left.type in [TokenType.TRUE, TokenType.FALSE]:
            self.left_val = left.literal

        if right.type is TokenType.IDENTIFIER:
            if glob.table.get(right.literal) is None:
                print(f'Name Undefined Error')
                return False

            elif not isinstance(glob.table.get(right.lexeme), int):
                print(f'Wrong type')
                return False
            else:
                self.right_val = glob.table.get(right.lexeme)
        elif right.type in [TokenType.TRUE, TokenType.FALSE]:
            self.right_val = right.literal

        return True

class AndAction(BooleanAction):
    def __init__(self):
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def run(self, glob: Environment) -> Environment:
        # Do the left and right actions
        newenv = EnvMonad(glob)
        newenv >> self.left.action
        newenv >> self.right.action
        
        # Extract the environment, then get the arguments
        glob = newenv.env
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        left_op = glob.stackmonad.out[-1]
        right_op = glob.stackmonad.out[-2]

        is_allowed = self.check(glob, left_op, right_op)

        if is_allowed:
            result = self.left_val and self.right_val
            if result == True:
                glob.stackmonad >> Stack.push(Token(TokenType.TRUE, str(result), left_op.line, result))
            elif result == False:
                glob.stackmonad >> Stack.push(Token(TokenType.FALSE, str(result), left_op.line, result))
        else:
            StatusHandler.throw(ErrorType.TypeError, left_op.line)

    def name(self) -> str:
        return f'AndAction with {self.left_val} and {self.right_val}'

class OrAction(BooleanAction):
    def __init__(self):
        super().__init__()

    @StatusHandler.checkerror
    @StatusHandler.logging('INFO')
    def run(self, glob: Environment) -> Environment:
        # Do the left and right actions
        newenv = EnvMonad(glob)
        newenv >> self.left.action
        newenv >> self.right.action
        
        # Extract the environment, then get the arguments
        glob = newenv.env
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        left_op = glob.stackmonad.out[-1]
        right_op = glob.stackmonad.out[-2]

        is_allowed = self.check(glob, left_op, right_op)

        if is_allowed:
            print(self.left_val, self.right_val)
            result = self.left_val or self.right_val
            if result == True:
                glob.stackmonad >> Stack.push(Token(TokenType.TRUE, str(result), left_op.line, result))
            elif result == False:
                glob.stackmonad >> Stack.push(Token(TokenType.FALSE, str(result), left_op.line, result))
        else:
            StatusHandler.throw(ErrorType.TypeError, left_op.line)

    def name(self) -> str:
        return f'OrAction with {self.left_val} and {self.right_val}'
