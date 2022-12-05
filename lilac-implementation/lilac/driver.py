from . import * 
from sys import exit

class Lilac: 
    tree_m = TreeMachine()
    
    @staticmethod
    def start_prompt():
        open(LICONF.LOG_PATH, 'w').close()
        LICONF.INTERACTIVE_MODE = True
        print(f'{"- "*6}-| Lilac Interactive |-{" -"*6}')
        print(f'  Type $[q]uit to quit and $[h]elp to get help.\n')
        Lilac.run_prompt()
    

    @staticmethod
    def run_prompt():
        """Runs an interactive prompt"""  
        user_in:str = ''
        while True:
            Lilac.tree_m.empty_stack()
            user_in = input(f'<i> ')

            if user_in[0] == '$':
                Lilac.do_interactive_command(user_in[1:])
                Lilac.run_prompt()

            scanner = Scanner(user_in)
            tokens = scanner.scan()

            if LICONF.HAD_ERROR:
                LICONF.HAD_ERROR = False
                Lilac.run_prompt()

            tokens_string = [f'{t.type}, {t.lexeme}' for t in scanner.scan()]
            # print(tokens)
            print(f'Tokens: {tokens_string}')
            tree = Parser.parse(tokens)

            if LICONF.HAD_ERROR:
                LICONF.HAD_ERROR = False
                Lilac.run_prompt()

            print(f'Tree: {tree.in_order()}\n')
            out = Lilac.tree_m.execute(tree)
            # print(PrettyPrinter.tree_to_mermaid(tree))
            # out = Lilac.tree_m.execute(tree) 
            if out != '':
                print(f'<o> {out}')
    
    @staticmethod
    def do_interactive_command(command: str) -> None:
        command_args = command.split()
        cmd = command_args[0]
        args = command_args[1:]
        match cmd:
            case 'q' | 'quit': 
                print('Leaving Lilac...')
                exit(0)
            case 'h' | 'help': Lilac.print_help(args)
            case 'i' | 'info': Lilac.print_info(args)
    
    @staticmethod
    def print_help(args: list[str]) -> None:
        if not args:
            print(f'Lilac language repl cool :D')
        else:
            match args[0]:
                case 'author':
                    print(f'Lilac was built and designed by Valérie Thibault.')
                case 'help':
                    print(f'Real smart, nice one...')
                    print(f'You can use the help command followed by any other command to learn about its usage.')
                case 'info':
                    print(f'Use info with any operator to see informtion about it.')
                case 'quit':
                    print(f'Use this to quit the interactive mode.')
                case _:
                    print(f'Lilac language repl cool :D')
    
    @staticmethod
    def print_info(args: list[str]) -> None:
        if args is []:
            print(f'Well, what do you need info about?')
        else:
            rule = Grammar.bindings.get(args[0])
            if rule is None:
                print(f'Not an operator')
            else:
                print(f'({args[0]}) has a precedence of {rule["prec"]} and is associative in the {rule["assoc"]} direction.')


