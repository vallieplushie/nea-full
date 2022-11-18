from . import TokenType

class Grammar:
    reserved_ids = {
            # 'fn'
            # 'let'
            'in' : TokenType.IN,
            'true' : TokenType.TRUE,
            'false' : TokenType.FALSE
            } 
    # operators = [
    #         TokenType.PLUS,
    #         TokenType.MINUS,
    #         TokenType.STAR,
    #         TokenType.SLASH,
    #         TokenType.COLON,
    #         TokenType.SPACE,
    #         TokenType.SEMI_COLON,
    #         TokenType.PIPE,
    #         TokenType.QUESTION,
    #         ]
    parens = [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN] 
    bindings = {
            TokenType.COLON: { 'prec': 0, 'assoc': 'R' },
            TokenType.SPACE: {'prec': 10, 'assoc': 'L'},
            TokenType.ARROW: {'prec': 1, 'assoc': 'R'},
            TokenType.PIPE: {'prec': 2, 'assoc': 'L'},
            TokenType.QUESTION: {'prec': 2, 'assoc': 'R'},
            TokenType.SEMI_COLON: {'prec': 3, 'assoc': 'R'},
            TokenType.SLASH: {'prec': 8, 'assoc': 'R'},
            TokenType.STAR: {'prec': 8, 'assoc': 'R'},
            TokenType.PLUS: {'prec': 7, 'assoc': 'R'}, 
            TokenType.MINUS: {'prec': 7, 'assoc': 'R'},
            TokenType.EQUAL: {'prec': 6, 'assoc': 'R'},
            TokenType.LESS: {'prec': 6, 'assoc': 'R'},
            TokenType.GREATER: {'prec': 6, 'assoc': 'R'},
            TokenType.LESS_EQUAL: {'prec': 6, 'assoc': 'R'},
            TokenType.GREATER_EQUAL: {'prec': 6, 'assoc': 'R'},
            TokenType.OR: {'prec': 5, 'assoc': 'R'},
            TokenType.AND: {'prec': 4, 'assoc': 'R'},
            }
    operators = bindings.keys()
    unary = [TokenType.NOT, TokenType.MINUS]
    literal = [TokenType.NUMBER, TokenType.STRING, TokenType.IDENTIFIER]
