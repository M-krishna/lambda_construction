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

## Test cases to test Beta reduction

* `(fn x. x) y` => `y`

* `(fn x. x x) y` => `y y`

* `(fn x. (fn y. x)) z` => `fn y.z`

* `(fn x. x y) z` => `z y`

* `((fn x. x) (fn y. y)) z` => `z`

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

### The Big Picture
1. **Beta Reduction** is the core evaluation rule of lambda calculus: `(λx.M) N → M[x:=N]`
2. **Variable capture** can occur during substitution when free variables in `N` become accidentally bound in `M`
3. **Alpha conversion** resolves this by renaming bound variables in `M` to avoid conflicts with free variables in `N`
4. In a complete lambda calculus evaluator:
    * First check if substitution would cause variable capture
    * If so, perform the substitution
    * Then safely perform the substitution
    * Continue beta reduction until no more reductions are possible

## Test cases for free and bound variables

* `x` => free variable: `x` and bound variable is empty

* `fn x.x` => free variable is empty and bound variable is `x`

* `fn x. x y` => free variable is `y` and bound variable is `x`

* `fn x. fn y. x y` => free variable is empty and bound variables are `x` and `y`

* `(fn x. x) y` => free variable is `y` and bound variable is `x`

* `fn x. (fn y. x) z` => free variable is `z` and bound variables are `x` and `y`

## Looking at Variable Scoping and Variable Capture

**What is Variable Scoping?**

Lets take an expression `fn x. M`. Whenever there is a lambda abstraction it creates a scope for it. In this case, `x` is bounded to the scope `M`, that is the **body of the lambda expression**.

**Another example:** `fn x. x y`. Here the body of the lambda abstraction is `x y` and we have one param in Lambda abstraction named `x`. This parameter is bounded to the whole body of the lambda abstraction, which means the `x` in **body** is same as the param `x`


**Another example:** `fn x. fn x. y`. Here we have 2 lambda abstraction.
* The outer lambda abstraction is `fn x. M`, where `M` is `fn x. y`, which the body of the outer lambda abstraction
* The inner lambda abstraction is `fn x. y` and `y` is the body of the inner lambda abstraction
* Here,
    * The param `x` in outer lambda abstraction is bounded to inner lambda abstraction `fn x. y`
    * The param `x` in inner lambda abstraction is bounded to the body of the inner lambda abstraction, which is `y`

To recap what Variable scoping is,
* Variable scoping comes into picture when there is a Lambda abstraction
* For a given lambda abstraction `fn x. M`, `x` is bounded to `M` where `M` can be a **VariableNode, LambdaAbstractionNode or LambdaApplicatioNode**


**What is Variable Capture?**

We have seen what variable scoping is and how it works. To know more about variable capture, we need to understand the evaluation of Lambda calculus expressions. Let's look at some examples:

* **Example 1:** `(fn x.x) y`
    * Here I have a Lambda application of type `(M N)`, where `M` is `fn x. x` and `N` is `y`
    * `M` represents an **identity function**, which means the function returns its argument as the result
    * In `(fn x.x) y`, we are applying the identity function to the argument `y`
    * Which will give us `y` as its result
    * Since the body of the Lambda abstraction is just another Variable(`x`), **there is no variable capture here**

* **Example 2:** `(fn x. fn y. x y) y`
    * This is an interesting example for **Variable capture**
    * Here we have a Lambda application of type `(M N)`, where `M` is `(fn x. fn y. x y)` and `N` is `y`
    * Lets look at how this will get evaluated with **Normal order evaluation**
        * With Normal order evaluation, we won't **beta reduce** the argument first, instead we directly apply the function to the argument
        * In this case, `y` is bound to the outer lambda abstraction. Where `x := y`
        * Now we need to substitute `y` for `x` in the body of the outer lambda abstraction which is `fn x. x y`
        * After applying, we get `fn y. y y`. AHH THIS IS A PROBLEM!!!!
        * Can you see what the problem is????
        * The free variable `y` in `fn x. x y` got captured with this substitution and becomes a bound variable
        * But that is not the original form of the expression, in the original expression we had `fn x. x y`, where only `x` is bounded and `y` is free.
        * This is what we call as Variable capture

