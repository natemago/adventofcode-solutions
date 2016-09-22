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

#replacements = {'e':['O','H'],'H':['HO','OH'],'O':['HH']}

def invreplace(mol, step):
  print('%d (%d)\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b'%(len(mol), step),end='')
  #print(mol)
  if mol == 'e':
    print(step)
    raise Exception(step)
  for key, repls in replacements.items():
    molecules = set()
    for replacement in repls:
      r_len = len(replacement)
      start_idx = 0
      while True:
        idx = mol.find(replacement, start_idx)
        if idx < 0:
          break
        new = mol[0:idx] + key + mol[idx + r_len:]
        molecules.add(new)
        start_idx = idx+1
    molecules = sorted(molecules)
    for m in molecules:
      invreplace(m, step + 1)

invreplace(molecule, 0)

# this runs on pure christmas luck. The algorithm breaks on the first path found
# and it turns out to be the right answer.






