from enum import Enum, auto

class Keys(Enum):
    SYMB = 1
    PREC = 2


class Operators:
    PLUS = {Keys.SYMB: '+', Keys.PREC: 3}
    MINUS = {Keys.SYMB: '-', Keys.PREC: 2}
    STAR = {Keys.SYMB: '*', Keys.PREC: 4}
    SLASH = {Keys.SYMB: '/', Keys.PREC: 5}
    CARET = {Keys.SYMB: '^', Keys.PREC: 6}
    ASSIGN = {Keys.SYMB: ':', Keys.PREC: 1}
    TERMINATOR = {Keys.SYMB: ';', Keys.PREC: 0}
    LPAREN = auto()
    RPAREN = auto()


OPERATORS= {
        ':': 0, 
        ';': 1, 
        '-': 2, 
        '+': 3, 
        '*': 4,
        '/': 5,
        '^': 6,
        }


class Tree:
    def __init__(self, data, action, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        
        self.action = action
        self.action.left = self.left
        self.action.right = self.right

    def __str__(self):
        if self.is_leaf():
            return f'{self.data}'
        return f"({self.data}, left:{self.left}, right:{self.right})"

    def post_order(self):
        string = ''
        if not self.is_leaf():
            string += self.left.post_order()
            string += self.right.post_order()
            string += self.data
        else:
            string = self.data
        return string

    def is_leaf(self):
        return (self.left is None and self.right is None)


class StackMonad:
    def __init__(self, stack=None, out=[]):
        if stack is None:
            self.stack = Stack()
        else:
            self.stack = stack
        self.out = out

    def bind(self, f):
        result, out = f(self.stack)
        if result is None:
            return StackMonad(self.stack)
        else:
            self.out = out
            return StackMonad(result)

    def __rshift__(self, f):
        result, out = f(self.stack)
        if result is None:
            return StackMonad(self.stack)
        elif out is None:
            return StackMonad(result)
        else:
            self.out.append(out)
            return StackMonad(result)


class Node:
    def __init__(self, val=None, n=None):
        self.value = val
        self.next = n


class Stack:
    def __init__(self):
        self.top = Node()

    def __str__(self):
        cur = self.top
        msg = f'top: '
        while cur is not None:
            msg += f'{cur.value}\n     '
            cur = cur.next
        return msg

    @staticmethod
    def push(value):
        def inner_push(stack):
            if stack.top is None:
                stack.top = Node(value)
            else:
                stack.top = Node(value, stack.top)
            return stack, None
        return inner_push

    @staticmethod
    def pop():
        def inner_pop(stack):
            val = stack.top.value
            stack.top = stack.top.next
            return stack, val
        return inner_pop

    @staticmethod
    def Push(value):
        def inner_push(env):
            if env.stackmonad.stack.top is None:
                env.stackmonad.stack.top = Node(value)
            else:
                env.stackmonad.stack.top = Node(value, env.stackmonad.stack.top)
            return env.stackmonad.stack, None

        return inner_push

    # New pop function defined for the
    @staticmethod
    def Pop():
        def inner_pop(env):
            val = env.stackmonad.stack.top.value
            env.stackmonad.stack.top = env.stackmonad.stack.top.next

            if isinstance(val, str):
                try:
                    output = checkenv.env.table[val]
                    checkenv = EnvMonad(env)
                    checkenv >> output.action
                    output = checkenv.env.stackmonad.stack.value
                except:
                    print(f'Identifier {val} does not exist in the data table')
            else:
                output = val
            return env, output
        return inner_pop

class Environment:
    def __init__(self):
        self.stackmonad = StackMonad(Stack())
        self.table = {}

class EnvMonad:
    def __init__(self, env=None):
        if env is None:
            self.env = Environment()
        else:
            self.env = env
        self.trace = []

    def trace(self):
        string = ''
        for s in self.trace:
            string += s
        return string

    def bind(self, action):
        result = action.run(self.env)
        # Add to the trace the action being run
        self.trace.append(action.name())
        return result

    def __rshift__(self, action):
        result = action.run(self.env)
        # Add to the trace the action being run
        self.trace.append(action.name())
        #if result is None:
            #return result
        #else:
            #return EnvMonad(result)
        return result