#!/usr/bin/python3

import re


PROPERTIES = ['children', 'cats', 'samoyeds', 'pomeranians', 'akitas', 'vizslas', 'goldfish', 'trees', 'cars', 'perfumes']

FILTER = {
  "children": 3,
  "cats": 7,
  "samoyeds": 2,
  "pomeranians": 3,
  "akitas": 0,
  "vizslas": 0,
  "goldfish": 5,
  "trees": 3,
  "cars": 2,
  "perfumes": 1
}

aunts = []

with open('input') as f:
  for line in f:
    line = line.strip()
    m = re.match('Sue (?P<number>\d+):', line)
    number = m.group('number')
    
    sue = { 'number': number }
    for m in re.finditer('(?P<label>\w+): (?P<value>\d+)', line):
      label = m.group('label')
      value = int(m.group('value'))
      sue[label] = value
    aunts.append(sue)

print(len(aunts))


def filter_aunt(aunt, by_prop, known):
  val = aunt.get(by_prop)
  if val is None:
    return True
  return val == known[by_prop]

def aunt_filter(by_prop):
  def __filter(aunt):
    return filter_aunt(aunt, by_prop, FILTER)
  return __filter
  
filtered = aunts

for prop in PROPERTIES:
  filtered = filter(aunt_filter(prop), filtered)

filtered = [a for a in filtered]
print(filtered)
  
if len(filtered) == 1:
  print('By processof elimination I have deduced that this must be my Aunt Sue %s.' % filtered[0]['number'])
elif len(filtered) == 0:
  print('This is not from my Aunt Sue.')
else:
  print('I still cannot determine which of these is it? ', filtered)
  
  
