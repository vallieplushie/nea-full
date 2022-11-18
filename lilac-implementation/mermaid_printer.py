from . import *

class PrettyPrinter:
    @staticmethod
    def tree_to_mermaid(tree: Tree) -> str:
        output = 'graph TB\n'
        output += PrettyPrinter.mermaid_string(tree)
        return output
        

    @staticmethod
    def mermaid_string(tree: Tree) -> str:
        output = ''
        if not tree.is_leaf():
            output += f'{hash(tree.data)}["{tree.data.lexeme}"] -> {hash(tree.left.data)}["{tree.left.data.lexeme}"]'
            output += f'{hash(tree.data)}["{tree.data.lexeme}"] -> {hash(tree.left.data)}["{tree.left.data.lexeme}"]'
            output += PrettyPrinter.mermaid_string(tree.left)
            output += PrettyPrinter.mermaid_string(tree.right)
        return output

        
