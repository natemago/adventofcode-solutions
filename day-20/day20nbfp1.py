#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

#
# From the sum-of-divisors function:
#
#               (a(i)  + 1)
#             p             
#         r    i              -  1
# σ(n) =  Π   ---------------------
#        i=1    p   -   1
#                i
#
#
#  where:
#   - n is the number
#   - r is the number of prime divisors
#   - p  is the i-th prime divisor of n
#      i
#   - a(i) is the max power of p
#
#  The sumation is expressed as a product of numbers of the following form:
#     (p^(n + 1) - 1)/(p - 1)
#  where p is prime and n is natural number.
# Since we know the sum of all divisors of N, we can then factor N into primes,
# then look for combination of d1*d2*...dk where di is of the reqired form.
# We can then reverse engineer the parameters (pi,ni) for each {d1,d2,..,dk) and 
# and reconstruct the original number as p1^n1*p2^n2*...*pk^nk .

import math

def is_prime(n):
  for i in range(2, math.floor(math.sqrt(n)) ):
    if n%i == 0:
      return False
  return True


def load_primes(pf):
  with open(pf) as f:
    return [int(p.strip()) for p in f]

# possibly the simplest combinations without repetition generator
def combinations(choice, elements, base):
  if choice == 1:
    for e in elements:
      yield base +[e]
  else:
    for i in range(0, len(elements) - choice + 1):
      yield from combinations(choice - 1, elements[i+1:], base + [elements[i]])

def factor(n, primes_list):
  factors = []
  for p in primes_list:
    while n and (n % p) == 0:
      factors.append(p)
      n /= p
  return factors



def find_form(N, primes_list):
  forms = []
  for n in range(1, 15): # 15th power
    for p in primes_list:
      val = (p**(n+1) - 1)/(p - 1)
      if val == N:
        forms.append( (p,n) )
      elif val > N or p > N:
        break
  
  return forms if len(forms) else None
      



PRIMES = load_primes('primes')


# First let's factor the number
N = 33100000/10 # we divide by 10 because each elf carries 10 presents

N = 120

N_factors = factor(N, PRIMES)
print(N, 'prime factors ->',N_factors)
  
all_combinations = {(n,) for n in N_factors}

for i in range(1, len(N_factors)):
  for comb in combinations(i, N_factors, []):
    all_combinations.add(tuple(sorted(comb)))



print('All representations:\n ','\n  '.join(map(lambda c: str(c), all_combinations)))
print('In total: ',len(all_combinations))


from functools import reduce

print('Looking for numbers of form: (p^(n+1) - 1)/(p - 1)')
of_form = []
for comb in all_combinations:
  #print(comb)
  NN = reduce(lambda a,b: a*b, comb)
  result = find_form(NN,PRIMES)
  if result:
    for form in result:
      p,n = form
      of_form.append((p,n,NN, comb))

print('Found these: \n ', '\n  '.join(map(lambda c: str(c), of_form)))
print(len(of_form))


possible = []
print()
print('Checking all combinations...')
for i in range(2, len(of_form)):
  print(i,'of',len(of_form))
  for comb in combinations(i, of_form,[]):
    #print(comb)
    val = reduce(lambda a,c: a*c[2], comb, 1)
    if val == N:
      possible.append(comb)

print('\nThese are the possible combinations:\n ','\n  '.join(map(lambda c: str(c),possible)))
print('Now let\'s reconstruct the number. Should be the minimum of the possile')

reconstructed = [ reduce(lambda a, c: a*c[0]**c[1], comb, 1) for comb in possible  ]

print('Reconstructed numbers are: ',reconstructed)
print('The smallest is:',min(reconstructed))
