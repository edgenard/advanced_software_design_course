# KWIC Refactoring drill

## Dataflow patterns

1. There are two pieces of code that compute the word associated with a circular shift. Find them.

   The `csword`(inside of `alphabetize`) and `csline`(inside of `print_all_alph_cs_lines`) compute the word associated with the circular shift

<------------ Feedback -------------->
Correct
<------------------------------------>

2. These two snippets of code have the same dataflow graph. What is it? Draw it if you can.

   I used MermaidJs to try and draw the graph. I think this is what the dataflow looks like this. It ends on `shiftedWord`

[![dataflow for circular shift](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBsaW5lcyBcbiAgICB3b3JkX25vXG4gICAgc2hpZnQgLS0-IFNwbGl0KChkZXN0cnVjdHVyZSkpXG4gICAgU3BsaXQgLS0-IGxpbmVfbm9cbiAgICBTcGxpdCAtLT4gZmlyc3Rfd29yZF9ub1xuICAgIGZpcnN0X3dvcmRfbm8gLS0-ICsoKCspKVxuICAgIHdvcmRfbm8gLS0-ICsoKCspKVxuICAgICsoKCspKSAtLT4gbW9kKCglKSlcbiAgICBsaW5lcyAtLT4gaW5kZXhPZkxpbmVcbiAgICBsaW5lX25vIC0tPiBpbmRleE9mTGluZVxuICAgIGluZGV4T2ZMaW5lIC0tPiBsaW5lXG4gICAgbGluZSAtLT4gbGVuKChsZW4pKVxuICAgIGxlbiAtLT4gbW9kXG4gICAgbW9kIC0tPiBzaGlmdEluZGV4XG4gICAgbGluZXMgLS0-IGxpbmVfbm9cbiAgICBzaGlmdEluZGV4IC0tPiBsaW5lXG4gICAgbGluZSAtLT4gc2hpZnRlZFdvcmRcbiAgICBcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBsaW5lcyBcbiAgICB3b3JkX25vXG4gICAgc2hpZnQgLS0-IFNwbGl0KChkZXN0cnVjdHVyZSkpXG4gICAgU3BsaXQgLS0-IGxpbmVfbm9cbiAgICBTcGxpdCAtLT4gZmlyc3Rfd29yZF9ub1xuICAgIGZpcnN0X3dvcmRfbm8gLS0-ICsoKCspKVxuICAgIHdvcmRfbm8gLS0-ICsoKCspKVxuICAgICsoKCspKSAtLT4gbW9kKCglKSlcbiAgICBsaW5lcyAtLT4gaW5kZXhPZkxpbmVcbiAgICBsaW5lX25vIC0tPiBpbmRleE9mTGluZVxuICAgIGluZGV4T2ZMaW5lIC0tPiBsaW5lXG4gICAgbGluZSAtLT4gbGVuKChsZW4pKVxuICAgIGxlbiAtLT4gbW9kXG4gICAgbW9kIC0tPiBzaGlmdEluZGV4XG4gICAgbGluZXMgLS0-IGxpbmVfbm9cbiAgICBzaGlmdEluZGV4IC0tPiBsaW5lXG4gICAgbGluZSAtLT4gc2hpZnRlZFdvcmRcbiAgICBcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

<------------ Feedback -------------->
Good job
<------------------------------------>

3. How would you go about finding code in other programs that follows the circular-shift pattern? I.e.: what would you look for when skimming the code? You can't use the dataflow graph directly, but you can be inspired by it.

   I would look for the modulo operation where the divisor is the length of the list and the dividend is the sum of indices of the first index and the index of the word whose circular shift we are looking for. I think that is a strong signal that some kind of circular shift operations is happening.

<------------ Feedback -------------->
Good answer!
<------------------------------------>

## Data-Centric Refactoring

1. For each module of the code: What secret is it hiding? That is, what design decisions are contained in that module, where changing the design decision could not change any other module.

   I'm not sure anything is hidden here. Since `line_storage` is a global variable and doing's operations on it depend on knowing that it is an array of arrays. The `circ_index` being a array of tuples also limits the reasonable implementations of calculating and sorting the circular shift.

<------------ Feedback -------------->
This is a good insight. In truth, almost no interesting design decisions are hidden by this design, except for the sorting algorithm on the Alphabetizing module. That's not to say that the other modules have absolutely no secrets. For example, the output module hides whether the output is buffered, but the likelihood of this being a relevant design decision in a general context is low.
<------------------------------------>

2. Consider each of the following design changes. What code would need to change for each?

   1. Use of persistent storage (not in-memory) for the line storage

      `cs_setup`, `alphabetize`, and `print_all_alph_cs_lines` would need to change. They all depend on `line_storage` being an an array of arrays. `putfile` would also need to change to accomodate the persistent store.

   <------------ Feedback -------------->
   Not necessarily for the `putfile` as the given array could just be persistently stored by the LineStorage. The rest is correct.
   <------------------------------------>

   2. Using on-demand instead of up-front alphabetization. (I.e.: Using a selection algorithm instead of a sorting algorithm.)

      The `alphabetize` function would need to change.

   <------------ Feedback -------------->
   The output and master control would also have to change as they use the `alph_index ` directly, which is a plain array and thus can't support on-demand sorting.
   <------------------------------------>

   3. Storing shifts in byte-packed arrays

      `alphabetize`, `print_all_alph_cs_lines`, and `cs_setup` would need to change.

   <------------ Feedback -------------->
   Correct
   <------------------------------------>

3. Separate each of lines_storage, circ_index, alph_index into their own "module," with an abstracted accessor interface. Each should not be accessed from outside that module.

   Gist: https://gist.github.com/edgenard/b4c5361f13a2f9b42d9e6ad99fb17ea6

<------------ Feedback -------------->
Correct
<------------------------------------>

4. Refactor the code so that (1) the storage format of the input, and (2) the format of circular shifts are both now secrets. In particular, there should now be only one instance of the pattern you identified in question 2 of the previous exercise.

   I am not sure how to do this. I've linked what I came up in the gist for the answer to question 3.

<------------ Feedback -------------->
The refactoring accomplishes to turn the storage format of the input into a secret. As it is, if the LineStorage was changed to use persistent memory, only the LineStorage module would have to change, so good job on that.

The given solution doesn't do a great job of hiding the circular shift formats. `CircularShift` returns shifts as a plain tuple of `lno` and `first_word_no`, meaning that to change the storage format of shifts it's necessary to either:

1.  Change code that uses shifts
2.  Write code on `CircularShift` to convert from the new storage format to the old storage format so existing clients don't break.

One approach that would prevent this issue would be to have `CircularShift` return the word of a shifted line `def get_word(shift_idx, word_idx)` instead of returning a shift. This approach also has the added benefit of centralizing the shift pattern identified in question 2 of the previous exercise into the `CircularShift` module. In the given solution, as shifts are tuples of `lno` and `first_word_no`, clients of `CircularShift` are forced to do the circular pattern to get the desired words, which lead to repeated code between the alphabetizer and the output module.

<------------------------------------>

3.  Repeat question 1 for this refactored version.

    I'm not sure about this since I could not come up with an answer to question 4

4.  Repeat question 2 for this refactored version.

    I'm not sure about this since I could not come up with answer to question 4.'s
