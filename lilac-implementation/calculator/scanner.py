from . import * 

# from .driver import Lilac

class Scanner:
    """
    Scans the source code
    """

    def __init__(self, source: str) -> None:
        self.source: str = source
        self.tokens: list[Tokens] = []
        self.start: int = 0
        self.current: int = -1
        self.line: int = 1

    def scan(self) -> list[Token]:
        """Scanning management class"""
        print(self.source)
        while not self.at_end():
            # new token starts where the last one ended  
            self.scan_token()
            self.start = self.current

        self.add_token(TokenType.EOF, "")
        # remove non-essential whitespace
        # self.clean_tokens()
        return self.tokens

    def scan_token(self) -> None:
        character = self.advance()
        print(character)

        # checks which token the current character is
        match character:
            case ':': self.add_token(TokenType.COLON)
            case '(': self.add_token(TokenType.LEFT_PAREN)
            case ')': self.add_token(TokenType.RIGHT_PAREN)
            case '+': self.add_token(TokenType.PLUS)
            case '*': self.add_token(TokenType.STAR)
            case '/': self.add_token(TokenType.DIV)
            case '%': self.add_token(TokenType.MOD)
            case '|': self.add_token(TokenType.PIPE)
            case '?': self.add_token(TokenType.QUESTION)

            case '-':
                if self.match('>'):
                    self.add_token(TokenType.ARROW)
                else:
                    self.add_token(TokenType.MINUS)
            
            # White space
            case ' ': self.add_token(TokenType.SPACE)
            case '\t': pass
            case '\r': pass
            case '\n': 
                self.add_token(TokenType.NEW_LINE)
                self.line +=1

            case '"':
                self.add_string()

            case _:
                if character.isnumeric():
                    self.add_number()
                elif character.isalpha():
                    self.add_identifier()
                else:
                    Lilac.error(ErrorType.SyntaxError, self.line, 
                                f'Unexpected character {character}')
                    return


    def at_end(self) -> bool:
        """Checks if we are at the end of the source code"""
        if self.current+1 >= len(self.source):
            return True
        else:
            return False


    def advance(self) -> str:
        """Consumes a character in the string and advances"""
        c = self.source[self.current]
        self.current += 1
        return c


    def add_token(self, type: TokenType, literal=None) -> None:
        """Adds a token to the list"""
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(type, lexeme, self.line, literal))


    def match(self, character) -> bool:
        """Looks ahead at the next character and consumes it"""
        next = self.peek()
        if next == character:
           self.advance()
           return True
        return False

    def peek(self) -> str:
        """looks at the next character without consuming it"""
        if self.at_end():
            return ''
        return self.source[self.current + 1]


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


    def add_number(self) -> None:
        """Adds a number"""
        is_float = 0
        while self.peek().isnumeric() or self.peek() == '.':
            if self.peek() == '.':
                is_float += 1
            if is_float > 1:
                Lilac.error(ErrorType.SyntaxError, self.line, 
                            'Incorrect number format, too many periods.')
                return
            else:
                self.advance() 

        value = self.source[self.start:self.current]
        if is_float == 0:
            self.add_token(TokenType.NUMBER, float(value))
        else:
            self.add_token(TokenType.NUMBER, int(value))

    def is_id_char(self, character) -> bool:
        if character.isalpha() or character.isnumeric() or character == '_':
            return True
        return False


    def add_identifier(self) -> None:
        """Adds an identifier token"""
        while self.is_id_char(self.peek()):
            self.advance()
        
        self.add_token(TokenType.IDENTIFIER)


