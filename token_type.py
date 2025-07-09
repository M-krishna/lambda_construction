from enum import Enum


class TokenType(Enum):
    VARIABLE = "variable"
    LAMBDA = "lambda" # In our program, "fn" is represented as lambda
    DOT = "dot"
    LPAREN = "lparen"
    RPAREN = "rparen"
    VAR = "var"
    IDENTIFIER = "identifier"
    EQUAL = "equal"
    EOF = "eof"