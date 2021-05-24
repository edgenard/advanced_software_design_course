# KWIC Refactoring drill

## Dataflow patterns

1. There are two pieces of code that compute the word associated with a circular shift. Find them.

  The `csword`(inside of `alphabetize`) and `csline`(inside of `print_all_alph_cs_lines`) compute the word associated with the circular shift

2. These two snippets of code have the same dataflow graph. What is it? Draw it if you can.

  I used MermaidJs to try and draw the graph. I think this is what the  dataflow looks like this. It ends on `shiftedWord`

[![dataflow for circular shift](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBsaW5lcyBcbiAgICB3b3JkX25vXG4gICAgc2hpZnQgLS0-IFNwbGl0KChkZXN0cnVjdHVyZSkpXG4gICAgU3BsaXQgLS0-IGxpbmVfbm9cbiAgICBTcGxpdCAtLT4gZmlyc3Rfd29yZF9ub1xuICAgIGZpcnN0X3dvcmRfbm8gLS0-ICsoKCspKVxuICAgIHdvcmRfbm8gLS0-ICsoKCspKVxuICAgICsoKCspKSAtLT4gbW9kKCglKSlcbiAgICBsaW5lcyAtLT4gaW5kZXhPZkxpbmVcbiAgICBsaW5lX25vIC0tPiBpbmRleE9mTGluZVxuICAgIGluZGV4T2ZMaW5lIC0tPiBsaW5lXG4gICAgbGluZSAtLT4gbGVuKChsZW4pKVxuICAgIGxlbiAtLT4gbW9kXG4gICAgbW9kIC0tPiBzaGlmdEluZGV4XG4gICAgbGluZXMgLS0-IGxpbmVfbm9cbiAgICBzaGlmdEluZGV4IC0tPiBsaW5lXG4gICAgbGluZSAtLT4gc2hpZnRlZFdvcmRcbiAgICBcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBsaW5lcyBcbiAgICB3b3JkX25vXG4gICAgc2hpZnQgLS0-IFNwbGl0KChkZXN0cnVjdHVyZSkpXG4gICAgU3BsaXQgLS0-IGxpbmVfbm9cbiAgICBTcGxpdCAtLT4gZmlyc3Rfd29yZF9ub1xuICAgIGZpcnN0X3dvcmRfbm8gLS0-ICsoKCspKVxuICAgIHdvcmRfbm8gLS0-ICsoKCspKVxuICAgICsoKCspKSAtLT4gbW9kKCglKSlcbiAgICBsaW5lcyAtLT4gaW5kZXhPZkxpbmVcbiAgICBsaW5lX25vIC0tPiBpbmRleE9mTGluZVxuICAgIGluZGV4T2ZMaW5lIC0tPiBsaW5lXG4gICAgbGluZSAtLT4gbGVuKChsZW4pKVxuICAgIGxlbiAtLT4gbW9kXG4gICAgbW9kIC0tPiBzaGlmdEluZGV4XG4gICAgbGluZXMgLS0-IGxpbmVfbm9cbiAgICBzaGlmdEluZGV4IC0tPiBsaW5lXG4gICAgbGluZSAtLT4gc2hpZnRlZFdvcmRcbiAgICBcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)



3. How would you go about finding code in other programs that follows the circular-shift pattern? I.e.: what would you look for when skimming the code? You can't use the dataflow graph directly, but you can be inspired by it.

I would look for the modulo operation that where the divisor is the lenght of the list and the dividend is the sum of indices of the first index and the index of the word whose circular shift we are looking for.



