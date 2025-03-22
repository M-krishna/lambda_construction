## Variable
* Things like x, y, etc
* The lexer should return a token type named `Variable`
* The parser should return an ast node named `VariableNode` whose value/lexeme should be the value we parsed

## Function Abstraction (Lambda Abstraction)
* Things like fn x. y, where fn => represents Lambda, x => represents parameter and y => represents body expression
* The lexer should return a token type named `Lamba` when it scans `fn`
* The parser should return an ast named `LambdaAbstractionNode` which contain 2 things.
    * One is `param`, which holds the parameter value
    * The other is `body` which holds the parsed body expression

## Function Application
* Things like `(x y)` or `xy` or `(fn x.y)x` and so on
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

## Beta reduction
Beta reduction is a fundamental operation in Lambda calculus that represents the process of function application. Think of it as "executing" a function by replacing its parameters with the argument provided.

**Imagine a function in Math**

Suppose you have a simple function:
> `f(x) = x + 2`

When you compute `f(3)`, you substitue `x` with `3` to get:
> `3 + 2 = 5`

**In Lambda Calculus**

Lambda calculus represents functions in a very compact form. A Lambda abstraction looks like this:
> `λx. M`

Here `x`, is the parameter and `M` is the function body(which could be any expression involving `x`). When you apply this function to an argument `N`, you write it as:

> `(λx. M) N`

**Beta reduction** is the process of **substituting every free occurence of x in M with N**. We denote this substitution as:

> `M[x := N]`

**An example step-by-step**

Consider this expression:

> `(λx. x + 1) 5`

**Step 1: Identify the function and the argument**
* Function: `λx. x + 1`
* Argument: `5`

**Step 2: Substitute the parameter**
* Replace `x` in the body `x + 1` with `5`:

> `x + 1 becomes 5 + 1`

**Step 3: Evaluate (if necessary)**

> `5 + 1 = 6`

So, the **beta reduction** of `(λx. x + 1) 5` results in `6`

**Examples for beta reduction**
1. Let's beta reduce `(fn x.x) a`
    * Here we have to apply the lambda abstraction to its argument a
    * The lambda abstraction have only one param named `x`, which is a bound variable
    * While substituing we will check, if the param `x` is present in the body.
    * In this case, its true. `x` is present in the body.
    * So we will substitute `x` with `a`

2. Let's beta reduce `(fn xy. y) a`
    * The above expression can be written as `(fn x. fn y. y) a`
    * Here the lambda abstraction is `(fn x. fn y. y)` and will be applied to `a`
    * The body of the lambda abstraction is again a Lambda abstraction which is `fn y. y`
    * So, We will first check if the outermost param is equal to the inner most param.

### Normal order Vs Applicative order evaluation (part of beta reduction evaluation strategy)

**Normal order evaluation**

In normal order evaluation, arguments to functions are evaluated only when needed. This is also known as "lazy-evaluation" or "call-by-name".

**Process:**
1. Always reduce the leftmost, outermost redex first
2. Arguments are substituted into functions without being evaluated first.
3. Only evaluate arguments when their values are actually needed.

**Example:**
`(λx. x x) ((λy. y) z)`

**Normal order evaluation steps**
```
(λx. x x) ((λy. y) z)
→ ((λy. y) z) ((λy. y) z)    // Substitute without evaluating
→ z ((λy. y) z)              // Reduce left expression
→ z z                        // Reduce right expression
```

**Applicative order evaluation**

In applicative order evaluation, arguments are fully evaluated before being passed to functions. This is also known as "eager evaluation" or "call-by-value".

**Process:**
1. Evaluate all arguments to a function before applying the function.
2. Reduce the leftmost, innermost redex first
3. Only substitute fully evaluated expressions

**Example**
`(λx. x x) ((λy. y) z)`

**Applicative order evaluation steps**
```
(λx. x x) ((λy. y) z)
→ (λx. x x) z                // Evaluate argument first
→ z z                        // Apply function
```

The key difference is that normal order delays evaluation until necessary, while applicative order evaluates arguments immediately. This can lead to different behaviour, especially with non-terminating expressions.


### Alpha conversion
Alpha conversion is the process of renaming bound variables in a lambda expression to avoid name conflicts (variable capture) during substitution.

**Purpose:** Ensures free variables in an argument don't accidently become bound when substituted.

**Where Alpha conversion fits in Beta reduction?**

Alpha conversion is a preparatory step before performing beta reduction when variable conflicts might occur. It preserves the meaning of the expressions while making substitution safe.

**Example 1: Simple Alpha Conversion**
```
λx.x → λy.y
```

These expressions are alpha equivalent (same function, different variable names)

**Example 2: Avoiding variable capture**

Consider beta reducing: `(λx.λy.x y) y`

Without alpha conversion:
```
(λx.λy.x y) y → λy.y y  // WRONG! The free 'y' became bound
```

With Alpha conversion:
```
(λx.λy.x y) y → (λx.λz.x z) y  // Alpha convert λy to λz
→ λz.y z  // Now correct beta reduction
```

**Example 3: Multiple Bound Variable**
```
λx.λx.x → λx.λy.y  // Rename the inner x to y for clarity
```

Alpha conversion ensures that substitution during beta reduction preserves the intended meaning of your lambda expressions by preventing variable capture problems.

## Test cases to test Beta reduction

* `(fn x. x) y` => `y`

* `(fn x. x x) y` => `y y`

* `(fn x. (fn y. x)) z` => `fn y.z`

* `(fn x. x y) z` => `z y`

* `((fn x. x) (fn y. y)) z` => `z`