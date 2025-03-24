from token_type import TokenType
from token_internal import Token
from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode
from typing import List


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens: List[Token] = tokens
        self.current_position: int = 0
        self.ast = []

    def parse(self) -> Expression:
        self.ast.append(self.parse_expression())
    
    def parse_expression(self) -> Expression:
        left: Expression = self.parse_term()

        while not self.is_at_end() and not self.check(TokenType.RPAREN.name):
            right: Expression = self.parse_term()
            left: Expression = LambdaApplicationNode(left, right)
        return left
    
    def parse_term(self):
        # Parse a term, which can be an abstraction, atom(variable) or paranthesised expression(application)
        # Let's first check if its a Lambda abstraction
        if self.match(TokenType.LAMBDA.name):
            return self.parse_abstraction()
        
        # If its not a Lambda abstraction, then it must be a Variable or an Application
        return self.parse_atom()
    
    def parse_abstraction(self) -> LambdaAbstractionNode:
        # There could be a single param or multiple params.
        # If its a single param, then its straight away a Lambda Abstraction
        # But if there are multiple params, then it is considered to be Lambda Abstraction with Lambda Application

        # we have already consumed the LAMBDA token, now let's consume the params
        params: List[Token] = []
        while not self.is_at_end() and self.peek().token_type != TokenType.DOT.name:
            params.append(self.advance())

        self.match(TokenType.DOT.name) # consume the "DOT" token

        body = self.parse_expression()
        for param in reversed(params):
            body = LambdaAbstractionNode(param.lexeme, body)
        return body
    
    def parse_atom(self) -> Expression:
        # Check if its starting with LPAREN, if true then it must be an application
        if self.match(TokenType.LPAREN.name):
            expr: Expression = self.parse_expression()

            # consume "RPAREN" token
            self.consume(TokenType.RPAREN.name, "Expected ')' after expression")

            return expr

        # Else it must be a Variable/Atom
        if self.match(TokenType.VARIABLE.name):
            return VariableNode(self.peek_previous().lexeme)

    ########################### HELPER FUNCTION ################################
    def consume(self, token_type: TokenType, error_msg: str) -> Token:
        if self.check(token_type):
            return self.advance()

        current_token: Token = self.peek()
        raise SyntaxError(f"{error_msg} Got {current_token} at line: {current_token.line}, column: {current_token.column}")

    def match(self, *expected_token_types: TokenType) -> bool:
        for token_type in expected_token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end(): return False
        return self.peek().token_type == token_type

    def advance(self) -> Token:
        current_token: Token = self.peek()
        self.current_position += 1
        return current_token

    def peek(self) -> Token:
        return self.tokens[self.current_position]
    
    def peek_previous(self) -> Token:
        return self.tokens[self.current_position - 1]

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.tokens) or self.tokens[self.current_position].token_type == TokenType.EOF.name

    def get_ast(self) -> List:
        return self.ast
    ########################### END OF HELPER FUNCTION #########################
