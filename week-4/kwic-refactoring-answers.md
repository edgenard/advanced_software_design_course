Dataflow patterns

1. There are two pieces of code that compute the word associated with a circular shift. Find them.

A:

First (in csword): shift_idx = (fwno + wordno) % len(lines[lno])
Second (in csline): return [lines[lno][(i+fwno) % wrd_cnt] for i in range(wrd_cnt)]

2. These two snippets of code have the same dataflow graph. What is it?

A:

(fwno + i) % len(lines[x])

Prescott Murphy illustrated this: http://jameskoppelcoaching.com/ofoa1hi/

3.How would you go about finding code in other programs that follows the circular-shift pattern?

A:

Scan for modulus operators; see if they fit the (const+i)%len pattern.

Data-Centric Refactoring

1. For each module of the code: What secret is it hiding? That is, what design decisions are contained in that module, where changing the design decision could not change any module.

A:

The short answer is "nothing interesting" for all modules except for the sorting algorithm. Exact answers may vary depending on what non-interesting secrets you notice and find mention-able. It also varies depending on exactly how you imagine the spec, and what restrictions you believe all client code should follow.

Input module: None
Circular shifter: Iteration order (but not output order)
Alphabetizing module: Sorting algorithm, sort order (if rest of code is written in restricted fashion)
Output module: Whether the output is buffered. The output destination (possibly).
Master control: The input source.

2. Consider each of the following design changes. What code would need to change for each?

- Use of persistent storage (not in-memory) for the line storage
  ---- Input, CS, alphabetize, and output modules.

- Using on-demand instead of up-front alphabetization. (I.e.: Using a selection algorithm instead of a sorting algorithm.)
  ---- Alphabetize, output, and master control modules

- Storing shifts in byte-packed arrays
  ---- CS, alphabetize, and output modules.

3. Separate each of lines_storage, circ_index, alph_index into their own "module," with an abstracted accessor interface. Each should not be accessed from outside that module.

A:

Here's one possible design. Following the original, it keeps everything in the top level rather than localizing state with objects.

Input module:

def initialize(lines)
def get_line(idx)
def line_count()

Circ shifts:

# Directly depends on Input module as data source

def get_word(shift_idx, word_idx)
def word_count(shift_idx)
def shift_counts()

Alph indexes:

def alph_idx(alpha_idx)
def alph_count()

4. Refactor the code so that the format of circular shifts is now a secret. In particular, there should now be only one instance of the pattern you identified in question 2 of the previous exercise.

A:

Actually, the above modularization already suffices.

5. Repeat question 1 for this refactored version.

Input module: Hides line representation
Circ shifts: Hides shift representation, when shifts are computed
Alph indexes: Hides sorting algorithm and order, hides when alphabetization is performed
Output: Still hides buffering behavior and output destination/format
Master control: Hides input source

6. Repeat question 2 for this refactored version.

- Use of persistent storage (not in-memory) for the line storage
  --- Just line storage
- Using on-demand instead of up-front alphabetization
  --- Just alphabetization
- Storing shifts in byte-packed arrays
  --- Just the circular shifter
