#!/usr/bin/python3

#!/usr/bin/python3

import re


def is_nice(s):
  if not re.search(r'(..).*\1', s):
    return False
  
  return re.search(r'(.)\w\1',s) is not None

nice_count = 0


with open('input') as f:
  line = f.readline()
  while(line):
    if is_nice(line.strip()):
      nice_count += 1
      print(line)
    line = f.readline()

print(nice_count)    