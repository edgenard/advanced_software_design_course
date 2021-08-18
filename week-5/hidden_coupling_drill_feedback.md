# Hidden Coupling Drill

1. What is the coupling in this example?
2. Is the coupling visible or hidden?
3. If the coupling is hidden, then how can I remove it?

## Example 1

```java
public void foo() {
  bar(1,2,3);
}

public void bar(int a, int b, int c) {
  System.out.println(a+b+c);
}
```

1. `foo` has to know that `bar` takes three arguments. That those arguments are integers.
2. I think the coupling is visible

<------------ Feedback -------------->
Correct, the coupling is visible since there's a method call from `foo` to `bar`
<------------------------------------>

## Example 2

```c
char *str = "Hello, ";
char *buf = malloc(8+strlen(name));
strcat(buf, str, name);
```

1. `*buf` has to know that `*str` is 8 characters.
2. This coupling is hidden
3. You can remove it by writing something like: `*buf = malloc(strlen(str)+strlen(name))`

<------------ Feedback -------------->
Correct
<------------------------------------>

## Example 3

```c++
struct Game {
   ....
   Player players[2];
   ....
}


for (int i = 0; i < 2; i++) {
  if (game.players[i].isVictorious()) {
      ....
  }
}
```

1. The `for` loop assumes that there are ever only two players. It also has to to know that `isVictorious` is a method on the `Player` object
2. I think the count of players is a hidden coupling but the the method name is visible.
3. The `for` loop could be changed to `for (int i = 0; i < game.players.count(); i++)` You can also not use a `for` loop at all and use something like a `select` or `find` function so iterates over `game.players`
   and returns the first player for which `isVictorious` is true.

<------------ Feedback -------------->
Correct
<------------------------------------>

## Example 4

```python
def user_history(days=90):
  # Do 90 days of history by default
  for i in xrange(days):
    # do stuff
```

I don't think I see any coupling here. This function seems to be fairly sef-contained.

<------------ Feedback -------------->
The hidden coupling exists between the default value 90 and the comment `# Do 90 days of history by default`. To keep the codebase consistent, both have to change in tandem.
<------------------------------------>

## Example 5

```java
public class A {
  public void log() {
    ....
    writeLineToFile("log.txt", ...)
    ....
  }
}



public class B {
  public void b() {
    ....
    writeLineToFile("log.txt", ...)
    ....
  }
}
```

1. Since both methods write to the same file, they might overwrite each other. It could be hard to know which method wrote which line.
2. If the classes are close to each other in the code base this coupling could be visible but most likely it's hidden. I bet the only way that this would be found out is through some weird data in the "log.txt" file.
3. To make this coupling visible we could use `A.log` in `B.b`. If that were not possible we could have the knowledge of the which file to write to hidden away somewhere, maybe a `LogWriter` class that just exposes a `write` method and nothing else.

<------------ Feedback -------------->
Recall that two pieces of code are coupled when changing a design decision will require both pieces of code to change in tandem to maintain some property of the system.

Given that logging is usually done by having different parts of the system write to the same file, it is very likely that if the name of the log file changes, both class A and class B have to change in tandem to keep the system working as expected. The underlying design decision that couples A and B is the name of the file.

> Since both methods write to the same file, they might overwrite each other. It could be hard to know which method wrote which line.

If there's concurrency at play and `writeLineToFile` is not correctly implemented to deal with that, that might be case. However, that doesn't mean that there's coupling between A and B.

> If the classes are close to each other in the code base this coupling could be visible but most likely it's hidden.

While proximity in the code between the classes makes it easy to identify the couping, the coupling is still hidden. As the answer points out, if it weren't for the proximity, it would be hard to figure out that A and B have to change in tandem.

One way to get rid of this hidden coupling is to encapsulate the name of the file behind a method, and have both A and B use the method.

<------------------------------------>

## Example 6

### Server

```python
def handleRequest(request):
  username = request["username"]
  password = request["password"]
  # …
```

### Client

```html
<form ...>
  <input type="text" name="username"></input>
  <input type="text" name="password"></input>
  <button type="submit"></button>
</form>
```

1. The keys, "username" and "password" are coupled between the client and server.
2. I think this coupling is visible.
3. I don't think it can be removed. We can add validation on the server to alert us if the request doesn't have the expected data but the coupling will still be there.

<------------ Feedback -------------->

To keep the program working correctly it is necessary to change both the client and server in tandem, and just by looking at the `handleRequest` and following the code it is not straightforward to figure out all the places in the client that would have to change. Therefore, the coupling is hidden.

One way to remove this coupling would be by using a template engine to generate the HTML.

<------------------------------------>

## Example 7

```python
openFile("prog/imgs/combat_images/MONSTER1.gif");
openFile("prog/imgs/combat_images/FIREBALL.gif");
```

1. The coupling is between the file system or file path and the actual resources needed. For example, this may break if the images are moved.
2. I think this coupling is visible.
3. I think the file path where the images are stored can be a configuration option in the program instead being hard coded. I think this will allow changing the path.

<------------ Feedback -------------->
The coupling in this exercise is hidden. Even though it might be easy to identify, it is only due to the proximity of the function calls. If the calls were happening in different parts of the system, it would be difficult for a programmer to spot all of them and change them in tandem.

Th rest of the answer is correct.
<------------------------------------>

## Example 8

```java
class Rectangle { public int getArea() { ... } }
class Circle { public int getArea() { ... } }

class GraphicsProgram {
   ...
   private Color computeAverageColor() {
     for (Rectangle r : this.rectangles) { ... }
     for (Circle c : this.circles) { ... }
   }
}
```

1. I think the coupling here is that `GraphicProgram` has to know about `Rectangle` and `Circle`. It has to know that both shapes have the `getArea` method.
2. I think this coupling is visible

<------------ Feedback -------------->
Even though the provided answer is true, it is not the expected one.

The hidden coupling in this exercise exists between the interfaces of `Rectangle` and `Circle`. As it seems, `GraphicProgram` provides methods that are intended to work across different shapes. This hints that design decisions that affect `Rectangle` would also affect `Circle`. For example, a decision that would cause adding `getPerimeter()` to a `Rectangle`, is also likely to result in adding `getPerimeter()` to `Circle`.

One way to mak this hidden coupling visible is by introducing an interface `Shape` that would be implemented by `Rectangle` and `Circle`.
<------------------------------------>

## Example 9

```java
String[] recipeNames     = { "Fried calamari", "Spaghetti with meatballs", "Apple pie", ... };
RecipeType[] recipeTypes = {APPETIZER, ENTREE, DESSERT, ... }
```

1. I don't think I see any coupling here. Maybe if individual `recipeTypes` are defined with one of the values from `recipeNames` that would couple them however I don't see that here.

<------------ Feedback -------------->
The coupling is hidden and happens between the indexes of each array. It is expected that the `recipeNames[0]` should have the type of `recipeTypes[0]`. To remove the coupling, merge both arrays into a single array of structures.

```java
class Recipe {
  private String name;
  private RecipeType type;
  // ...
}
Recipe [] recipes = [...]
```

<------------------------------------>
