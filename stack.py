import os
from typing import Callable

def print_stack(func: Callable):

    if not isinstance(func, Callable):
        raise TypeError("Expected an argument of type function")# Get DEBUG flag from environment, default to 0
    
    debug_flag = int(os.getenv('DEBUG', 0))

    # Return the original function if the debug is off
    if not debug_flag:
        return func

    

    depth: int = 0
    MAX_DEPTH: int = 500

    def wrapper(*args, **kwargs):
        nonlocal depth

        if depth >= MAX_DEPTH:
            raise Exception("Maximum call stack depth exceeded")
        
        indent = " " * depth

        print(f"{indent} Entering {func.__name__}")
        print(f"{indent} args {args}")
        print(f"{indent} kwargs {kwargs}")

        depth += 1
        result = func(*args, **kwargs)
        depth -= 1

        print(f"{indent} Exiting {func.__name__}")
        return result

    return wrapper