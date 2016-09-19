#!/usr/bin/python3

import re


def is_nice(s):
  # should not contain ab, cd, pq or xy
  if re.search('(ab|cd|pq|xy)', s):
    return False
  
  # at least 3 DIFFERENT wowels somewhere in the string
  
  if not re.search('[aeiou].*[aeiou].*[aeiou]', s):
    return False
  
  
  return re.search(r'(.)\1', s) is not None


nice_count = 0

with open('input') as f:
  line = f.readline()
  while(line):
    if is_nice(line.strip()):
      nice_count += 1
    line = f.readline()

print(nice_count)    