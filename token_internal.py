from token_type import TokenType
from dataclasses import dataclass

@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    line: int = 0
    column: int = 0

    def __str__(self):
        return f""
    
    def __repr__(self):
        return f"Token({self.token_type}, {self.lexeme})"