from abc import ABC
from dataclasses import dataclass


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