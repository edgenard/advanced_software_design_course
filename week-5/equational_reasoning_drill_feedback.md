# Equational Reasoning Drill

## Changing a function call

```
((x, y) -> x + y + 1)(a + 1, b) ===  ((x, y) -> x + y + 1)(a, b + 1)
((a + 1) + b + 1) === (a + (b + 1) + 1)
// Associative Property of Addition
((a + 1) + (b + 1)) === ((a + 1) + (b + 1))
```

<------------ Feedback -------------->
Correct
<------------------------------------>

## Swapping an if-statement

```
if (true)  x else y -> x
if (false) x else y -> y
!true -> false
!false -> true
```

```
if (x) a else b === if (!x) b else a
x = true
if(true) a else b  === if(!true) b else a
!true -> false
if(true) a else b === if(false) b else a
a === a

x = false
if (false) a else b === if(!false) b else a
!false -> true
if (false) a else b === if (true) b else a
b === b
```

<------------ Feedback -------------->
Correct
<------------------------------------>

## Un-nesting an if statement

```
if (x) { if (y) a else b  } else b === if (x && y) a else b
```

```
x = true; y = true
if (true) { if (true) a else b } else b === if (true && true) a else b
if (true) { a } else b=== if (true) a else b
a === a

x = true; y = false
if (true) { if (false) a else b } else b === if (true && false) a else b
if (true) { b } else b === if (false) a else b
b === b

x = false; y = true
if (false) { if (true) a else b } else b === if (false && true) a else b
if (false) { a } else b === if (false) a else b
b === b

x = false; y = false
if (false) { if (false) a else b } else b === if (false && false) a else b
if (false) { b } else b === if (false && false) a else b
if (false) { b } else b === if (false) a else b
b === b
```

```
if (x) a else { if (y) a else b } === if (x || y) a else b

x = true; y = true
if (true) a else { if (true) a else b } === if (true || true) a else b
if (true) a else {  a  } === if (true || true) a else b
if (true) a else  a   === if (true) a else b
a === a

x = true; y = false
if (true) a else { if (false) a else b } === if (true || false) a else b
if (true) a else {  b  } === if (true || false) a else b
if (true) a else  a   === if (true) a else b
a === a

x = false; y = true
if (false) a else { if (true) a else b } === if (false || true) a else b
if (false) a else {  a  } === if (false || true) a else b
if (false) a else  a  === if (true) a else b
a === a

x = false; y = false
if (false) a else { if (false) a else b } === if (false || false) a else b
if (false) a else { b } === if (false || false) a else b
if (false) a else b  === if (false) a else b
b === b
```

<------------ Feedback -------------->
Correct
<------------------------------------>

## Conditional to Function

```
if (A) o.foo() else o.bar() === f = if (A) (() -> o.foo()) else (() -> o.bar()); f()

A = false;
if (false) o.foo() else o.bar() === f = if (false) (() -> o.foo()) else (() -> o.bar()); f()
o.bar() === f = () -> o.bar(); f()
o.bar() === f = o.bar()

A = true
if (true) o.foo() else o.bar() === f = if (true) (() -> o.foo()) else (() -> o.bar()); f()
o.foo() === f = () -> o.foo()); f()
o.foo() === f = o.foo())
```

<------------ Feedback -------------->

> > o.bar() === f = () -> o.bar(); f()
> > o.bar() === f = o.bar()

The result of applying the given assignment rule should be `o.bar()` and not `f = o.bar` since the rule states "to evaluate an assignment of a value to a variable x, you replace all later uses of that variable with the value."

Aside from that, the answer is correct.

<------------------------------------>
