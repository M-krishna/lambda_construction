# Lambda Constructor

A simple Lambda Calculus interpreter implemented in Python that supports basic lambda calculus operations.

## Features
* Lambda abstractions (using `fn` keyword)
* Variable bindings
* Function applications
* Interactive REPL mode
* File execution mode
* Comment support (using `;`)

## Usage
```bash
# Run in REPL mode
python main.py

# Execute a lambda calculus file
python main.py program.lbda
```

## Syntax Examples
```lisp
; Variables
x

; Lambda abstraction
fn x.x

; Multiple parameter abstraction
fn x y z.x

; Function application
(x y)
```

## Grammar
The interpreter follows this grammar:
```text
Expression  -> Term { Term }
Term        -> LAMBDA VARIABLE DOT Expression   ; lambda abstraction
            | VARIABLE                          ; variable
            | LPAREN Expression RPAREN          ; parenthesized expression
```

## Exit REPL
Type `(exit)` to quit the interactive console.