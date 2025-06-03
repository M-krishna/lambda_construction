from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode

class ChurchNumeral:
    def decode_church_numeral(self, expression: LambdaAbstractionNode):
        if not isinstance(expression, LambdaAbstractionNode):
            print("Not a church numeral")
            return
        