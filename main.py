#!/usr/bin/env python3

import sys
import readline
import json
from typing import List, Callable, Dict, Set, Tuple
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from collections import deque

arguments = sys.argv

##################### TOKEN TYPE #########################

class TokenType(Enum):
    VARIABLE = "variable"
    LAMBDA = "lambda" # In our program, "fn" is represented as lambda
    DOT = "dot"
    LPAREN = "lparen"
    RPAREN = "rparen"
    EOF = "eof"

##################### END OF TOKEN TYPE ##################


##################### TOKEN ##########################

@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int

    def __str__(self):
        return f""
    
    def __repr__(self):
        return f"Token({self.token_type}, {self.lexeme})"
##################### END OF TOKEN ###################



################### AST REPRESENTATION ####################
class Expression(ABC):

    def to_json(self):
        if isinstance(self, VariableNode):
            return {"type": self.type, "value": self.value}
        elif isinstance(self, LambdaAbstractionNode):
            return {"type": self.type, "param": self.param, "body": self.body.to_json()}
        elif isinstance(self, LambdaApplicationNode):
            return {"type": self.type, "func": self.left.to_json(), "arg": self.right.to_json()}


@dataclass
class VariableNode(Expression):
    value: str
    type: str = "Variable"

    def __str__(self):
        return f"{self.value}"
    
    def __repr__(self):
        return f"VariableNode({self.value})"


@dataclass
class LambdaAbstractionNode(Expression):
    param: str
    body: Expression
    type: str = "Lambda"

    def __str__(self):
        return f"fn {self.param}.{repr(self.body)}"

    def __repr__(self):
        return f"LambdaAbstractionNode('{self.param}', '{repr(self.body)}')"


@dataclass
class LambdaApplicationNode(Expression):
    left: Expression
    right: Expression
    type: str = "Application"

    def __str__(self):
        return f"({self.left} {self.right})"
    
    def __repr__(self):
        return f"LambdaApplicationNode({repr(self.left)}, {repr(self.right)})"

################### END OF AST REPRESENTATION ####################

################### LEXER ########################################

class Lexer:
    def __init__(self, source: str):
        self.source: str = source
        self.tokens: List[Token] = []
        self.start_position: int = 0
        self.current_position: int = 0
        self.line: int = 1
        self.column: int = 1
    
    def tokenize(self) -> List[Token]:
        while not self.is_at_end():
            self.start_position = self.current_position
            self.scan_tokens()

    def scan_tokens(self) -> None:
        c: str = self.advance()

        symbols: Dict[str, Callable] = {
            "(": lambda: self.add_token(TokenType.LPAREN.name),
            ")": lambda: self.add_token(TokenType.RPAREN.name),
            ".": lambda: self.add_token(TokenType.DOT.name),
            ";": lambda: self.skip_comments()
        }

        fn: Callable = symbols.get(c, lambda: self.default_case(c))
        try:
            fn()
        except Exception as e:
            raise SyntaxError(f"something went wrong during scanning: {e}")
    
    def skip_comments(self):
        while self.peek() != "\n" and not self.is_at_end():
            self.advance()
    
    def default_case(self, c):
        if self.is_whitespace(c):
            if c == "\n":
                self.line += 1
                self.column = 1
        elif self.is_alpha(c):
            self.scan_identifier(c)
        else:
            raise SyntaxError(f"Unknown character: {c}")
    
    def scan_identifier(self, current_chr: str):
        if current_chr == "f" and self.peek() == "n" and self.peek_next() == " ":
            self.advance() # consume "n" character
            self.add_token(TokenType.LAMBDA.name)
        else:
            self.add_token(TokenType.VARIABLE.name)


    def add_token(self, token_type: TokenType) -> None:
        lexeme: str = self.source[self.start_position:self.current_position]
        self.tokens.append(Token(token_type, lexeme, self.line, self.column - len(lexeme)))

    ########################## HELPER FUNCTIONS #######################
    def is_alpha(self, c: str) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' or c <= 'Z')

    def is_whitespace(self, c: str) -> bool:
        SPACE: str = " "
        NEWLINE: str = "\n"
        TABSPACE: str = "\t"
        return c in [SPACE, NEWLINE, TABSPACE]

    def advance(self) -> str:
        current: str = self.source[self.current_position]
        self.current_position += 1
        self.column += 1
        return current

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current_position]
    
    def peek_next(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current_position + 1]

    def is_at_end(self) -> bool:
        return self.current_position >= len(self.source)

    def get_tokens(self) -> List[Token]:
        return self.tokens 
    ########################## END OF HELPER FUNCTIONS ################


