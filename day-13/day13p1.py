#!/usr/bin/python3

import re

# Same as in day 9, we can check all possible sitting arrangements

def permutate(pref, arr, perms):
  if len(arr) == 0:
    perms.append(pref)
    return
  for a in arr:
    rem = [] + arr
    rem.remove(a)
    permutate(pref + [a], rem, perms)


def happiness_change(arrangement):
  arrangement = arrangement + [arrangement[0]]
  print(arrangement)
  s = 0
  for i in range(0, len(arrangement) -1):
    this = arrangement[i]
    next = arrangement[i+1]
    s += happines_values[this + '-' + next] + happines_values[next + '-' + this]
  return s


happines_values = {}
people = set()


with open('input') as f:
  line = f.readline()
  
  while line:
    line = line.strip()
    
    m = re.match('(?P<p1>\w+) would (?P<sign>\w+) (?P<value>\d+) happiness units by sitting next to (?P<p2>\w+)', line)
    person1 = m.group('p1')
    person2 = m.group('p2')
    sign = '-' if m.group('sign') == 'lose' else ''
    value = int('%s%s' % (sign, m.group('value')))
    
    happines_values[person1 + '-' + person2] = value
    people.add(person1)
    people.add(person2)
    
    
    line = f.readline()


print(len(happines_values))

arrangements = []
permutate([], [p for p in people], arrangements)
print(len(arrangements))

happines_deltas = [happiness_change(a) for a in arrangements]
print(max(happines_deltas))


