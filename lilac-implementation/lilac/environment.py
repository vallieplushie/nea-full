from . import *

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

    def consume(self, scope: Environment):
        """
        'Consumes' an environment, merging it with the current one.
        The stack of the second is pushed to the top, and the datatables are merged scope ont env.
        """
        newenv = Environment()
        newenv.stack_monad = StackMonad(Stack(Stack.join(scope.stack_monad.stack, self.env.stack_monad.stack)))
        newenv.table = self.env.table | scope.table
        return EnvMonad(newenv)
        # self.env.stack_monad = StackMonad(Stack(Stack.join(scope.stack_monad.stack, self.env.stack_monad.stack)))
        # self.env.table = self.env.table | scope.table

    @StatusHandler.logging('INFO')
    def bind(self, action):
        result = action.run(self.env)
        # Add to the trace the action being run
        self.trace.append(action.name())
        return result

    @StatusHandler.logging('INFO')
    def __rshift__(self, action):
        result = action.run(self.env)
        # Add to the trace the action being run
        self.trace.append(action.name())
        #if result is None:
            #return result
        #else:
            #return EnvMonad(result)
        return result