################### END OF LEXER #################################

################### PARSER ########################################

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

################### END OF PARSER ########################################

################### ALPHA CONVERSION ##########################

class AlphaConversion:
    def alpha_convert(self, ast: Expression, old_param: str, new_param: str):
        if isinstance(ast, VariableNode):
            if ast.value == old_param:
                return VariableNode(new_param)
            return ast
        elif isinstance(ast, LambdaAbstractionNode):
            if ast.param == old_param:
                return LambdaAbstractionNode(new_param, self.alpha_convert(ast.body, old_param, new_param))
            else:
                return LambdaAbstractionNode(ast.param, self.alpha_convert(ast.body, old_param, new_param))
        elif isinstance(ast, LambdaApplicationNode):
            new_left = self.alpha_convert(ast.left, old_param, new_param)
            new_right = self.alpha_convert(ast.right, old_param, new_param)
            return LambdaApplicationNode(new_left, new_right)
        else:
            raise SyntaxError(f"Unknown node type: {ast}")

    def get_free_variables(self, ast: Expression):
        if isinstance(ast, VariableNode):
            return {ast.value}
        elif isinstance(ast, LambdaAbstractionNode):
            return self.get_free_variables(ast.body) - {ast.param}
        elif isinstance(ast, LambdaApplicationNode):
            return self.get_free_variables(ast.left) | self.get_free_variables(ast.right)
        else:
            raise SyntaxError(f"Unknown node type: {ast}")

    def get_bound_variables(self, ast: Expression, scope: Set = set()):
        if isinstance(ast, VariableNode):
            return {ast.value} if ast.value in scope else set()
        elif isinstance(ast, LambdaAbstractionNode):
            new_scope: Set = scope | {ast.param}
            inner_bound: Set = self.get_bound_variables(ast.body, new_scope)
            return inner_bound | {ast.param}
        elif isinstance(ast, LambdaApplicationNode):
            return self.get_bound_variables(ast.left, scope) | self.get_bound_variables(ast.right, scope)
        else:
            raise SyntaxError(f"Unknown node type: {ast}")


    def get_free_and_bound_variables(self, ast: Expression, scope: Set = set()):
        free_variables: Set = set()
        bound_variables: Set = set()
        queue: deque = deque([(ast, scope)])

        while queue:
            current_node, current_scope = queue.pop()

            match current_node:
                case VariableNode(value):
                    if value not in current_scope:
                        free_variables.add(value)
                    else:
                        bound_variables.add(value)
                case LambdaAbstractionNode(param, body):
                    bound_variables.add(param) # Add the param as bound variable
                    new_scope = current_scope | {param}
                    queue.append((body, new_scope)) # This will get the bounded variables in inner scope as well
                case LambdaApplicationNode(left, right):
                    queue.append((left, current_scope))
                    queue.append((right, current_scope))
                case _:
                    raise SyntaxError(f"Unknown node type: {current_node}")
        result: Tuple[List, List] = (list(free_variables), list(bound_variables))
        return result

    def generate_new_variable(self, old_param: str, forbidded_variables: Set):
        # The newly generated variable shouldn't be part of the "free_variables" set
        # and it should be like "old_param"
        candidate = old_param
        counter = 1
        while candidate in forbidded_variables:
            candidate = f"{old_param}{counter}"
            counter += 1
        return candidate

################### END OF ALPHA CONVERSION ##########################

################### INTERPRETER/EVALUATOR ########################

