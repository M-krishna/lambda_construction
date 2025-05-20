import unittest
from typing import List
from token_internal import Token
from token_type import TokenType
from lexer import Lexer
from parser import Parser
from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode
from beta_reduction_v2 import Evaluator


class TestBetaReductionV2(unittest.TestCase):
    
    @unittest.skip
    def test_variable_node(self):
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

    @unittest.skip
    def test_lambda_abstraction(self):
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

    @unittest.skip
    def test_lambda_application(self):
        source = "(x y)"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result: LambdaApplicationNode = evaluator.beta_reduce(ast[0])

        self.assertEqual(result.left, VariableNode("x"))
        self.assertEqual(result.right, VariableNode("y"))

    @unittest.skip
    def test_apply_lambda_abstraction_1(self):
        source = "(fn x.x) y"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result: Expression = evaluator.beta_reduce(ast[0])

        self.assertEqual(result, VariableNode("y"))

    @unittest.skip
    def test_apply_lambda_abstraction_2(self):
        source = "(fn x. x) (fn y. y)"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result: LambdaAbstractionNode = evaluator.beta_reduce(ast[0])

        self.assertIsInstance(result, LambdaAbstractionNode)
        self.assertEqual(result.param, "y")
        self.assertEqual(result.body, VariableNode("y"))
        self.assertIsInstance(result.body, VariableNode)

    def test_apply_lambda_abstraction_3(self):
        # source = "(fn x. fn y. x y) y"
        source = "(fn xy. x y) y"

        lexer = Lexer(source)
        lexer.tokenize()
        tokens: List[Token] = lexer.get_tokens()

        parser = Parser(tokens)
        parser.parse()
        ast: List[Expression] = parser.get_ast()

        evaluator = Evaluator()
        result: Expression = evaluator.beta_reduce(ast[0])
        print(f"result: {result}")

if __name__ == "__main__":
    unittest.main()