from collections import deque
from typing import Set, List, Tuple
from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode


class AlphaConversion:
    def alpha_convert(self, ast: Expression, old_param: str, new_param: str):

        def normalize(ast: Expression, scope: Set):
            if isinstance(ast, VariableNode):
                if ast.value == old_param and old_param in scope[-1]:
                    return VariableNode(new_param)
                return ast
            elif isinstance(ast, LambdaAbstractionNode):
                new_scope = set(scope[-1]) # create a new scope by extending the current scope

                # Handle the parameter
                new_param_name = ast.param
                if ast.param == old_param and old_param in scope[-1]:
                    new_param_name = new_param
                    # Add new param to the scope for the body
                    new_scope.add(new_param)
                else:
                    new_scope.add(ast.param)
                
                # Process the body with the new scope
                new_body = normalize(ast.body, scope + [new_scope])
                return LambdaAbstractionNode(new_param_name, new_body)
            elif isinstance(ast, LambdaApplicationNode):
                new_left = normalize(ast.left, scope)
                new_right = normalize(ast.right, scope)
                return LambdaApplicationNode(new_left, new_right)
            else:
                raise SyntaxError(f"Unknown node type: {ast}")
        initial_scope = {old_param}
        return normalize(ast, [initial_scope])

        # if isinstance(ast, VariableNode):
        #     if ast.value == old_param:
        #         return VariableNode(new_param)
        #     return ast
        # elif isinstance(ast, LambdaAbstractionNode):
        #     if ast.param == old_param:
        #         return LambdaAbstractionNode(new_param, self.alpha_convert(ast.body, old_param, new_param))
        #     else:
        #         return LambdaAbstractionNode(ast.param, self.alpha_convert(ast.body, old_param, new_param))
        # elif isinstance(ast, LambdaApplicationNode):
        #     new_left = self.alpha_convert(ast.left, old_param, new_param)
        #     new_right = self.alpha_convert(ast.right, old_param, new_param)
        #     return LambdaApplicationNode(new_left, new_right)
        # else:
        #     raise SyntaxError(f"Unknown node type: {ast}")

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
