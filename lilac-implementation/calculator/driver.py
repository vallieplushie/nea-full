from . import *

class Lilac:
    interactive = True 
    tree_m = TreeMachine()

    @staticmethod
    def run_prompt():
        """Runs an interactive prompt""" 
        Lilac.interactive = True
        user_in:str = ''
        while True:
            user_in = input(f'<i> ')

            if user_in == 'quit':
                exit(0)
            
            scanner = Scanner(user_in)
            tokens = scanner.scan()
            tokens_string = [f'{t.type}, {t.lexeme}' for t in scanner.scan()]
            # print(tokens)
            tree = Parser.to_tree(tokens)
            out = f'Tokens: {tokens_string}\n  > Tree: {tree}'
            # out = Lilac.tree_m.execute(tree)
            print(f'<o> {out}')

