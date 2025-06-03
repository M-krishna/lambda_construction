import unittest
from typing import List
from token_internal import Token
from ast_internal import Expression, VariableNode
from lexer import Lexer
from parser import Parser
from beta_reduction import Evaluator
from church_encoding import ChurchNumeral


class TestChurchNumeral(unittest.TestCase):
    def test_non_numeral(self):
        source = "x" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, None)

    def test_non_church_numeral_1(self):
        source = "fn x.x" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, None)

    def test_non_church_numeral_2(self):
        source = "(x y)" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, None)
    
    def test_non_church_numeral_3(self):
        source = "fn f. fn x. fn y. z" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, None)

    def test_church_numeral_zero(self):
        source = "fn f. fn x. x" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, 0)
    
    def test_church_numeral_one(self):
        source = "fn f. fn x. f(x)" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, 1)

    def test_church_numeral_two(self):
        source = "fn f. fn x. f(f(x))" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, 2)

    def test_church_numeral_three(self):
        source = "fn f. fn x. f(f(f(x)))" # variable node

        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        result: VariableNode = evaluator.beta_reduce(parser.get_ast()[0])

        church_numeral = ChurchNumeral().decode_church_numeral(evaluator.beta_reduce(result))
        self.assertEqual(church_numeral, 3)
    

if __name__ == "__main__":
    unittest.main()