#!/usr/bin/python3

#!/usr/bin/python3

import re



old = 0
new = 0

with open('input') as f:
  line = f.readline()
  while line:
    line = line.strip()
    nl = ""
    for c in line:
      if c == '\\':
        nl += '\\\\'
      elif c == '"':
        nl += '\\"'
      else:
        nl += c
    
    nl = '"%s"' % nl
    
    print(line)
    print(nl)
    old += len(line)
    new += len(nl)
    
    line = f.readline()

print(old)
print(new)
print(new - old)