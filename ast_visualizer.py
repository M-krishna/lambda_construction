import json
from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode


def to_json(expression: Expression, indent: int = 2) -> str:

    def to_dict(expr: Expression) -> dict:
        match expr:
            case VariableNode(value):
                return {"type": "VariableNode", "value": value}
            case LambdaAbstractionNode(param, body):
                return {"type": "LambdaAbstractionNode", "param": param, "body": to_dict(body)}
            case LambdaApplicationNode(left, right):
                return {"type": "LambdaApplicationNode", "left": to_dict(left), "right": to_dict(right)}
    return json.dumps(to_dict(expression), indent=indent)