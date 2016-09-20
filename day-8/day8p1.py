#!/usr/bin/python3

import re



total_in_file = 0
total_in_memory = 0

with open('input') as f:
  line = f.readline()
  while line:
    line = line.strip()
    total_in_file += len(line)
    line = line[1:-1] # remove the lead/trail double quotes
    decoded = bytes(line, 'utf-8').decode('unicode_escape')
    
    print(line)
    print(decoded)
    
    total_in_memory += len(decoded)
    line = f.readline()

print(total_in_file)
print(total_in_memory)
print(total_in_file - total_in_memory)