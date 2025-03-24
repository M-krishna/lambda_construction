import sys
import readline
from lexer import Lexer
from parser import Parser
from beta_reduction import Evaluator


class Repl:
    def __init__(self, debug: int = 0):
        self.program_contents: str = ""
        self.debug = debug

    def run_file(self, file_path: str) -> None:
        with open(file_path, "r") as f:
            file_contents = f.read()
        self.program_contents = file_contents
        self.run(self.program_contents)

    def run_prompt(self):
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Lambda Constructor 0.0.1 (default, {now})")
        print("Type (exit) to quit the console")
        while True:
            line = input(">>> ")
            if not line: continue
            if line.strip() == "(exit)": sys.exit(0)
            try:
                self.run(line)
            except Exception as e:
               print(f"{e}") 

    def run(self, source) -> None:
        lexer = Lexer(source)
        lexer.tokenize()
        # for t in lexer.get_tokens():
        #     print(t)

        parser = Parser(lexer.get_tokens())
        parser.parse()
        # for a in parser.get_ast():
        #     print(json.dumps(a.to_json(), indent=4))

        evaluator = Evaluator()
        for a in parser.get_ast():
            print(evaluator.beta_reduce(a))

        # for a in parser.get_ast():
        #     free_variables = AlphaConversion()
        #     fv = free_variables.get_free_variables(a)
        #     print(f"free variables: {fv}")

        # for a in parser.get_ast():
        #     alpha_conversion = AlphaConversion()
        #     bv = alpha_conversion.get_bound_variables(a)
        #     print(f"Bound variables: {bv}")

        # for a in parser.get_ast():
        #     alpha_conversion = AlphaConversion()
        #     fv, bv = alpha_conversion.get_free_and_bound_variables(a)
        #     print(f"Free variables: {fv}")
        #     print(f"Bound variables: {bv}")
