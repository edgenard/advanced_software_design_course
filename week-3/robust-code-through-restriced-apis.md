# Robust Code Through Restricted APIS

## Exercise 1

1. Suppose you are writing code that needs to turn the laundry machine on by calling the run method. There are at least four ways to accidentally call the run method incorrectly. (This is just counting single calls to run, not counting errors like calling run on a running machine.) What are they, and how would you prevent misuse?

   I've found 2 kinds of ways that `run` could be called incorrectly.

   The first by calling it with parameters in the wrong order, especially `time` and `temperature`. For example, if the caller writes something like `run(75, 90, 1)` they could have meant it to be run for 90 minutes at 75 degrees instead it's going to be run for 75 minutes at 90 degrees.

   The second kind of way to call `run` with invalid integers. Examples of this include, negative integers, integers that are too large(300 for temperature), 0 for any of the parameters(though this might work for mode), an integer for the `mode` that doesn't represent an actual mode.The value for mode is especially prone to errors since there seem to only be three valid integers that a mode can be repsented with, however the `run` method with accept any integer to represent mode.

   I haven't been able to think of the two other ways the run method can be.

2. In the first design, LaundryDisplay contains its own copy of the list of WashingMachine’s. How would you enforce that it can only access whether a laundry machine is on?

   If `LaundryDisplay` has it's own copy of the `WashingMachine` list, I don't think there is a way to programmatically enforce that it can only access whether or not a laundry machine is on. I think it can discouraged. I would discourage it by making the list private and creating a new type `WashingMachineState` that has a property, `on`, that is an `enum` with values `ON` and `OFF` and a property to identify the washing machine(`id` or `name`).

   ```java
      enum WashingState {
         ON,
         OFF
      }
      public class WashingMachineState {
         public WashingState state();
         public int id();
      }

      public class LaundryDisplay {
         private final List<WashingMachine> washers;
         public final List<WashingMachineState> washerState;
      }
   ```
   Again I don't think this programmatically enforces anything but hopefully communicates to the user of `LaundryDisplay` how it is intended to be used.

3. In the second design, LaundryDisplay has a reference to the Laundromat, but not to the WashingMachine’s. How would you enforce that it can only access whether a laundry machine is on?

   In this instance we might have more of an ability to make sure that `LaundryDisplay` only has access to whether or not a `WashingMachine` is on. The `WashingMachine` list is already private in `Laundromat`. If `Laundromat` exposes a list of `WashingMachineState` then `LaundryDisplay` will only be able to have access to public properties of `WashingMachineState`.

   ```java
      public class Laundromat {
         private final List<WashingMachine> washers;
         public final List<WashingMachineState> washerStates;
      }
   ```


