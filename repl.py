import sys
import readline # needed for input history
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
            try:
                line = input(">>> ")
                if not line: continue
                if line.strip() == "(exit)": sys.exit(0)
                try:
                    self.run(line)
                except Exception as e:
                    print(f"{e}") 
            except EOFError:
                sys.exit(0)

    def run(self, source) -> None:
        lexer = Lexer(source)
        lexer.tokenize()

        parser = Parser(lexer.get_tokens())
        parser.parse()

        evaluator = Evaluator()
        for a in parser.get_ast():
            print(evaluator.beta_reduce(a))