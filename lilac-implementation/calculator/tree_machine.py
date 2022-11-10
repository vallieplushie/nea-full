from . import *

class TreeMachine:
    def __init__(self, tree=None):
        self.env_monad = EnvMonad()
        self.tree = tree

    def execute(self, tree):
        self.env_monad >> tree.action
        return self.env_monad.env.stackmonad.stack.top.value
        
