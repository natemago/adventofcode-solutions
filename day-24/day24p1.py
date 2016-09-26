from queue import Queue

from random import randint
from functools import reduce

weights = []

with open('input') as f:
  for line in f:
    weights.append(int(line.strip()))

TOTAL = sum(weights)

group_weight = TOTAL/3
print('Number of packages: ', len(weights))
print('Weight per group is: ', group_weight)


from itertools import combinations

def traverse_space_bfs(weights):
  total = sum(weights)
  third = total/3
  
  mQE = None
  mL = None
  
  for i in range(2, len(weights)):
    for comb in combinations(weights, i):
      if mL and len(comb) > mL:
        continue
      if sum(comb) == third:
        if sum_exists([x for x in weights if x not in comb], third):
          if mL is None or mL > len(comb):
            QE = reduce(lambda a,b: a*b, comb)        
            if mQE is None or QE < mQE:
              print(QE, len(comb), comb)
              mQE = QE
              mL = len(comb)
  return mQE, mL

def sum_exists(weights, the_sum):
  for i in range(2, len(weights)):
    for comb in combinations(weights, i):
      if sum(comb) == the_sum:
        return sum([x for x in weights if x not in comb]) == the_sum
  return False
        

print(traverse_space_bfs(weights))
  
