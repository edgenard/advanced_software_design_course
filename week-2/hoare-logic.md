# Hoare Logic
#### Emmanuel Genard

## Exercise 1

```
{ true }
x = 10;
{ x > 1}
y = 42;
{ x > 1, y > 1 }
z = x + y
{ z > 1}
```



### In the latter example, how could we change the code without altering the postcondition?

The values assigned to x and y can be changed to any number greater than 1. The assertions will still hold.

### How does the "forgetting" of assertions correspond to a form of modularity?

The code is less dependent on its environment. The more specific the assertion that is a precondition for a line of code
the more specific the code must be to be valid.

## Exercise 2

```
{ a = 0 }
b := 2 - a
{ b = 2 }
c := b * 2
{ c = 4 }
d := c + 1
{ d = 5}
```

## Exercise 3

```
{ x > 0 }
y := (x / 2) * 2
{ y = x or y = x - 1 }
z := x - y
{ z = 1 or z = 0 }
a := z * 5 + (1 - z) * 12
{ ((x is odd) => a = 5) /\ ((x is even) => a = 12) }
```

## Exercise 4

```
{ true }
d :=
```