####################################################################
# INPUT MODULE
#%%
import copy
import functools

class Line():
  def __init__(self, line: list):
    self.line = line

  def word_at(self, index: int):
    return self.line[index]

  def word_count(self):
    return len(self.line)

class LineStorage():

  def __init__(self, line_list: list):
    self.line_list = self.__store_lines(line_list)
    self.index = 0

  def __store_lines(self, line_list):
    return list(map(lambda line: Line(line), line_list))


  def word_at(self, line_index: int, word_index: int):
    return self.line_list[line_index].word_at(word_index)

  def line(self, index: int):
    return self.line_list[index]

  def lines_count(self):
    return len(self.line_list)

  def words_in_line_count(self, line_index: int):
    return self.line_list[index].word_count()

  def __iter__(self):
    return self

  def __next__(self):
    try:
      current_line = self.line(self.index)
      self.index += 1
      return current_line

    except IndexError:
      self.index = 0
      raise StopIteration

class CircularShift():

  def __init__(self, line_storage: LineStorage):
    self.line_storage = line_storage
    self.circ_index = self.setup() # Returns shifts as pairs
    self.index = 0
    self.circular_shifts = self.store_circ_shifts()
    super().__init__()

  def setup(self):
    circ_index = []
    for lineno in range(line_storage.lines_count()):
      line = line_storage.line(lineno)
      for wordno in range(line.word_count()):
          circ_index.append( (lineno, wordno) )
    return circ_index

  def __iter__(self):
    return self

  def __next__(self):
    try:
      shift = self.circ_index[self.index]
      self.index += 1
      return shift
    except IndexError:
      self.index = 0
      raise StopIteration

  def store_circ_shifts(self):
    circ_shifts = []
    for shift in self.circ_index:
      (line_idx, first_word_no) = shift
      line = self.line_storage.line(line_idx)
      word_count = line.word_count()
      for idx_of_curr_word in range(word_count):
        shifted_index = ((idx_of_curr_word + first_word_no) % word_count)
        circular_shift = (line_idx, idx_of_curr_word, line.word_at(shifted_index))
        circ_shifts.append(circular_shift)
    return circ_shifts

  def circ_shift_at(self, line: Line, word_idx: int):
    pass

class AlphIndex():
  def __init__(self, circularShift: CircularShift, line_storage: LineStorage):
    self.circularShift = circularShift
    self.line_storage = line_storage
    self.alph_index = self.alphabetize()
    self.index = 0

  def alphabetize(self):
    pass

  def __iter__(self):
    return self

  def __next__(self):
    try:
      shift = self.alph_index[self.index]
      self.index += 1
      return shift
    except IndexError:
      self.index = 0
      raise StopIteration

# List of list of words

line_storage = None
def putfile(linelist):
    global line_storage
    line_storage = LineStorage(copy.copy(linelist))

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

    circ_index = CircularShift(line_storage)

######################################################################
## ALPHABETIZING MODULE

alph_index = None

def alphabetize():
    global alph_index, line_storage, circ_index
    def compare_circ_shift_for_line(loc_line_and_word1, loc_line_and_word2):
      # print('Inside cmp_csline', shift1, shift2)
      def circ_shifted_word(shift, index_of_curr_word_in_line, lines):
        (line_index, first_word_index) = shift
        line = lines.line(line_index)
        shifted_word_index = (first_word_index + index_of_curr_word_in_line) % line.word_count()
        return line.word_at(shifted_word_index)

      def cswords(shift, lines):
        return lines.line(shift[0]).word_count()

      def cmp(num1, num2):
        return (num1>num2)-(num1<num2)

      lines = line_storage

      number_of_words1 = cswords(loc_line_and_word1, lines)
      # print(f'# of words in line {shift1[0]}: {nwords1} ')
      number_of_words2 = cswords(loc_line_and_word2, lines)
      # print(f'# of words in line {shift2[0]}: {nwords2} ')
      last_index = min(number_of_words1, number_of_words2)

      for index_of_curr_word_in_line in range(last_index+1):
        shifted_word1 = circ_shifted_word(loc_line_and_word1, index_of_curr_word_in_line, lines)
        shifted_word2 = circ_shifted_word(loc_line_and_word2, index_of_curr_word_in_line, lines)
        # print(f'circular shift word {cword1}, {cword2}')

        if shifted_word1 != shifted_word2:
          # print(f'when the words do not match result of {cmp(cword1, cword2)}')
          return cmp(shifted_word1, shifted_word2)

      return cmp(number_of_words1, number_of_words2)

    alph_index = sorted(circ_index, key=functools.cmp_to_key(compare_circ_shift_for_line))

######################################################################
## OUTPUT MODULE

def print_all_alph_cs_lines():
    global alph_index, line_storage
    def csline(shift, lines):
        (lno, first_word_no) = shift
        wrd_cnt = lines.line(lno).word_count()
        # print(f'Shift {shift}')
        # print(f' word count {wrd_cnt}')
        # print(f'{ [lines[lno][(0+first_word_no) % wrd_cnt]] }')
        return [lines.word_at(lno,((idx_of_curr_word + first_word_no) % wrd_cnt)) for idx_of_curr_word in range(wrd_cnt)]

    shifted_lines = []
    for shift in alph_index:
        shifted_lines.append((csline(shift, line_storage)))
        print (csline(shift, line_storage))
    return shifted_lines


## MASTER CONTROL
# putfile([["a", "b", "c", "d"],
#          ["one"],
#          ["hey", "this", "is", "different"],
#          ["a", "b", "c", "d"]])


putfile([["a", "b", "c", "d"],
         ["one"],
         ["hey", "this", "is", "different"]])
cs_setup()
alphabetize()
print_all_alph_cs_lines()
print(circ_index.circular_shifts)

import unittest

class KwicTest(unittest.TestCase):

  def setUp(self):
    putfile([["a", "b", "c", "d"],
         ["one"],
         ["hey", "this", "is", "different"]])
    cs_setup()
    alphabetize()

  def test_result_stays_the_same(self):
    expectation = [
      ['a', 'b', 'c', 'd'],
      ['b', 'c', 'd', 'a'],
      ['c', 'd', 'a', 'b'],
      ['d', 'a', 'b', 'c'],
      ['different', 'hey', 'this', 'is'],
      ['hey', 'this', 'is', 'different'],
      ['is', 'different', 'hey', 'this'],
      ['one'],
      ['this', 'is', 'different', 'hey']
      ]
    self.assertEqual(expectation, print_all_alph_cs_lines())



#%%