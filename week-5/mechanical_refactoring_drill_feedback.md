# Mechanical Refactoring Drill

## Algebraically Refactoring a Weak API

```python
class ToDoItem:
  def __init__(self, dueDate, description, status, colour, isPublic):
    self.dueDate = dueDate
    self.description = description
    self.status = status
    self.colour = colour
    self.isPublic = isPublic

  def updateItem(self, key, value):
    setattr(self, key, value)
```

1. Imagine a program which takes a ToDoItem and sets all its attributes. What will happen if an attribute gets renamed, e.g.: "colour" to "color"?

   You might end up with two attributes for color. One named `color` and the other `colour`. The `updateItem` method does not enforce the name of the attributes.

<------------ Feedback -------------->
Correct. And it is likely to cause a runtime failure.
<------------------------------------>

2. Via the external view, it is possible to describe all states of a ToDoItem without referencing the implementation: a state of a ToDoItem is a call to the constructor followed by a sequence of calls to updateItem such that no key is set twice. Any sequence of calls can be "normalized" into a sequence of this form by removing all but the last call to each key. Using this as a definition of representable state, how does the implementation of ToDoItem violate the Representable/Valid principle?

   `updateItem` allows us to set an attribute on `TodoItem` that is not one of the ones in the constructor. You can also set the value of any of the attributes to whatever. This means that `dueDate` can be the integer 3 and `isPublic` can be the string "yes".

<------------ Feedback -------------->
The pointed issues are correct.

The first one can be both a violation of the "no junk" and "no fluff" parts of the R/V principle, depending on the interpretation of the valid states of a ToDoItem. If a TodoItem that has properties set that aren't received in the constructor is considered and invalid TodoItem, then it violates the "no junk" part. If a ToDoItem that gets an unknown property added represents the same ToDoItem, it violates the "no fluff" part as it allows for the same ToDoItem to be represented in multiple different ways.

<------------------------------------>

3. Write down the type of the updateItem function (i.e.: the sets of valid inputs and outputs) using the notation from lecture. Change it using algebraic laws to an equivalent type which helps avoid the problems raised in the earlier parts of this question. Update the code accordingly.

   ```
   # Currently
   updateItem: (key: string, value: any) -> None

   ```

   I think the way to avoid the problems raised in earlier parts of the this question is to have the `value` be dependent on the `key`. For example, the `dueDate` key should only have a value of the type `DateTime`. I'm not sure how to show this using the notation or if it's even possible in a type system. So I just made methods to update each key individually

   ```python
     from enum import Enum
     Status = Enum('Status', 'Complete Incomplete')
     Colour = Enum('Colour', 'Red Yellow Green')

     def updateDueDate(self, value: datetime) -> None:
       setattr(self, 'dueDate', value)

     def updateDescription(self, value: string) -> None:
       setattr(self, 'description', value)

     def updateStatus(self, value: Status) -> None:
       setattr(self, 'status', value)

     def updateColour(self, value: Colour) -> None:
       setattr(self, 'colour', value)

     def updateIsPublic(self, value: boolean) -> None:
       setattr(self, 'isPublic', value)

   ```

   > Hint 2: What is the exact set of all legal valid values to the "key" field? Use the notation S(x) to denote the "singleton type" that only contains one element, e.g.: S("hello") is the type that only contains the string hello. You should be able to write the type of all valid keys using the singleton type and the operators introduced in lecture

   The second hint seems to suggest that we can capture the type of the keys as `S('dueDate' 'description', 'status', 'colour', 'isPublic')`. However, there still seems to be the problem that the validity of the values for `value` depends on the `key`. So in order to limit the representable states to valid ones we would still need to have the valid values of the `value` field be dependent on the key. I don't see how having a type that enumerates the valid value of the `key` field does that.

   <------------ Feedback -------------->
   The suggested refactoring is the expected one.

   Note that the question asks to write the type of the function given its valid set of inputs and outputs. The suggested type `updateItem: (key: string, value: any) -> None` allows for invalid inputs. For example, it allows for the key `dueDate` with the value `true`.

   What the second hint meant to say is that it is possible to represent a key field as singleton using the notation S(x). For example, to represent the key `dueDate`, the notation would be S('dueDate').

   Given the above, the type `updateItem` can be described as:

   ```
   unit ^ (
   (S('dueDate') * date) +
   (S('description') * string) +
   (S('status') * string) +
   (S('colour') * string) +
   (S('ispPublic') * 2))
   ```

