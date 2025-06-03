from ast_internal import VariableNode, LambdaAbstractionNode, LambdaApplicationNode
from typing import Optional

class ChurchNumeral:
    def decode_church_numeral(self, expression: LambdaAbstractionNode) -> Optional[int]:
        """
        Check if expression is a Church numeral and return its value.
        
        Args:
            expression: Lambda abstraction to check
            
        Returns:
            int: The Church numeral value if valid
            None: If not a valid Church numeral
        """
        # Validate basic structure
        if not isinstance(expression, LambdaAbstractionNode):
            return None

        if not isinstance(expression.body, LambdaAbstractionNode):
            return None

        inner_body = expression.body.body

        # Not a valid church numeral structure
        if (not isinstance(inner_body, VariableNode)) and (not isinstance(inner_body, LambdaApplicationNode)):
            return None

        # Handle zero case
        if isinstance(inner_body, VariableNode):
            return 0

        # Handle positive numbers
        if isinstance(inner_body, LambdaApplicationNode):
            return self._count_application(inner_body)

    def _count_application(self, node: LambdaApplicationNode):
        count: int = 0
        current = node

        while isinstance(current, LambdaApplicationNode):
            count += 1
            current = current.right
        return count