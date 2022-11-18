from . import *

class Parser:
    iterpointer = 0
    
    @staticmethod
    def printlog(func):
        """Decorator used for debugging, prints trace."""
        def wrapper(*args):
            Parser.iterpointer += 1
            print(f'{" "*Parser.iterpointer*4}Doing: {func.__name__}')
            print(f'{" "*(Parser.iterpointer*4+2)}Input: {args}')
            out = func(*args)

            if isinstance(out, list):
                ts = out
                out_str = f'[{[str(t) for t in ts]}]'
                out = ts
            else:
                out_str = out

            print(f'{" "*(Parser.iterpointer*4+2)}Output: {out_str}\n')
            Parser.iterpointer -= 1
            return out
        return wrapper

    @staticmethod
    def checkerror(func):
        """Decorator which checks if there has been an error.

        If there has been an error, it will return out of the function.
        """
        def wrapper(*args):
            if LICONF.HAD_ERROR:
                return
            else:
                out = func(*args)
                return out
        return wrapper

    @staticmethod
    @checkerror
    def find_lowest_bound(expr):
        # returns the index of the operator with the least precedence in the expression
        # skips over any expressions in parentheticals
        in_paren = 0
        min_bind = 20
        min_index = 0 
    
        for i in range(len(expr)):
            # skip parentheses 
            if expr[i].type is TokenType.LEFT_PAREN:
                in_paren += 1
            elif expr[i].type is TokenType.RIGHT_PAREN:
                in_paren -= 1
            else:
                in_paren += 0
    
            if in_paren > 0:
                continue

            if expr[i].type in Grammar.operators:
                rule = Grammar.bindings[expr[i].type]
                if rule['prec'] < min_bind:
                    min_bind = rule['prec']
                    min_index = i
                elif rule['prec'] == min_bind:
                    if rule['assoc'] == 'R':
                        continue
                    elif rule['assoc'] == 'L':
                        min_index = i

        return min_index
    
    @staticmethod
    @checkerror
    def clean_expression(expr: list[Token]) -> list[Token]:
        """Cleans an expression before it is parsed and checks for certain conditions."""
        if len(expr) >= 3:
            if expr[0].type is TokenType.LEFT_PAREN and expr[-1].type is TokenType.RIGHT_PAREN:
                expr = expr[1:-1]
        elif len(expr) == 2:
            if expr[0].type in Grammar.unary:
                expr = [Token(None, '', expr[0].line)] + expr
            elif expr[0].type in Grammar.operators:
                Error.throw(ErrorType.OperatorUseError, expr[0].line,
                            f'Operator {expr[0].lexeme} is missing a left operand.')
            elif expr[1].type in Grammar.operators:
                Error.throw(ErrorType.OperatorUseError, expr[0].line,
                            f'Operator {expr[1].lexeme} is missing a right operand.')
        return expr

    @staticmethod
    @checkerror
    def get_action(token) -> Action:
        match token.type:
            # case TokenType.COLON: return AssignAction()
            case TokenType.PLUS: return AdditionAction()
            
            case _:
                if token.type in Grammar.literal:
                    return LiteralAction(token)
                else:
                    return Action()

    @staticmethod 
    @checkerror
    def to_tree(expr: list[Token]) -> Tree:
        """Converts a list of tokens into a Tree, which it returns"""
        index = Parser.find_lowest_bound(expr) 
        action = Action()# Parser.get_action(expr[index])
        if [i for i in expr if i.type in Grammar.operators]:
            lexp = Parser.clean_expression(expr[:index])
            #print(f'lexp: {lexp}')
            rexp = Parser.clean_expression(expr[index+1:]) 
            ltree = Parser.to_tree(lexp)
            rtree = Parser.to_tree(rexp) 
            # print(Tree(expr[index], action, ltree, rtree)) 
            return Tree(expr[index], action, ltree, rtree)
        else:
            # print(Tree(expr[index], action))
            return Tree(expr[index], action)

    @staticmethod
    #@printlog
    def parse(expr):
        if expr[-1].type is TokenType.EOF:
            return Parser.to_tree(Parser.clean_expression(expr[:-2]))
        return Parser.to_tree(expr)
