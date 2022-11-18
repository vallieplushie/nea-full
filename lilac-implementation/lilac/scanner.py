from . import * 

class Scanner:
    """
    Scans the source code
    """
    
    # for printing the log
    # iterpointer = 0

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Tokens] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1

    def print_log(func):
        def wrapper(self, *args):
            Scanner.iterpointer += 1
            print(f'{" "*Scanner.iterpointer*4}Doing: {func.__name__}')
            print(f'{" "*(Scanner.iterpointer*4+2)}Input: {args}')
            out = func(self, *args)
            print(f'{" "*(Scanner.iterpointer*4+2)}Output: {out}\n')
            Scanner.iterpointer -= 1
            return out
        return wrapper
    
    # @printlog
    def scan(self) -> list[Token]: 
        while not self.at_end():
            # new token starts where the last one ended 
            self.start = self.current
            self.scan_token()
            if LICONF.HAD_ERROR: 
                return []

        # remove non-essential whitespace
        self.tokens += [Token(TokenType.EOF, '', self.line, '')]
        self.clean_tokens()
        return self.tokens
    
    # @printlog
    def scan_token(self) -> None:
        """Scans a single token by consuming it and checking against combinations"""
        character = self.advance()
        # checks which token the current character is
        match character:
            # single character tokens
            case ':': self.add_token(TokenType.COLON)
            case ';': self.add_token(TokenType.SEMI_COLON)
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '+': self.add_token(TokenType.PLUS)
            case '*': self.add_token(TokenType.STAR)
            case '/': self.add_token(TokenType.SLASH)
            case '%': self.add_token(TokenType.MOD)
            case '?': self.add_token(TokenType.QUESTION)
            case '=': self.add_token(TokenType.EQUAL)
            
            # multi character tokens
            case '-':
                if self.match('>'):
                    self.add_token(TokenType.ARROW)
                else:
                    self.add_token(TokenType.MINUS)
            case '|':
                if self.match('-'):
                    self.add_comment()
                elif self.match('|'):
                    self.add_token(TokenType.OR)
                else:
                    self.add_token(TokenType.PIPE)

            case '&':
                if self.match('&'):
                    self.add_token(TextType.AND)
                else:
                    Error.throw(ErrorType.SyntaxError, self.line, 
                                f'Unexpected character {character}')

            case '<':
                if self.match('='):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)

            case '>':
                if self.match('='):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)

            case '!':
                if self.match('='):
                    self.add_token(TokenType.NOT_EQUAL)
                else:
                    self.add_token(TokenType.NOT)
            
            # white space
            case ' ': self.add_token(TokenType.SPACE)
            case '\t': pass
            case '\r': pass
            case '\n': 
                self.add_token(TokenType.NEW_LINE)
                self.line +=1
            
            # strings
            case '"':
                self.add_string()

            case _:
                if character.isnumeric(): 
                    self.add_number()
                elif character.isalpha():
                    self.add_identifier()
                else:
                    Error.throw(ErrorType.SyntaxError, self.line, 
                                f'Unexpected character {character}')
                    return

    def clean_tokens(self):
        """Removes unecessary white space and new lines"""
        t = 0
        paren_count = 0
        function_call = False
        while self.tokens[t+1].type is not TokenType.EOF:
            t += 1
            if self.tokens[t].type is TokenType.SEMI_COLON:
                function_call = True

            if self.tokens[t].type is TokenType.SPACE:
                if t == 0:
                    continue
                elif self.tokens[t-1].type is TokenType.IDENTIFIER\
                        and self.tokens[t+1].type in Grammar.literal + Grammar.parens:
                    function_call = True
                    continue
                elif function_call\
                        and self.tokens[t-1].type in Grammar.literal + Grammar.parens\
                        and self.tokens[t+1].type in Grammar.literal + Grammar.parens:
                    continue
                else:
                    del self.tokens[t]
            
            if self.tokens[t].type is TokenType.LEFT_PAREN:
                paren_count += 1
            elif self.tokens[t].type is TokenType.RIGHT_PAREN:
                paren_count -= 1
            
            if self.tokens[t].type is TokenType.NEW_LINE:
                function_call = False
                if paren_count == 0:
                    continue
                else:
                    del self.tokens[t]

    # @printlog
    def at_end(self) -> bool:
        """Checks if we are at the end of the source code"""
        if self.current >= len(self.source): 
            return True 
        else:
            return False 

    # @printlog
    def advance(self) -> str:
        """Consumes a character in the string and advances"""
        c = self.source[self.current]
        self.current += 1
        return c

    # @printlog
    def add_token(self, type: TokenType, literal=None) -> None:
        """Adds a token to the list"""
        if type is TokenType.EOF:
            lexeme = ""
        else:
            lexeme = self.source[self.start:self.current]

        self.tokens.append(Token(type, lexeme, self.line, literal))

    # @printlog
    def match(self, character) -> bool:
        """Looks ahead at the next character and consumes it"""
        next = self.peek()
        if next == character:
           self.advance()
           return True
        return False

    # @printlog
    def peek(self) -> str:
        """looks at the next character without consuming it"""
        if self.at_end():
            return ''
        return self.source[self.current]

    def add_comment(self) -> None:
        while True:
            character = self.advance()
            if (character == '-' and self.match('|')) or self.at_end():
                return
            else:
                continue

    def add_string(self) -> None:
        """Adds a string literal, continues advancing until the string stops"""
        while self.peek() != '"' and not self.at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.at_end():
            Lilac.error(ErrorType.SyntaxError, self.line,
                        'Unterminated string, did you forget a \'"\'?')
            return

        self.advance()

        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    # @printlog
    def add_number(self) -> None:
        """Adds a number"""
        is_float = 0
        # in a number the next character is either a number or a period 
        while self.peek().isnumeric() or self.peek() == '.':
            if self.peek() == '.':
                is_float += 1
            if is_float > 1:
                Lilac.error(ErrorType.SyntaxError, self.line, 
                            'Incorrect number format, too many periods.')
                return
            else:
                self.advance()

        # string representing the number
        lexeme = self.source[self.start:self.current]
        # store as int or float depending on the type
        if is_float == 0:
            self.add_token(TokenType.NUMBER, float(lexeme))
        else:
            self.add_token(TokenType.NUMBER, int(lexeme))

    def is_id_char(self, character) -> bool:
        if character.isalpha() or character.isnumeric() or character == '_':
            return True
        return False


    def add_identifier(self) -> None:
        """Adds an identifier token"""
        while self.is_id_char(self.peek()):
            self.advance()
        
        lexeme = self.source[self.start:self.current]
        if lexeme == 'true':
            self.add_token(TokenType.TRUE)
        elif lexeme == 'false':
            self.add_token(TokenType.FALSE)
        self.add_token(TokenType.IDENTIFIER)


