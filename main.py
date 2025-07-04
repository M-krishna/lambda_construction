#!/usr/bin/env python3

import sys
from repl import Repl

arguments = sys.argv

def main():
    PROGRAM_NAME = "lambda_constructor"
    arg_len = len(arguments)
    repl = Repl()
    if arg_len > 2:
        print(f"Usage: {PROGRAM_NAME} [script]")
        sys.exit(64)
    elif arg_len == 2:
        repl.run_file(arguments[1])
    else:
        repl.run_prompt()

if __name__ == "__main__":
    main()