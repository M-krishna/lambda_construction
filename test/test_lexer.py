import unittest
from typing import List
from lexer import Lexer
from token_internal import Token
from token_type import TokenType

class TestLexer(unittest.TestCase):
    def test_comment(self):
        source = "; variable"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens = lexer.get_tokens()

        self.assertEqual(tokens, [])

    def test_variable(self):
        source = "a"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        self.assertEqual(tokens[0].token_type, TokenType.VARIABLE.name)
        self.assertEqual(tokens[0].lexeme, "a")

    def test_abstraction(self):
        source = "fn x.x"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        expected_tokens: List[Token] = [
            Token(TokenType.LAMBDA, "fn"),
            Token(TokenType.VARIABLE, "x"),
            Token(TokenType.DOT, "."),
            Token(TokenType.VARIABLE, "x")
        ]

        for index, token in enumerate(tokens):
            with self.subTest(index):
                self.assertEqual(expected_tokens[index].token_type.name, token.token_type)
                self.assertEqual(expected_tokens[index].lexeme, token.lexeme)
    
    def test_application_1(self):
        source = "(x y)"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.VARIABLE, "x"),
            Token(TokenType.VARIABLE, "y"),
            Token(TokenType.RPAREN, ")")
        ]

        for index, token in enumerate(tokens):
            with self.subTest(index):
                self.assertEqual(expected_tokens[index].token_type.name, token.token_type)
                self.assertEqual(expected_tokens[index].lexeme, token.lexeme)

    def test_application_2(self):
        source = "(fn x.x) y"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.LAMBDA, "fn"),
            Token(TokenType.VARIABLE, "x"),
            Token(TokenType.DOT, "."),
            Token(TokenType.VARIABLE, "x"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.VARIABLE, "y")
        ]

        for index, token in enumerate(tokens):
            with self.subTest(index):
                self.assertEqual(expected_tokens[index].token_type.name, token.token_type)
                self.assertEqual(expected_tokens[index].lexeme, token.lexeme)

    def test_application_3(self):
        source = "(fn x.x) (fn y.y)"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, "("),
            Token(TokenType.LAMBDA, "fn"),
            Token(TokenType.VARIABLE, "x"),
            Token(TokenType.DOT, "."),
            Token(TokenType.VARIABLE, "x"),
            Token(TokenType.RPAREN, ")"),
            Token(TokenType.LPAREN, "("),
            Token(TokenType.LAMBDA, "fn"),
            Token(TokenType.VARIABLE, "y"),
            Token(TokenType.DOT, "."),
            Token(TokenType.VARIABLE, "y"),
            Token(TokenType.RPAREN, ")")
        ]

        for index, token in enumerate(tokens):
            with self.subTest(index):
                self.assertEqual(expected_tokens[index].token_type.name, token.token_type)
                self.assertEqual(expected_tokens[index].lexeme, token.lexeme)

if __name__ == "__main__":
    unittest.main()