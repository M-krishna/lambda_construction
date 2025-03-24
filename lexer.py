from token_type import TokenType
from token_internal import Token
from typing import List, Dict, Callable

class Lexer:
    def __init__(self, source: str):
        self.source: str = source
        self.tokens: List[Token] = []
        self.start_position: int = 0
        self.current_position: int = 0
        self.line: int = 1
        self.column: int = 1
    
    def tokenize(self) -> List[Token]:
        while not self.is_at_end():
            self.start_position = self.current_position
            self.scan_tokens()

    def scan_tokens(self) -> None:
        c: str = self.advance()

        symbols: Dict[str, Callable] = {
            "(": lambda: self.add_token(TokenType.LPAREN.name),
            ")": lambda: self.add_token(TokenType.RPAREN.name),
            ".": lambda: self.add_token(TokenType.DOT.name),
            ";": lambda: self.skip_comments()
        }

        fn: Callable = symbols.get(c, lambda: self.default_case(c))
        try:
            fn()
        except Exception as e:
            raise SyntaxError(f"something went wrong during scanning: {e}")
    
    def skip_comments(self):
        while self.peek() != "\n" and not self.is_at_end():
            self.advance()
    
    def default_case(self, c):
        if self.is_whitespace(c):
            if c == "\n":
                self.line += 1
                self.column = 1
        elif self.is_alpha(c):
            self.scan_identifier(c)
        else:
            raise SyntaxError(f"Unknown character: {c}")
    
    def scan_identifier(self, current_chr: str):
        if current_chr == "f" and self.peek() == "n" and self.peek_next() == " ":
            self.advance() # consume "n" character
            self.add_token(TokenType.LAMBDA.name)
        else:
            self.add_token(TokenType.VARIABLE.name)


    def add_token(self, token_type: TokenType) -> None:
        lexeme: str = self.source[self.start_position:self.current_position]
        self.tokens.append(Token(token_type, lexeme, self.line, self.column - len(lexeme)))

    ########################## HELPER FUNCTIONS #######################
    def is_alpha(self, c: str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' or c <= 'Z')

    def is_whitespace(self, c: str) -> bool:
        SPACE: str = " "
        NEWLINE: str = "\n"
        TABSPACE: str = "\t"
        return c in [SPACE, NEWLINE, TABSPACE]

    def advance(self) -> str:
        current: str = self.source[self.current_position]
        self.current_position += 1
        self.column += 1
        return current

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current_position]
    
    def peek_next(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current_position + 1]

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.source)

    def get_tokens(self) -> List[Token]:
        return self.tokens 
    ########################## END OF HELPER FUNCTIONS ################