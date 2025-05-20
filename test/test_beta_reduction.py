import unittest
from typing import List
from token_internal import Token
from token_type import TokenType
from lexer import Lexer
from parser import Parser
from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode
from beta_reduction import Evaluator

class TestBetaReduction(unittest.TestCase):

    def test_beta_reduce_variable(self):
        source = "x"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(ast[0])

        self.assertIsInstance(result, VariableNode)
        self.assertEqual(result, VariableNode("x")) # can't reduce a variable node further

    def test_beta_reduce_abstraction(self):
        source = "fn x.x"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result: LambdaAbstractionNode = evaluator.beta_reduce(ast[0])

        # Returns the expression as it since reducing the body (x) doesn't do anything because its a VariableNode
        self.assertIsInstance(result, LambdaAbstractionNode)
        self.assertEqual(result.param, "x")
        self.assertIsInstance(result.body, VariableNode)
        self.assertEqual(result.body.value, "x")

    def test_beta_reduce_application_1(self):
        source = "(fn x.x) y" # Identity function

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result = evaluator.beta_reduce(ast[0]) # should return VariableNode(y)

        self.assertIsInstance(result, VariableNode)
        self.assertEqual(result.value, "y")

    def test_beta_reduce_application_2(self):
        source = "(fn x.x) (fn y.y)"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result = evaluator.beta_reduce(ast[0]) # it should return (fn y.y) because it gets replaced for 'x' in the first lambda
    
        self.assertIsInstance(result, LambdaAbstractionNode)
        self.assertEqual(result.param, "y")
        self.assertIsInstance(result.body, VariableNode)
        self.assertEqual(result.body.value, "y")

    def test_beta_reduce_application_3(self):
        source = "(fn x. x x) y" # Self application

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result = evaluator.beta_reduce(ast[0]) # should return an Application node (y y)

        self.assertIsInstance(result, LambdaApplicationNode)
        self.assertIsInstance(result.left, VariableNode)
        self.assertIsInstance(result.right, VariableNode)
        self.assertEqual(result.left.value, "y")
        self.assertEqual(result.right.value, "y")

    def test_beta_reduce_application_4(self):
        source = "(fn x. (fn y. x)) y"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result = evaluator.beta_reduce(ast[0])
        print(result)

if __name__ == "__main__":
    unittest.main()