import unittest
from main import Lexer, Parser, AlphaConversion, VariableNode, LambdaAbstractionNode, LambdaApplicationNode

class TestAlphaConversion(unittest.TestCase):
    def test_expr1(self):
        expr: str = "fn x.x"

        lexer = Lexer(source=expr)
        lexer.tokenize()

        parser = Parser(tokens=lexer.get_tokens())
        parser.parse()

        alpha_conversion: LambdaAbstractionNode = AlphaConversion().alpha_convert(parser.get_ast()[0], "x", "y")

        self.assertEqual(alpha_conversion.param, "y")
        self.assertEqual(alpha_conversion.body, VariableNode("y"))


    def test_expr2(self):
        expr: str = "fn xy.(x y)" # renaming in nested expressions

        lexer = Lexer(source=expr)
        lexer.tokenize()

        parser = Parser(tokens=lexer.get_tokens())
        parser.parse()

        alpha_conversion: LambdaAbstractionNode = AlphaConversion().alpha_convert(parser.get_ast()[0], "x", "z")

        self.assertEqual(alpha_conversion.param, "z")
        self.assertEqual(alpha_conversion.body.body.left, VariableNode("z"))

    def test_expr3(self):
        expr: str = "fn x.fn x.(x y)" # Renaming that's shadowed by inner binding

        lexer = Lexer(source=expr)
        lexer.tokenize()

        parser = Parser(tokens=lexer.get_tokens())
        parser.parse()

        alpha_conversion: LambdaAbstractionNode = AlphaConversion().alpha_convert(parser.get_ast()[0], "x", "z")
        print(alpha_conversion)

if __name__ == "__main__":
    unittest.main()