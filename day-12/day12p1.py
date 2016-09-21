#!/usr/bin/python3

import re


with open('input') as f:
  content = f.read()


pattern = re.compile('-?\d+')

total = 0
for m in re.finditer(pattern, content):
  total += int(m.group(0))

print(total)