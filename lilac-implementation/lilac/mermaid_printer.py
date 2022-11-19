from . import *

class PrettyPrinter:
    @staticmethod
    def tree_to_mermaid(tree) -> str:
        output = 'graph TB\n'
        output += PrettyPrinter.mermaid_string(tree)
        return output
        

    @staticmethod
    def mermaid_string(tree) -> str:
        output = ''
        if not tree.is_leaf():
            output += f'{hash(tree.data)}["{tree.data.lexeme}"] --> {hash(tree.right.data)}["{tree.right.data.lexeme}"]\n'
            output += f'{hash(tree.data)}["{tree.data.lexeme}"] --> {hash(tree.left.data)}["{tree.left.data.lexeme}"]\n'
            output += PrettyPrinter.mermaid_string(tree.left)
            output += PrettyPrinter.mermaid_string(tree.right)
        return output
    
    @staticmethod
    def print_args(*args) -> str:
        output = ''
        for a in args:
            if isinstance(a, list):
                output += f'\t{[str(b) for b in a]}\n'
            else:
                output += f'\t{a}\n'
        return output

        
