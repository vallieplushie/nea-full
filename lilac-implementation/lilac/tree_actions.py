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

    def run(self, glob: Environment) -> Environment:
        return glob

    def name(self) -> str:
        return f'Action'


class ArithmeticAction(Action):
    def __init__(self) -> None:
        self.left_val = None
        self.right_val = None
        super().__init__()

    def check(self, glob: Environment, left: Token, right: Token) -> bool: 
        if left.type is TokenType.IDENTIFIER:
            if glob.table.get(left.lexeme) is None:
                print(f'Name Undefined Error')
                return False

            elif isinstance(glob.table.get(left.lexeme), int):
                print(f'Wrong Type')
                return False

            else:
                self.left_val = glob.table.get(left.lexeme)

        if right.type is TokenType.IDENTIFIER:
            if glob.table.get(right.literal) is None:
                print(f'Name Undefined Error')
                return False

            elif not isinstance(glob.table.get(right.lexeme), int):
                print(f'Wrong type')
                return False

            else:
                self.right_val = glob.table.get(right.lexeme)

        return True


class AdditionAction(ArithmeticAction):
    def __init__(self) -> None:
        super().__init__()

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
            glob.stackk >> Stack.push(result)
        else:
            print(f'type error')

    def name(self) -> str:
        return f'AdditionAction with {self.left_val} and {self.right_val}'
            

class LiteralAction(Action):
    def __init__(self, value: Token) -> None:
        self.value = value
        super().__init__()

    def run(self, glob):
        glob.stackmonad >> Stack.push(self.value)
        return EnvMonad(glob)

    def name(self):
        return f'Literal Action, literal is {self.value}'


# class Action:
#     def __init__(self):
#         self.left = None
#         self.right = None

#     def check(self, glob):
#         pass

# class LiteralAction(Action):
#     def __init__(self, val):
#         self.val = val
#         super().__init__()

#     def run(self, glob):
#         glob.stackmonad >> Stack.push(self.val)
#         return EnvMonad(glob)

#     def name(self):
#         return f'Literal Action, literal is {self.val}'

# class AssignAction(Action):
#     def __init__(self):
#         super().__init__()

#     def run(self, glob):
#         # make a wrapper to do the left action (add the name)
#         # newenv = EnvMonad(glob)
#         # newenv >> self.left.action
#         # glob = newenv.env
#         # get the name
#         # glob.stackmonad >> Stack.pop()
#         # val1 = glob.stackmonad.out[-1]
#         # glob.table[val1] = self.right
#         if not self.check(glob):
#             return

#         glob.table[self.left.lexeme] = self.right
#         glob.stackmonad >> Stack.push('Assignment')
#         return newenv

#     def check(self, glob):
#         if glob.table.get(self.left.lexeme) is None:
#             return True
#         else:
#             print(f'Redefining Name Error')
#             return False

#     def name(self):
#         return f'Assignment Action, left is {self.left}, right is {self.right}'

# class FunctionCallAction(Action):
#     def __init__(self):
#         pass

#     def run(self):
#         pass
#         # left is an identifier, right is *something*
#         # if f is x -> then make x in theh data table = to the right.

# class ArithmeticAction:
#     def __init__(self):
#         super().__init__()

#     def check(self, checkenv, op1, op2):
#         if isinstance(op1, str):
#             try:
#                 val1 = checkenv.env.table[op1]
#                 checkenv >> val1.action
#                 val1 = checkenv.env.stackmonad.stack.value
#             except:
#                 print(f'Identifier {op2} does not exist in the data table')
#         else:
#             val1 = op1

#         if isinstance(op2, str):
#             try:
#                 val2 = checkenv.env.table[op2]
#                 checkenv >> val2.action
#                 val2 = checkenv.env.stackmonad.stack.value
#             except:
#                 print(f'Identifier {op2} does not exist in the data table')
#         else:
#             val2 = op2

#         return op1, op2


# class AdditionAction(ArithmeticAction):
#     def __init__(self):
#         super().__init__()
#     
#     def run(self, glob):
#         newenv = EnvMonad(glob)
#         newenv >> self.left.action >> self.right.action

#         # Unwrap to stack
#         glob = newenv.env
#         glob.stackmonad >> Stack.pop() >> Stack.pop()
#         op1 = glob.stackmonad.out[-1]
#         op2 = glob.stackmonad.out[-2]

#         # Wrap for checks
#         checkenv = EnvMonad(glob)

#         # check the results
#         val1, val2 = self.check(checkenv, op1, op2)

#         # do the operation
#         ans = val1 + val2
#         glob.stackmonad >> Stack.push(ans)
#         return glob

#     def name(self):
#         return f'Addition Action, left is {self.left}, right is {self.right}'
