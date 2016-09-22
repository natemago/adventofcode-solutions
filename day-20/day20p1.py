#!/usr/bin/python3

def divisors(n):
  divs = [1]
  for i in range(2,n):
    if n%i == 0:
      divs.append(i)
  return divs + [n]


n = 1

while True:
  if sum(divisors(n))*10 == 33100000:
    print(n)
    break
  if n%1000 == 0:
    print('not',n)
  n += 1