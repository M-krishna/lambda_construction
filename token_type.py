from enum import Enum


class TokenType(Enum):
    VARIABLE = "variable"
    LAMBDA = "lambda" # In our program, "fn" is represented as lambda
    DOT = "dot"
    LPAREN = "lparen"
    RPAREN = "rparen"
    EOF = "eof"