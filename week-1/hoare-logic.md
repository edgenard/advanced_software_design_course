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

__In the latter example, how could we change the code without altering the postcondition?__

The values assigned to x and y can be changed to any number greater than 1. The assertions will still hold.

__How does the "forgetting" of assertions correspond to a form of modularity?__

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
d := (2-(a+1)/a)/2;
{ d = 0 or d = 1 }
m := d * 2 + (1 - d) * 3;
{ m = 3 or m = 2; if a = 0 => b = 0 else b is any integer}
x := b * 2;
{ m = 3 or m = 2; x is any integer }
x := x * 2
{ m = 3 or m = 2; x is any integer }
x := m * x
{ x is any integer }
x := x + 1;
{ ((a <= 0) => x = 8 * b + 1) /\ ((a > 0) => x = 12 * b + 1) }
```

__In what sense does this code contain a conditional?__

In order for the post-condition to hold, if a is 0 then b must also be 0, otherwise b can be any integer.

## Exercise 5

```
{ true }
d := (2-(a+1)/a)/2;
{ d = 0 or d = 1 }
m := d * 2 + (1 - d) * 3;
{ m = 3 or m = 2; if a = 0 => b = 0 else b is any integer}
x := b * 2;
{ m = 3 or m = 2; x is any integer }
x := m * x
{ x is any integer }
x := x * 2
{ x is any integer }
x := x + 1;
{ ((a <= 0) => x = 8 * b + 1) /\ ((a > 0) => x = 12 * b + 1)
```

I could not figure out how to use the CONSEQUENCE rule here. The only thing I could see to reduce the amount of
information in the assertions was to move `x := m * x` up a line so that the assertion would not have to have
`{ m = 3 or m = 2}`


## Exercise 6

```
i := 0
{ arr.length >= 1 /\ n =< arr.length } # loop invariant
while arr[i] != val && i < n  do
  { arr[i] != val && i < n } # this seems wrong but it's the only assertion that I can think of
  i := i + 1
  { i =< n}
end
{ arr[i] == val || (forall j, (j >= 0 && j < n ) => arr[j] != val)  }