class Evaluator:
    def __init__(self):
        self.alpha_conversion = AlphaConversion()

    def beta_reduce(self, ast: Expression):
        match ast:
            case VariableNode(_):
                return ast
            case LambdaAbstractionNode(param, body):
                reduced_body = self.beta_reduce(body)
                return LambdaAbstractionNode(param, reduced_body)
            case LambdaApplicationNode(left, right):
                new_left = self.beta_reduce(left)

                if isinstance(new_left, LambdaAbstractionNode):
                    substituted_result = self.substitute(new_left.param, new_left.body, right)
                    return self.beta_reduce(substituted_result)
                
                new_right = self.beta_reduce(right)
                return LambdaApplicationNode(new_left, new_right)
            case _:
                raise SyntaxError(f"Unknown node type: {ast}")
    
    def substitute(self, param: Expression, body: Expression, argument: Expression):
        match body:
            case VariableNode(value):
                if param == value:
                    return argument
                return body
            case LambdaAbstractionNode(_param, _body):
                if param != _param:
                    # Before substituting we have to check, whether the substitution will cause variable capture

                    # Get the free variable in the argument
                    fv = self.alpha_conversion.get_free_variables(argument)

                    # Check if the free variable conflicts with the lambda's parameter
                    if _param in fv:
                        # Generate a new variable
                        new_param: str = self.alpha_conversion.generate_new_variable(_param, fv | self.alpha_conversion.get_free_variables(_body) | self.alpha_conversion.get_bound_variables(_body))

                        # Once you have a new variable, now alpha convert the body
                        new_body = self.alpha_conversion.alpha_convert(_body, _param, new_param)

                        # Now substitute the alpha converted body
                        r = self.substitute(param, new_body, argument)
                        return LambdaAbstractionNode(new_param, r)

                    r = self.substitute(param, _body, argument)
                    return LambdaAbstractionNode(_param, r)
                return body
            case LambdaApplicationNode(left, right):
                new_left = self.substitute(param, left, argument)
                new_right = self.substitute(param, right, argument)
                return LambdaApplicationNode(new_left, new_right)
            case _:
                raise SyntaxError(f"Unknown node type: {body}")

################### END OF INTERPRETER/EVALUATOR #################

################### REPL #############################

class Repl:
    def __init__(self, debug: int = 0):
        self.program_contents: str = ""
        self.debug = debug

    def run_file(self, file_path: str) -> None:
        with open(file_path, "r") as f:
            file_contents = f.read()
        self.program_contents = file_contents
        self.run(self.program_contents)

    def run_prompt(self):
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Lambda Constructor 0.0.1 (default, {now})")
        print("Type (exit) to quit the console")
        while True:
            line = input(">>> ")
            if not line: continue
            if line.strip() == "(exit)": sys.exit(0)
            try:
                self.run(line)
            except Exception as e:
               print(f"{e}") 

    def run(self, source) -> None:
        lexer = Lexer(source)
        lexer.tokenize()
        # for t in lexer.get_tokens():
        #     print(t)

        parser = Parser(lexer.get_tokens())
        parser.parse()
        # for a in parser.get_ast():
        #     print(json.dumps(a.to_json(), indent=4))

        evaluator = Evaluator()
        for a in parser.get_ast():
            print(evaluator.beta_reduce(a))

        # for a in parser.get_ast():
        #     free_variables = AlphaConversion()
        #     fv = free_variables.get_free_variables(a)
        #     print(f"free variables: {fv}")

        # for a in parser.get_ast():
        #     alpha_conversion = AlphaConversion()
        #     bv = alpha_conversion.get_bound_variables(a)
        #     print(f"Bound variables: {bv}")

        # for a in parser.get_ast():
        #     alpha_conversion = AlphaConversion()
        #     fv, bv = alpha_conversion.get_free_and_bound_variables(a)
        #     print(f"Free variables: {fv}")
        #     print(f"Bound variables: {bv}")

################### END OF REPL #############################

def main():
    PROGRAM_NAME = "lambda_constructor"
    arg_len = len(arguments)
    repl = Repl()
    if arg_len > 2:
        print(f"Usage: {PROGRAM_NAME} [script]")
        sys.exit(64)
    elif arg_len == 2:
        repl.run_file(arguments[1])
    else:
        repl.run_prompt()

if __name__ == "__main__":
    main()