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



def invreplace(mol, step):
  print('%d (%d) \b\b\b\b\b\b\b\b\b\b\b\b\b'%(len(mol), step), end='')
  if mol == 'e':
    print(step)
  for key, repls in replacements.items():
    repls.sort(key=lambda x: len(x))
    repls.reverse()
    for replacement in repls:
      r_len = len(replacement)
      start_idx = 0
      while True:
        idx = mol.find(replacement, start_idx)
        if idx < 0:
          break
        new = mol[0:idx] + key + mol[idx + r_len:]
        #if len(new) < 30:
        #  print(new , '%s with %s'%( replacement, key)) 
        invreplace(new, step + 1)
        start_idx = idx+1

invreplace(molecule, 1)








