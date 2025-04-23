from ast_internal import VariableNode, LambdaAbstractionNode, LambdaApplicationNode


class ChurchEncoding:
    
    def encode_numeral(self, numeral: int):
        pass

    def decode_numeral(self, ast: LambdaAbstractionNode):
        match ast:
            case LambdaAbstractionNode(param, body):  # Outer Lambda
                match body:
                    case LambdaAbstractionNode(_param, _body): # Inner Lambda
                        # Check the param of outer lambda and inner lambda
                        # If both are equal, then the expression is not a church numeral
                        if param == _param:
                            print("parameters must not be equal in church numeral")
                            return

                        # Check the body of the inner lambda
                        match _body:
                            case VariableNode(value):
                                # If its a VariableNode, then the value must be equal to the
                                # value of inner lambda param
                                if value != _param:
                                    print("This is not a church numeral")
                                    return
                                return 0
                            case LambdaApplicationNode(left, right):
                                # If its an ApplicationNode, then we have to count how many times
                                # the function has been applied to the argument
                                application_count = 1

                                current_node = right
                                while isinstance(current_node, LambdaApplicationNode):
                                    application_count += 1
                                    current_node = current_node.right
                                return application_count
                    case _:
                        print("not a church numeral")
                        return
            case _:
                print("Looks like the given expression is not a church numeral")
                return