```
Apply product rule

void ^ (S('dueDate') * date) *
void ^ (S('description') * string) *
void ^ (S('status') * string) *
void ^ (S('colour') * string) *
void ^ (S('isPublic') * 2)

Substitute singleton type for unit

void ^ (1 * date) *
void ^ (1 * string) *
void ^ (1 * string) *
void ^ (1 * string) *
void ^ (1 * 2)

Multiply by identity

void ^ (date) *
void ^ (string) *
void ^ (string) *
void ^ (string) *
void ^ (2)

```

The type above translates to the refactoring shown in the answer.

<------------------------------------>

## Mechanically Refactoring a Weak API

```java
public void displayGame(String mode) {
  if (mode.equals("small")) {
        setColorDepth(8);
        drawRect(screen, 1024, 768);
  } else if (mode.equals("medium")) {
        setColorDepth(16);
        drawRect(screen, 1600, 1200);
  }
}
```

1. Suppose you wanted to write another function which printed the graphical settings associated with each mode. How would you reuse this code to do so?

   I don't think this code be re-used as is to get the graphical settings associated with each mode. The `printGraphicalSettings` code would look very similar:

   ```java
   public void printGraphicalSettings(String mode) {
     if (mode.equals("small")) {
         print('Color Depth: 8')
         print('Screen Resolution: 1024, 768')
     } else if (mode.equals("medium")) {
         print('Color Depth: 16')
         print('Screen Resolution: 1600, 1200')
       }
     }
   ```

<------------ Feedback -------------->
Correct. As is, the code can't be reused.
<------------------------------------>

2. Suppose someone who doesn't speak English is reading some code that invokes displayGame. Assume they had also not read the implementation of displayGame. What information would seeing the "mode" argument being passed in convey to them?

   Someone reading `displayGame('small')` or `displayGame('medium')` might assume that it has to do with the size of the game and not the size of the screen where the game is going to be displayed.

<------------ Feedback -------------->
Since whoever is reading the code doesn't understand english he/she wouldn't even get so far. The only information to be extracted here would be that `displayGame` receives a `string`.
<------------------------------------>

3. Refactor the function to replace the "mode" argument with something more semantically meaningful. Doing so should also eliminate the conditional

   ```java
   public datatype ScreenSize = Small | Medium;

   public void displayGame(ScreenSize screenSize) {
     setColor(screenSize.colorDepth)
     drawRect(screen, screenSize.width, screenSize.height)
   }
   ```

<------------ Feedback -------------->

There are a couple of issues with this solution.

The first one is that ScreenSize doesn't have the properties `colorDepth`, `width` and `height`. So `displayGame` won't compile.

The second one is that `ScreenSize` is declared as sum type (Not to be confused with union types from TypeScript). Recall from lecture 5 that for a sum type to be used, it's necessary to case over it. This means that by declaring `ScreenSize` as a sum type the code is bound to have a conditional. Here's how using `ScreenSize` looks like:

```java
   public datatype ScreenSize = Small | Medium;
   public void displayGame(ScreenSize screenSize) {
     switch(screenSize){
       case (Small):
          setColor(8);
          drawRect(screen, 1024, 768);
       case (Medium):
          setColor(16);
          drawRect(screen, 1600, 1200);
     }
   }
```

One way to make this answer correct is by changing the type of `ScreenSize` to the type below:

```java
enum Screen {
  SMALL(8, 1024, 768),
  MEDIUM(16, 1600, 1200);

  private int colorDepth;
  private int width;
  private int height;
}
```

<------------------------------------>

4. Show how to do this refactoring through a sequence of mechanical steps, as in lecture.

   I'm not sure if I can do this in a sequence of mechanical steps, the insight that led to the refactoring was to move the information about the color depth and resolution into a `ScreenSize` data type after I got to the point below.
   It also could have been a HashMap or similar data structure. It is also equivalent with the "Replace Conditional with Polymorphism" refactoring.

   ```java
     public void displayGame(String mode) {
       if (mode.equals("small")) {
           int colorDepth = 8
           int screenWidth = 1024
           int screenHeight = 768
       } else if (mode.equals("medium")) {
           int colorDepth = 16
           int screenWidth = 1600
           int screenHeight = 1200
       }
       setColorDepth(colorDepth);
       drawRect(screen, screenWidth, screenHeight);
     }
   ```

   I didn't find the hints helpful.

<------------ Feedback -------------->
Since the question before wasn't answered as expected, doing this exercise becomes very difficult to do. Please check the official solutions and let us know if there are any questions.
<------------------------------------>
