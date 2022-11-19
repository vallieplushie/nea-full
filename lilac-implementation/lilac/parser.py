from . import *

class Parser:
    iterpointer = 0

    @staticmethod
    @StatusHandler.checkerror
    @StatusHandler.logging('DEBUG')
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
    @StatusHandler.checkerror
    @StatusHandler.logging('TRACE')
    def clean_expression(expr: list[Token]) -> list[Token]:
        """Cleans an expression before it is parsed and checks for certain conditions."""
        if len(expr) >= 3:
            if expr[0].type is TokenType.LEFT_PAREN and expr[-1].type is TokenType.RIGHT_PAREN:
                expr = expr[1:-1]
        elif len(expr) == 2:
            if expr[0].type in Grammar.unary:
                expr = [Token(None, '', expr[0].line)] + expr
            elif expr[0].type in Grammar.operators:
                StatusHandler.throw(ErrorType.OperatorUseError, expr[0].line,
                            f'Operator {expr[0].lexeme} is missing a left operand.')
            elif expr[1].type in Grammar.operators:
                StatusHandler.throw(ErrorType.OperatorUseError, expr[0].line,
                            f'Operator {expr[1].lexeme} is missing a right operand.')
        return expr

    @staticmethod
    @StatusHandler.checkerror
    @StatusHandler.logging('DEBUG')
    def get_action(token) -> Action:
        match token.type:
            # case TokenType.COLON: return AssignAction()
            case TokenType.PLUS: return AdditionAction()
            case TokenType.MINUS: return SubtractionAction()
            case TokenType.STAR: return MultiplicationAction()
            case TokenType.SLASH: return DivisionAction()
            case TokenType.AND: return AndAction()
            case TokenType.OR: return OrAction()
            case TokenType.COLON: return AssignAction()
            case TokenType.IDENTIFIER: return IdentifierAction(token)
            case _:
                if token.type in Grammar.literal:
                    return LiteralAction(token)
                else:
                    return Action()

    @staticmethod
    @StatusHandler.checkerror
    @StatusHandler.logging('DEBUG')
    def to_tree(expr: list[Token]) -> Tree:
        """Converts a list of tokens into a Tree, which it returns"""
        index = Parser.find_lowest_bound(expr) 
        action = Parser.get_action(expr[index])
        if [i for i in expr if i.type in Grammar.operators]:
            lexp = Parser.clean_expression(expr[:index])
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
    @StatusHandler.logging('INFO')
    def parse(expr):
        if expr[-1].type is TokenType.EOF:
            return Parser.to_tree(Parser.clean_expression(expr[:-2]))
        return Parser.to_tree(expr)
