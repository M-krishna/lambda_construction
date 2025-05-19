from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode


class Evaluator:
    def beta_reduce(self, expression: Expression) -> Expression:
        match expression:
            case VariableNode(_):
                return expression
            case LambdaAbstractionNode(param, body):
                reduced_body: Expression = self.beta_reduce(body)
                return LambdaAbstractionNode(param, reduced_body)
            case LambdaApplicationNode(left, right):
                reduced_left = self.beta_reduce(left)

                if isinstance(reduced_left, LambdaAbstractionNode):
                    # Apply the lambda abstraction to whatever on the right
                    substituted_result = self.substitute(reduced_left.body, reduced_left.param, right)
                    return self.beta_reduce(substituted_result)

                reduced_right = self.beta_reduce(right)
                return LambdaApplicationNode(reduced_left, reduced_right)
    
    def substitute(self, body: Expression, param: Expression, argument: Expression):
        match body:
            case VariableNode(value):
                if value == param:
                    return argument
            case _:
                print("ignoring for now")