#!/usr/bin/python3

containers = []

with open('input') as f:
  containers = [int(line.strip()) for line in f ]

# possibly the simplest combinations without repetition generator
def combinations(choice, elements, base):
  if choice == 1:
    for e in elements:
      yield base +[e]
  else:
    for i in range(0, len(elements) - choice + 1):
      yield from combinations(choice - 1, elements[i+1:], base + [elements[i]])


#combinations(5, [i for i in range(0,20)],[])

count = 0 # part 1
min_i = None # part 2
min_count = 0 # part 2 
for i in range(2, len(containers)):
  print(i)
  for combination in combinations(i, containers, []):
    if sum(combination) == 150:
      count += 1
      if min_i is None:
        min_i = i
      if min_i == i:
        min_count += 1
        
print('Max number of ways:', count)
print('Min number of containers is', min_i)
print('Number of ways for minimal containers: ', min_count)
