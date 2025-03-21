## Variable
* Things like x, y, etc
* The lexer should return a token type named `Variable`
* The parser should return an ast node named `VariableNode` whose value/lexeme should be the value we parsed

## Function Abstraction (Lambda Abstraction)
* Things like \x. y, where \ => represents Lambda, x => represents parameter and y => represents body expression
* The lexer should return a token type named `Lamba` when it scans the `\`
* The parser should return an ast named `LambdaAbstractionNode` which contain 2 things.
    * One is `param`, which holds the parameter value
    * The other is `body` which holds the parsed body expression

## Function Application
* Things like (x y) or xy or (\x.y)x and so on
* A function application starts with `left paranthesis` and ends with `right parenthesis`
* The parser should return an ast named `LambdaApplication` which contains 2 things.
    * `left` holds the left section of the application
    * `right` holds the right section of the application
* While evaluating a function application, we apply the value of `right` to `left` only if applicable


## Grammar for Lambda calculus
```
Expression  -> Term { Term }
Term        -> LAMBDA VARIABLE DOT Expression   ; lambda abstraction
            | VARIABLE                        ; single-character variable
            | LPAREN Expression RPAREN        ; parenthesized expression

The { Term } means that consecutive terms form an application.
```