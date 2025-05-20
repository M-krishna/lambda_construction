from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode

def print_stack(func):

    depth: int = 0

    def wrapper(*args, **kwargs):
        nonlocal depth

        indent = " " * depth
        print(f"{indent}\r Entering {func.__name__}")
        print(f"{indent} args: {args}")
        print(f"{indent} kwargs: {kwargs}")

        depth += 1 # Increment before recursive call
        result = func(*args, **kwargs)
        depth -= 1 # Decrement after recursive call

        print(f"{indent} Exiting {func.__name__}")
        return result


    return wrapper

class Evaluator:
    
    @print_stack
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
    
    @print_stack
    def substitute(self, body: Expression, param: Expression, argument: Expression):
        match body:
            case VariableNode(value):
                if value == param:
                    return argument
            case LambdaAbstractionNode(_param, _body):
                print(f"param: {_param}")
                print(f"body: {_body}")
                print(f"argument: {argument}")
            case _:
                print("ignoring for now")