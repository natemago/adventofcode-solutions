#!/usr/bin/python3


import re
from functools import reduce


def mixture(mixtures, parts, on_mixture):
  if len(parts) == 1:
    on_mixture(mixtures + parts)
  else:
    total = sum(parts)
    for i in range(0, total-len(parts)+1):
      p = parts[1:]
      for j in range(0, len(p)):
        if (p[j] - i) > 0:
          p[j] -= i
      mixture(mixtures + [parts[0] + i], p, on_mixture)

ingredients = {}

with open('input')  as f:
  for line in f:
    m = re.match('(?P<ingr>\w+): capacity (?P<cap>-?\d+), durability (?P<dur>-?\d+), flavor (?P<flav>-?\d+), texture (?P<tex>-?\d+), calories (?P<cal>-?\d+)',line)
    name = m.group('ingr')
    values = [int(m.group('cap')),
              int(m.group('dur')),
              int(m.group('flav')),
              int(m.group('tex')),
              int(m.group('cal'))]
    ingredients[name] = values
    


print(ingredients)

ing_vals = []

for name, vals in ingredients.items():
  ing_vals.append([name] + vals)


def calc_score(recipe, ingredients):
  
  used_ingr = [i[1:-1] for i in ingredients]
  
  score = 1
  
  for i in range(0, len(used_ingr[0])):
    partial = 0
    
    for j in range(0, len(recipe)):
      partial += recipe[j] * used_ingr[j][i]
    if partial < 0:
      partial = 0
    
    score *= partial
  
  return (score, sum([ recipe[i]*ingredients[i][-1] for i in range(0, len(recipe)) ]))

count = 0
mixture_max = None
mixture_max_with_500_cal = None

def on_mixture(recipe):
  global mixture_max
  global mixture_max_with_500_cal
  global count
  count += 1
  score, calories = calc_score(recipe, ing_vals)
  if score:
    if mixture_max is None:
      mixture_max = (score, recipe)
    else:
      olds, r = mixture_max
      if olds < score:
        mixture_max = (score, recipe)
    
    if calories == 500:
      if mixture_max_with_500_cal is None or mixture_max_with_500_cal[0] < score:
        mixture_max_with_500_cal = (score, recipe)



total = 100

init_mixture = []

for i in range(0, len(ingredients)-1):
  init_mixture.append(1)
init_mixture.append(total - len(ingredients) + 1)

mixture([], init_mixture, on_mixture)
print('Best cookie mixture: ',mixture_max)
print('With exactly 500 cal: ', mixture_max_with_500_cal)

