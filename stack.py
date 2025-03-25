from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from ast_internal import Expression


@dataclass
class StackFrame:
    function_name: str
    ast: Expression
    depth: int
    meta_data: Dict[str, Any] = field(default_factory=list)

    def __repr__(self):
        return f"StackFrame(function_name: {self.function_name}, AST: {self.ast}, Depth: {self.depth})"


class Stack:
    _instance = None # holds an instance of the class

    def __init__(self):
        self.stack: List[StackFrame] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __len__(self):
        return len(self.stack)

    def push(self, frame: StackFrame) -> None:
        print(f"Pushing: {frame} into stack")
        self.stack.append(frame)
        print(f"Current Stack state: {self.stack}")

    def pop(self) -> StackFrame:
        print(f"Popping item from stack")
        popped_item: StackFrame = self.stack.pop()
        print(f"Popped item: {popped_item}")
        return popped_item

    def peek(self) -> Optional[StackFrame]:
        if self.is_empty(): return None
        return self.stack[-1]

    def log(self) -> None:
        for stack_frame in self.stack:
            print(stack_frame)

    @property
    def is_empty(self) -> bool:
        return len(self.stack) == 0