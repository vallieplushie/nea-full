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

class Environment:
    def __init__(self):
        self.stack = Stack()
        self.output = []
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
        # if result is None:
        #     return result
        # else:
        #     return EnvMonad(result)
        return result

class Push:
    def __init__(self, value):
        self.value = value

    def run(self, glob):
        if glob.stack.top is None:
            glob.stack.top = Node(self.value)
        else:
            glob.stack.top = Node(self.value, glob.stack.top)
        return glob

class Pop:
    def __init__(self):
        pass
    def run(self, glob):
        literal = glob.stack.top.value

        # If popping an identifier, return its value in the table
        if isinstance(literal, str):
            try:
                val = glob.table[literal]
                checkenv = EnvMonad(glob)
                checkenv >> val.action
                val = checkenv.env.stack.value
                glob = checkenv.env
            except:
                print(f'Identifier {literal} does not exist in the data table')
        else:
            val = literal

        glob.stack.top = glob.stack.top.next
        glob.output.append(val)
        return glob