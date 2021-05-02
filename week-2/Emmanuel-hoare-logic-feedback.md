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

**In the latter example, how could we change the code without altering the postcondition?**

The values assigned to x and y can be changed to any number greater than 1. The assertions will still hold.

<------------ Feedback -------------->
Correct. Note that it is correct because it's a change that is part of the family of possible changes to the code that still hold the final postcondition `{ z > 1 }`.
<------------------------------------>

**How does the "forgetting" of assertions correspond to a form of modularity?**

The code is less dependent on its environment. The more specific the assertion that is a precondition for a line of code
the more specific the code must be to be valid.

<------------ Feedback -------------->
That's a nice intuition on the relation of "forgetting" assertions and modularity.

To be more concrete, when there's the "forgetting" of an assertion the condition weakens. And a weakened condition describes a larger space of possible behaviors, meaning that there are more possible changes to the code that still fulfill the specification.
<------------------------------------>

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

<------------ Feedback -------------->
Correct
<------------------------------------>

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

<------------ Feedback -------------->

```
{ z = 1 or z = 0 }
a := z * 5 + (1 - z) * 12
{ ((x is odd) => a = 5) /\ ((x is even) => a = 12) }
```

Note how the precondition `{ z = 1 or z = 0 }` doesn't have any information on `x`. This means that on further conditions information about the value of `x` can't be recovered, since it's valid for the program to do anything with `x` (including trashing it). Therefore, the postcondition `{ ((x is odd) => a = 5) /\ ((x is even) => a = 12) }` doesn't hold

Check the official solutions to see the answer to this exercise.
<------------------------------------>

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

<------------ Feedback -------------->
There seems to be some misunderstandings on how to approach this exercise.

One of the goals of the Hoare Logic exercises is to mechanically derive preconditions from postconditions + commands using the rules given in the worksheet.
Here's an example of what that would look like for exercise 2:

{ a = 0 }
1 { (2-a) _ 2 + 1 = 5}
2 b := 2 -a
3 { b _ 2 + 1 = 5 }
4 c := b \* 2
5 { c+1 = 5 }
6 d := c + 1
7 { d = 5}

Notice how going from the condition on line 7 to the condition on line 5 is a simple matter of substituting "d" for "c+1". This is the result of doing applying the assignment rule shown on the worksheet: {[E/x]P}x:=E{P}

The same process should be used when doing this exercise. To give another example, here's how the first precondition of this exercise would look like:

```
{ ((a <= 0) => x = 8*b) /\ ((a > 0) => x = 12 * b)
{ ((a <= 0) => x + 1 = 8*b+1) /\ ((a > 0) => x + 1 = 12 * b + 1)
x := x + 1
{ ((a <= 0) => x = 8*b+1) /\ ((a > 0) => x = 12 * b + 1)
```

I suggest trying to do the exercises 3 and 4 again following the mechanical process and comparing them to the official solutions. Keep in mind that understanding Hoare triples gives the ability to identify the functionality of one or more statements completely independently of the rest of the program. It is a valuable skill to have when programming, so it's worth the extra effort to acquire it. Feel free to send us a message if there are any questions during the process.

Also note that the Hoare Triple below isn't valid as `x` being any integer, and `x = x + 1`, doesn't imply that `x = 8b + 1` when `a <= 0` or `x = 12b + 1` when `a > b`

```
{ x is any integer }
x := x + 1;
{ ((a <= 0) => x = 8 _ b + 1) /\ ((a > 0) => x = 12 _ b + 1) }
```

<------------------------------------>

**In what sense does this code contain a conditional?**

In order for the post-condition to hold, if a is 0 then b must also be 0, otherwise b can be any integer.

<------------ Feedback -------------->
Please check the official solutions and let us know if there are questions.
<------------------------------------>

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

<------------ Feedback -------------->
Note that some commands have dependencies in the order they execute, and if those dependencies aren't respected the end value of `x` won't be the same as it was before and the final postcondition won't hold. For example `x := m * x` has to run after ` x := x * 2`, so those two can´t be reordered as they were in the above solution.

Check the official solutions to see the answer to this exercise and also where the consequence rule is used. Please let's know if there are still questions after that.
<------------------------------------>

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

```

<------------ Feedback -------------->
Note that the given loop invariant isn't valid since it doesn't imply the final postcondition of the exercise.

```
{ arr[i] != val && i < n }
i := i + 1
{ i =< n}
```

Also note how the postcondition above doesn't make assertions about `arr`. This means that code following this postcondition can't make any assumption about `arr`, and changes to `arr`, such as trashing it, are valid changes that should keep the program working. Therefore, after this postcondition, it is impossible to reintroduce facts about `arr` and thus the final postcondition `{arr[i] == val || (forall j, (j >= 0 && j < n) => arr[j] != val)}` can't hold.

Check the official solutions to see the answer to this exercise.
<------------------------------------>
