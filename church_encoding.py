from ast_internal import Expression, VariableNode, LambdaAbstractionNode, LambdaApplicationNode
from ast_visualizer import to_json

class ChurchNumeral:
    def decode_church_numeral(self, expression: LambdaAbstractionNode):
        if not isinstance(expression, LambdaAbstractionNode):
            print("Not a church numeral")
            return
        
        body = expression.body
        
        # the lambda abstraction should have minimum two arguments
        # The body should also be a Lambda abstraction
        if not isinstance(body, LambdaAbstractionNode):
            print("Not a church numeral")
            return
        
        # Now we have an expression of the form: fn f. fn x. x
        # The last value in the whole expression could be either a VariableNode or a LambdaApplicationNode

        # If its a VariableNode, then we can consider it to be church numeral "zero"
        inner_body = body.body

        if (not isinstance(inner_body, VariableNode)) and (not isinstance(inner_body, LambdaApplicationNode)):
            print("Not a church numeral")
            return

        if isinstance(inner_body, VariableNode):
            print("church numeral zero 0")
        # else it must be an application
        if isinstance(inner_body, LambdaApplicationNode):
            # there might be "n" number of nested lambda applications
            print(to_json(inner_body))