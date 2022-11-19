from . import *

class TreeMachine:
    def __init__(self, tree=None):
        self.env_monad = EnvMonad()
        self.tree = tree
    
    @StatusHandler.logging('INFO')
    def execute(self, tree):
        self.env_monad >> tree.action
        # print(self.env_monad.trace)
        top = self.env_monad.env.stackmonad.stack.top.value
        if top.literal is not None:
            return top.literal
        else:
            return ''

    def empty_stack(self):
        self.env_monad.env.stackmonad = StackMonad()

        
