1.

a) The run method, as defined currently, risks being misused. How, and how would you prevent misuse?

A: Times and temperatures can be negative; mode can be an invalid value. And the arguments may be given out of order.

Option 1: Distinct types for all parameters; each type restricts values.

enum Mode {
LOW, MEDIUM, HIGH
}

public void run(Time time, Temperature temp, Mode mode)

Can call it like so:

run(Time.min(60), Temp.f(110), Mode.MEDIUM);

Option 2 (for order problem): Keyword arguments, or some simulacrum (e.g.: argument structure with the builder pattern)

class LaundryRunConfig {
private final Time time;
private final Temperature temp;
private final Mode mode;
}

b) The website should not be able to control the washing machines, nor access internal details about the state of the washer. We want to enforce this programmatically.

b.1) In the first design, LaundryDisplay has a direct reference to the list of WashingMachine's. How would you enforce that it can only access whether a laundry machine is on?

A:

Option 1:

public class WashingMachine implements CheckableWashingMachine {
...
public boolean isOn() { .... }
}

interface CheckableWashingMachine { public boolean isOn(...) { ... } }

// LaundryDisplay just has a list of CheckableWashingMachine

Option 2:

public class WashingMachine {
...

    public class IsOnChecker {
        public boolean isOn() {
            return WashingMachine.this.isOn();
        }
    }

    public IsOnChecker getIsOnChecker() {
        return new IsOnChecker();
    }

    public boolean isOn() { .... }

}

// LaundryDisplay has a list of IsOnChecker's

b.2): In the second design, LaundryDisplay has a reference to the {\tt Laundromat}, but not to the WashingMachine's. How would you enforce that it can only access whether a laundry machine is on?

A:

public class Laundromat {
public boolean isWashingMachineOn(int i) {
return washingMachines.get(i).isOn();
}
}

2. Tic-tac-toe challenge

```JAVA
enum GameResult {
  PLAYER_X,
  PLAYER_O,
  DRAW
}

class BoardCoordinates {
    // Enforced within range
    private int x;
    private int Y;
    public Position(int x, int y) {}
    // getters
}

// Game is sum type of StartingGame | InProgressGame | FinishedGame
// Use instanceof to distinguish them
interface Game {}
interface StartedGame extends Game {
    public UnfinishedGame takeMoveBack() {}
    public boolean isPositionOccupied(BoardCoordinates coordinates) {}
}
interface UnfinishedGame extends Game {
    public StartedGame move(BoardCoordinates coordinates) {}
}

class StartingGame implements UnfinishedGame {
    // Representation elided
}
class InProgressGame implements UnfinishedGame, StartedGame {
    // Representation elided
}
class FinishedGame implements StartedGame {
    // Representation elided
    public GameResult whoWonOrDraw() {}
}
```

Extra challenge 1 (dynamic language): Same, but without the checking

Extra challenge 2 (cannot make an invalid move):

Option 1: Generate distinct types for every board position, and distinct methods for every place.

Option 2: Use type parameters to give distinct types for every board position. E.g.:

public abstract class CS {} // CS = "CellState"
public final class O extends CellState {}
public final class X extends CellState {}
public final class E extends CellState {}

public class Board<P00 extends CS, P01 extends CS, P02 extends CS, P10 extends CS, P11 extends CS, P12 extends CS, P20 extends CS, P21 extends CS, P22 extends CS> {
public static <P01 extends CS, ... , P22 extends CS Board<O, P01, P02, ..., P22> void playOInP00(Board<E, P01, ..., P22>) { ... }
// ...
}

Haskell version:

{-# LANGUAGE DataKinds #-}
data CellState = E | O | X

-- The type variables are all phantom types
data Board (a :: CellState) (b :: CellState) <etc> (i :: CellState) = Board <list of cells>

isCell11Empty :: Board a b c d e f g h i -> Maybe (Board E b c d e f g h i)
isCell12Empty :: Board a b c d e f g h i -> Maybe (Board a E c d e f g h i)
<...>

placeOInCell11 :: Board E b c d e f g h i -> Board O b c d e f g h i
placeXInCell11 :: Board E b c d e f g h i -> Board X b c d e f g h i
placeOInCell12 :: Board a E c d e f g h i -> Board a O c d e f g h i
placeXInCell12 :: Board a E c d e f g h i -> Board a X c d e f g h i
<...>
