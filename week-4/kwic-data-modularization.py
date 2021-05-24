####################################################################
# INPUT MODULE
#%%
import copy
import functools
from abc import ABC, abstractmethod

class LineStorage(ABC):
  @abstractmethod
  def word_at(self, index):
    pass

# List of list of words

line_storage = None
def putfile(linelist):
    global line_storage
    line_storage = copy.copy(linelist)

######################################################################
## CIRCULAR SHIFTER
#
# Make circ_index store something represetning all circular shifts
#
# Fact: For a line with K words, there are K circular shifts.
# As a result, the ith shift is the line containing the ith word in the file,
#

# Store shifts as (line, shift idx) pairs
circ_index = None

def cs_setup():
    global circ_index, line_storage

    circ_index = []
    for lineno in range(len(line_storage)):
        line = line_storage[lineno]
        for wordno in range(len(line)):
            circ_index.append( (lineno, wordno) )

######################################################################
## ALPHABETIZING MODULE

alph_index = None

def alphabetize():
    global alph_index, line_storage, circ_index
    def cmp_csline(shift1, shift2):
      # print('Inside cmp_csline', shift1, shift2)
      def csword(shift, wordno, lines):
        (lno, first_word_no) = shift
        shift_idx = (first_word_no + wordno) % len(lines[lno])
        return lines[lno][shift_idx]

      def cswords(shift, lines):
        return len(lines[shift[0]])

      def cmp(num1, num2):
        return (num1>num2)-(num1<num2)

      lines = line_storage

      nwords1 = cswords(shift1, lines)
      # print(f'# of words in line {shift1[0]}: {nwords1} ')
      nwords2 = cswords(shift2, lines)
      # print(f'# of words in line {shift2[0]}: {nwords2} ')
      lasti = min(nwords1, nwords2)

      for i in range(lasti+1):
        cword1 = csword(shift1, i, lines)
        cword2 = csword(shift2, i, lines)
        # print(f'circular shift word {cword1}, {cword2}')

        if cword1 != cword2:
          # print(f'when the words do not match result of {cmp(cword1, cword2)}')
          return cmp(cword1, cword2)

      return cmp(nwords1, nwords2)

    alph_index = sorted(circ_index, key=functools.cmp_to_key(cmp_csline))

######################################################################
## OUTPUT MODULE

def print_all_alph_cs_lines():
    global alph_index, line_storage
    def csline(shift, lines):
        (lno, first_word_no) = shift
        wrd_cnt = len(lines[lno])
        # print(f'Shift {shift}')
        # print(f' word count {wrd_cnt}')
        # print(f'{ [lines[lno][(0+first_word_no) % wrd_cnt]] }')
        return [lines[lno][(i+first_word_no) % wrd_cnt] for i in range(wrd_cnt)]

    for shift in alph_index:
        print (csline(shift, line_storage))


## MASTER CONTROL
putfile([["a", "b", "c", "d"],
         ["one"],
         ["hey", "this", "is", "different"],
         ["a", "b", "c", "d"]])
cs_setup()
alphabetize()
print_all_alph_cs_lines()
