from . import *

class Grammar:
    # set of symbols that are allowed, and a dict containing bidmas
    operators = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.COLON
            ]
    parens = [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN] 
    bindings = {
            TokenType.COLON: { 'prec': 0, 'assoc': 'R' },
            TokenType.SLASH: {'prec': 3, 'assoc': 'R'},
            TokenType.STAR: {'prec': 3, 'assoc': 'R'},
            TokenType.PLUS: {'prec': 2, 'assoc': 'R'}, 
            TokenType.MINUS: {'prec': 2, 'assoc': 'R'}
            }
    literal = [TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER]

class Parser:
    @staticmethod
    def find_lowest_bound(expr):
        # returns the index of the operator with the least precedence in the expression
        # skips over any expressions in parentheticals
        in_paren = 0
        min_bind = 10
        min_index = -1
    
        for i in range(len(expr)):
            # ignore expressions in parentheses
            if expr[i].type is TokenType.LEFT_PAREN:
                in_paren += 1
            if expr[i-1].type is TokenType.RIGHT_PAREN:
                in_paren -= 1
    
            if in_paren != 0:
                continue
            elif expr[i].type in Grammar.operators:
                rule = Grammar.bindings[expr[i].type]

                if rule['prec'] < min_bind:
                    min_bind = rule['prec']
                    min_index = i
                elif rule['prec'] == min_bind:
                    if rule['assoc'] == 'L':
                        min_index = i

        return min_index
    
    @staticmethod 
    def clean_outer_parens(expr):
        # removes any brackets around an expression before it is read
        if expr[0].type is TokenType.LEFT_PAREN and expr[-1].type is TokenType.RIGHT_PAREN:
            expr = expr[1:-1]
        return expr

    @staticmethod
    def get_action(token) -> Action:
        match token.type:
            case TokenType.COLON: return AssignAction()
            case TokenType.PLUS: return AdditionAction()
            case _:
                if token.type in Grammar.literal:
                    return LiteralAction(token)
                else:
                    return Action()

    @staticmethod 
    def to_tree(expr: list[Token]) -> Tree:
        # recursively converts the expression to a binary tree
        index = Parser.find_lowest_bound(expr)
        action = Parser.get_action(expr[index])
        # True if the list is not empty, if there are operators left
        if [i for i in expr if i.type in Grammar.operators]:
            lexp = Parser.clean_outer_parens(expr[:index])
            rexp = Parser.clean_outer_parens(expr[index+1:])
            ltree = Parser.to_tree(lexp)
            rtree = Parser.to_tree(rexp)
    
            return Tree(expr[index], action, ltree, rtree)
        else:
            return Tree(expr[index], action)

    @staticmethod
    def parse(expr):
        return Parser.to_tree(expr)
    
    def convert_to_rpn(expr):
        # turns the binary tree into an rpn string
        return Parser.parse(expr).post_order()
