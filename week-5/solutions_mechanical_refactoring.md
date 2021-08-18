Algebraically Refactoring a Weak API

1) Imagine a program which takes a ToDoItem and sets all its attributes. What will happen if an attribute gets renamed, e.g.: "colour" to "color"?

A: It will set the non-existent field "colour"; the rest of the program will continue using the unchanged "color" field.

2) Consider the external view of a ToDoItem, i.e.: define the state of a ToDoItem as the constructor followed by a sequence of calls to updateItem. How does this violate the Representable/Valid principle?

A: Depending on your perspective, adding calls to updateItem for a nonexistent attribute either represent an invalid ToDoItem, or represents the same ToDoItem as without that call. Also, no enforcement that the values of updateItem are valid for that attribute.

3) Write down the type of this function (i.e.: the sets of valid inputs and outputs) using the notation from lecture. Change it using algebraic laws to an equivalent type which helps avoid the problems raised in the earlier parts of this question. Update the code accordingly.

A:

updateItem :: (S("dueDate")*Date + S("description")*String + S("status")*Status + S("colour")*Color + S("isPublic") * bool) -> unit
                ===
              (S("dueDate")*Date->unit) * ... * (S("isPublic")*bool->unit)
                ===
              (Date->Unit) * ... * (bool -> unit)


Updated code:

class ToDoItem:
  ...
  def setDueDate(date)
  ...
  def setIsPublic(isPublic)


Mechanically Refactoring a Weak API

1. Suppose you wanted to write another function which printed the graphical settings associated with each mode. How would you reuse this code to do so?

A:

Cannot (except maybe by redefining setColorDepth/drawRect)

------ More on that last idea:  There's actually a legitimate technique in FP folklore similar to this, overriding the core operators. Simon Peyton-Jones and friends used it to extract the dependencies of build tasks ( https://www.youtube.com/watch?v=BQVT6wiwCxM ). I used it at Apptimize for a similar purpose: getting a list of images to pre-fetch.

2. Suppose someone who hadn't read this code and didn't speak English saw the "mode" argument being passed in. What information would this argument convey to them?

A: Nothing, save that it's a string and related to other things named "mode"

3. Refactor the function to replace the "mode" argument with something more semantically meaningful. Doing so should also eliminate the conditional.

A:

enum Config {
  SMALL(8, 1024, 768),
  MEDIUM(16, 1600, 1200);

  private int colorDepth;
  private int width;
  private int height;
}


public void displayGame(Config cfg) {
  setColorDepth(cfg.getColorDepth());
  drawRect(screen, cfg.getWidth(), cfg.getHeight());
}


4) Show how to do this refactoring through a sequence of mechanical steps, as in lecture.

A: 

We start from this code:

public void displayGame(String mode) {
  if (mode.equals("small")) {
        setColorDepth(8);
        drawRect(screen, 1024, 768);
  } else if (mode.equals("medium")) {
        setColorDepth(16);
        drawRect(screen, 1600, 1200);
  }
}

Step 1: We anti-unify the two branches into a common function. Using reverse substitution on each branch + bacward reduction of a function application, we have:


public void displayGame(String mode) {
  if (mode.equals("small")) {
      ((x,w,h) -> {
        setColorDepth(x);
        drawRect(screen, w, h);)(8,1024,768)
  } else if(mode.equals("medium"))
      ((x,w,h) -> {
        setColorDepth(x);
        drawRect(screen, w, h);)(16,1600,1200)
  }
}


(Remaining steps can be done in different orders:)

Step 2:

We hoist this common function out of the if-statement. 

For syntactic convenience, we'll treat the code as if "small" and "medium" were guaranteed to be the only two modes.

public void displayGame(String mode) {
  ((x,w,h) -> {
        setColorDepth(x);
        drawRect(screen, w, h);
  })(mode.equals("small") ? (8,1024,768) : (16,1600,1200));
}


Step 3: 

These arguments are equivalent to a tuple or named tupled object. We create a Config type

public void displayGame(String mode) {
  ((cfg) -> {
        setColorDepth(cfg.getColorDepth());
        drawRect(..., cfg.getWidth(), cfg.getHeight());
  })(mode.equals("small") ? new Config(colorDepth=8, width=1024, height=768) : new Config(colorDepth=16, width=1600, height=1200));
}

Step 4:

We Lift if statement out of function

public void displayGame(Config cfg) {
  ((cfg) -> {
        setColorDepth(cfg.colorDepth);
        drawRect(..., cfg.width, cfg.height);
  })(cfg)
}

This means that we replace all caller arguments with (mode.equals("small") ? new Config(colorDepth=8, width=1024, height=768) : Config(colorDepth=16, width=1600, height=1200)))

All callers, either the mode is known and this conditional collapses into a single fixed Config, or we continue moving the conditional backwards up until the point where mode is chosen, resulting in having a structured Config object instead of string values.

Step 5: Inline

public void displayGame(Config cfg) {
        setColorDepth(cfg.getColorDepth());
        drawRect(..., cfg.getWidth(), cfg.getHeight());
}


Q: Why doesn't defunctionalization help here?

A: Actually, the original example is already defunctionalized. The refunctionalized form would have separate displayGameSmall and displayGameMedium versions, and use dynamic dispatch to call the appropriate one. The code actually does the same thing in both branches, but with different values. So, we need to factor out a single common function, whereas defunctionalization/refunctionalization is always for multiple distinct operations, rather than the same operation with different values.
