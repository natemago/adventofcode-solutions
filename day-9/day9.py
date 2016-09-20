#!/usr/bin/python3


# This is a traveling salesman problem and can be solved with more sphisticated
# algorithm, but since the input is quite small (8 nodes), this code will test
# all possible combinations (8! = 40320).
# For a more sphisticated alg. refer to https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm


import re


def permutate(pref, arr, perms):
  if len(arr) == 0:
    perms.append(pref)
    return
  for a in arr:
    rem = [] + arr
    rem.remove(a)
    permutate(pref + [a], rem, perms)


def distance(path, distances):
  d = 0
  for i in range(0, len(path)-1):
    this = path[i]
    next = path[i+1]
    d += distances[this + '-' + next]
  return d



towns = set()
distances = {}


with open('input') as f:
  line = f.readline()
  while line:
    line = line.strip()
    
    m = re.match('(?P<from>\w+) to (?P<to>\w+) = (?P<dist>\w+)', line)
    
    fr = m.group('from')
    to = m.group('to')
    dist = int(m.group('dist'))
    
    towns.add(fr)
    towns.add(to)
    distances[fr+'-'+to] = dist
    distances[to+'-'+fr] = dist
    
    line = f.readline()

all_paths = []
all_towns = [t for t in towns]

permutate([], all_towns, all_paths)

all_distances = [distance(p, distances) for p in all_paths]


print('Min: ', min(all_distances))
print('Max: ', max(all_distances))

