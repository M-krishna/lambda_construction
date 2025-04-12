import unittest
from typing import List
from token_internal import Token
from token_type import TokenType
from lexer import Lexer
from parser import Parser
from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode


class TestParser(unittest.TestCase):

    def test_variable_parser(self):
        source = "x"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        self.assertIsInstance(ast[0], VariableNode)
        self.assertEqual(ast[0].value, "x")

    def test_abstraction_parser(self):
        source = "fn x.x"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        self.assertIsInstance(ast[0], LambdaAbstractionNode)
        self.assertEqual(ast[0].param, "x")
        self.assertIsInstance(ast[0].body, VariableNode)
        self.assertEqual(ast[0].body.value, "x")

    def test_application_1(self):
        source = "(x y)"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        self.assertIsInstance(ast[0], LambdaApplicationNode)
        self.assertIsInstance(ast[0].left, VariableNode)
        self.assertIsInstance(ast[0].right, VariableNode)
        self.assertEqual(ast[0].left.value, "x")
        self.assertEqual(ast[0].right.value, "y")

    def test_application_2(self):
        source = "(fn x.x) y"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        self.assertIsInstance(ast[0], LambdaApplicationNode)
        self.assertIsInstance(ast[0].left, LambdaAbstractionNode)
        self.assertIsInstance(ast[0].right, VariableNode)
        self.assertEqual(ast[0].left.param, "x")
        self.assertIsInstance(ast[0].left.body, VariableNode)
        self.assertEqual(ast[0].left.body.value, "x")
        self.assertEqual(ast[0].right.value, "y")

    def test_application_3(self):
        source = "(fn x.x) (fn y.y)"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        self.assertIsInstance(ast[0], LambdaApplicationNode)
        self.assertIsInstance(ast[0].left, LambdaAbstractionNode)
        self.assertIsInstance(ast[0].right, LambdaAbstractionNode)
        self.assertEqual(ast[0].left.param, "x")
        self.assertEqual(ast[0].right.param, "y")
        self.assertIsInstance(ast[0].left.body, VariableNode)
        self.assertIsInstance(ast[0].right.body, VariableNode)
        self.assertEqual(ast[0].left.body.value, "x")
        self.assertEqual(ast[0].right.body.value, "y")


if __name__ == "__main__":
    unittest.main()