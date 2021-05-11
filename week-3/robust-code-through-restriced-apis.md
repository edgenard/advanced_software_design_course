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


## Exercise 2

Design an API for a Tic-Tac-Toe board, consisting of types repre- senting states of the board, along with functions move, takeMoveBack, whoWonOrDraw, and isPositionOccupied
Note that you should not provide an AI for the game, nor an interactive interface for playing it, though either of these applications may use your API for manipulating board state.

 - All functions must be pure. If you write a function, I must be able to call it with the same arguments and always get the same results, forever.
 - All functions must return a sensible result, and may not throw exceptions
 - If I call move on a tic-tac-toe board, but the game has finished, I should get a compile-time type-error. In other words, calling move on inappropriate game states (i.e. move doesnt make sense) is disallowed by the types.
 - If I call takeMoveBack on a tic-tac-toe board, but no moves have yet been made, I get a compile-time type-error.
 - If I call whoWonOrDraw on a tic-tac-toe board, but the game hasnt yet finished, I get a compile-time type-error.
 - isPositionOccupied works for in-play and completed games.

```typescript
   const POSITIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8]
   type Position = typeof POSITIONS[number]
   // I'm not sure if this right. The idea is that Position is one of the values in POSITIONS

   type Player = 'X' | 'O'

   type Winner = Player | 'Draw'

   interface Placement {
       player: Player,
       position: Position
   }

   interface EmptyBoard {
       move(placement: Placement): InPlayBoard
   }

   interface InPlayBoard {
       lastMove: Placement
       takeMoveBack(): InPlayBoard | EmptyBoard
       isPositionOccupied(position: Position): Boolean
       move(placement: Placement): InPlayBoard | CompletedBoard
   }

   interface CompletedBoard {
       lastMove: Placement
       whoWonorDraw(): Winner
       isPositionOccupied(position: Position): Boolean
       takeMoveBack(): InPlayBoard

   }

```