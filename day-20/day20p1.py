#!/usr/bin/python3

import math

def divisors(n):
  divs = set()
  for i in range(2,math.floor(math.sqrt(n))):
    if n%i == 0:
      divs.add(i)
      divs.add(n/i)
  divs.add(1)
  divs.add(n)
  return divs

n = 1

while True:
  if sum(divisors(n))*10 == 33100000:
    print(n)
    break
  if n%1000 == 0:
    print('not',n)
  n += 1