Now that we know about Variable scoping and Variable capture. Let's take a look at how can we solve this variable capture problem.

### Alpha conversion (again)
* Here is where alpha conversion comes in, specifically to solve variable capture.
* Alpha conversion takes places before the actual substitution process.
* Alpha conversion looks at the current scope of the variable it is going to replace and checks/verify whether this replacement will make the free variable become captured(bounded)
* Let's look at an example for alpha conversion:
    * Let's take the same expression as an example: `(fn x. fn y. x y) y`
    * Here, without alpha conversion if the substitution happens, we get `fn y. y y` as the result. Resulting in the free variable `y` to be captured.
    * To fix this, while the substitution process
        * We first check, if the variable names in the lambda expression might cause capture
        * If so, we rename the bound variable. In this case, we rename `y` to `z` changing it to `fn z. x z`


## What is Variable Shadowing?

Variable shadowing occurs when a variable declared in an inner scope (eg. as a lambda parameter) has the same name as a variable declared in outer scope. In this case, the inner declaration "shadows" or hides the outer one within its scope.

**Example 1: Basic Shadowing**
* Expression: `fn x. (fn x. x)`
* Step by step analysis:
    1. Outer lambda
        * `fn x. ...` binds the variable `x` for the entire body
    2. Inner Lambda
        * Inside the body, we have `fn x.x`. Here a new lambda binds `x` again
        * The inner `x` shadows the outer `x`. This means that within the inner's lambda's body, the `x` refers to the inner binding, not the outer one.
    3. Evaluation
        * If you were to apply this function to an argument, the inner binding would be used, and the outer `x` would not be accessible inside the inner lambda.
* How to resolve this?
    1. One common approach is to perform **alpha conversion** (or normalization) before evaluation.
    2. In normalization, you'd rename the inner lambda's parameter to something different, such as: ```fn x. (fn z. z)```

**Example 2: Shadowing in more complex expression**
* Expression: `fn x. (fn y. (x y))   applied to some argument might look like:   ((fn x. (fn y. (x y))) z)`
* Step by step analysis:
    1. Outer lambda
        * `fn x. ...` binds the variable `x` for the entire body
    2. Inner lambda
        * Inside the body, we have `fn y. (x y)`
        * Here `y` is freshly bound. Notice that `x` inside the inner lambda is free with respect to the inner lambda, but it is bound by the outer lambda
    3. Shadowing considerations:
        * Although there is no shadowing of `x` here, imagine if the inner lambda also used `x` as its parameter, eg. `fn x. (x y)`. In the case, the inner lambda's `x` would shadow the outer lambda's `x`

## Test cases for Variable capture and Variable shadowing

1. Variable capture: `(fn x. fn y. x) y`
2. Variable shadowing: `(fn x. (fn x. x) x) y`

## Church encodings
Church encodings allows you to represent data types and operations purely through lambda functions without using any built-in primitive data types.

### The fundamental idea
Imagine you want to represent numbers, but you can't use 0, 1, 2, etc. How would you do that? Church encodings allows us to represent numbers as functions that repeat a certain operation

### Church Numerals: Representing numbers
* A church numeral is a function that takes two arguments:
    1. A function `f`
    2. An initial value `x`
* The church numeral applies the function `f` to `x` a specific number of times.
```
zero:       λf.λx.x                 (applies f zero times)
one:        λf.λx.f(x)              (applies f once)
two:        λf.λx.f(f(x))           (applies f twice)
three:      λf.λx.f(f(f(x)))       (applies f three times)
```

**Example:** Let's say we want to represent 3, and our operation is "increment"
```
Three   =   λf.λx.f(f(f(x)))

If f is "increment" and x is 0:
Three(increment)(0) = 3
```

### Why this matters in Lambda calculus?
1. Everything is a function
2. No primitive data types needed
3. Can represent complex computations purely through function composition