from . import *

class Action:
    def __init__(self):
        self.left = None
        self.right = None

    def check(self, glob):
        pass

class LiteralAction(Action):
    def __init__(self, val):
        self.val = val
        super().__init__()

    def run(self, glob):
        glob.stackmonad >> Stack.push(self.val)
        return EnvMonad(glob)

    def name(self):
        return f'Literal Action, literal is {self.val}'

class AssignAction(Action):
    def __init__(self):
        super().__init__()

    def run(self, glob):
        newenv = EnvMonad(glob)
        newenv >> self.left.action
        glob = newenv.env
        glob.stackmonad >> Stack.pop()
        val1 = glob.stackmonad.out[-1]
        glob.table[val1] = self.right
        glob.stackmonad >> Stack.push('Assignment')
        return newenv

    def name(self):
        return f'Assignment Action, left is {self.left}, right is {self.right}'

class FunctionCallAction(Action):
    def __init__(self):
        pass

    def run(self):
        pass
        # left is an identifier, right is *something*
        # if f is x -> then make x in theh data table = to the right.

class ArithmeticAction:
    def __init__(self):
        super().__init__()

    def check(self, checkenv, op1, op2):
        if isinstance(op1, str):
            try:
                val1 = checkenv.env.table[op1]
                checkenv >> val1.action
                val1 = checkenv.env.stackmonad.stack.value
            except:
                print(f'Identifier {op2} does not exist in the data table')
        else:
            val1 = op1

        if isinstance(op2, str):
            try:
                val2 = checkenv.env.table[op2]
                checkenv >> val2.action
                val2 = checkenv.env.stackmonad.stack.value
            except:
                print(f'Identifier {op2} does not exist in the data table')
        else:
            val2 = op2

        return op1, op2


class AdditionAction(ArithmeticAction):
    def __init__(self):
        super().__init__()
    
    def run(self, glob):
        newenv = EnvMonad(glob)
        newenv >> self.left.action >> self.right.action

        # Unwrap to stack
        glob = newenv.env
        glob.stackmonad >> Stack.pop() >> Stack.pop()
        op1 = glob.stackmonad.out[-1]
        op2 = glob.stackmonad.out[-2]

        # Wrap for checks
        checkenv = EnvMonad(glob)

        # check the results
        val1, val2 = self.check(checkenv, op1, op2)

        # do the operation
        ans = val1 + val2
        glob.stackmonad >> Stack.push(ans)
        return glob

    def name(self):
        return f'Addition Action, left is {self.left}, right is {self.right}'