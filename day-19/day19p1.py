#!/usr/bin/python3

import re
import hashlib

replacements = {}
molecule = ''

with open('input') as f:
  for line in f:
    if not line.strip():
      continue
    m = re.match('(?P<orig>\w+) => (?P<rep>\w+)',line.strip())
    if m:
      orig = m.group('orig')
      rep = m.group('rep')
      if not replacements.get(orig):
        replacements[orig] = []
      replacements[orig].append(rep)
    else:
      molecule += line.strip()
print(replacements)
print(molecule)

molecules = set()

for key, repls in replacements.items():
  print(key)
  l = len(key)
  for r in repls:
    print(' >', r)
    start_index = 0
    while True:
      index = molecule.find(key, start_index)
      #print(start_index, index)
      if index == -1:
        break
      generated = molecule[0:index] + r + molecule[index+l:]
      molecules.add(hashlib.md5(generated.encode('utf-8')).digest())
      start_index = index+1
print(len(molecules))
