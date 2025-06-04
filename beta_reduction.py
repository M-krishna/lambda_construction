from typing import Dict, Set
from alpha_conversion import AlphaConversion
from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode
from stack import print_stack


class Evaluator:
    def __init__(self):
        self.alpha_conversion = AlphaConversion()

    def normalize(self, ast: Expression, mapping: Dict = None, used: Set = None):
        # Normalize the AST to avoid variable shadowing
        # This will help with Alpha conversion (while substituting)
        if mapping is None:
            mapping = {}
        if used is None:
            used = set()
        
        if isinstance(ast, VariableNode):
            if ast.value in mapping:
                return VariableNode(mapping[ast.value])
            return ast
        elif isinstance(ast, LambdaAbstractionNode):
            # Generate a fresh name for the current parameter.
            # The forbidden set is everything already used
            new_param = self.alpha_conversion.generate_new_variable(ast.param, used | set(mapping.values()))
            used.add(new_param)

            # Copy the current mapping and add the new renaming
            new_mapping = mapping.copy()
            new_mapping[ast.param] = new_param

            # Recursively normalize the body
            new_body = self.normalize(ast.body, new_mapping, used)
            return LambdaAbstractionNode(new_param, new_body)
        elif isinstance(ast, LambdaApplicationNode):
            new_left = self.normalize(ast.left, mapping, used)
            new_right = self.normalize(ast.right, mapping, used)
            return LambdaApplicationNode(new_left, new_right)
        else:
            raise SyntaxError(f"Unknown node type: {ast}")

    @print_stack
    def beta_reduce(self, ast: Expression) -> Expression:
        # normalized_ast: Expression = self.normalize(ast)

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
    
    @print_stack
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