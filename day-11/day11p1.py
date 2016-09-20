#!/usr/bin/python3

import re

def lowest(chrs, s):
  lowest = None
  for c in chrs:
    i = s.find(c)
    if i >= 0:
      if lowest is None:
        lowest = i
      elif i < lowest:
        lowest = i
  return lowest

def replace(s, rep, frst, ind):
  r = ''
  for i in range(0, len(s)):
    if i == ind:
      r+=frst
    elif i > ind:
      r += rep
    else:
      r+=s[i]
  return r

def check_increasing(s):
  if len(s) < 3:
    return False
  for i in range(0, len(s) - 3):
    c1 = ord(s[i])
    c2 = ord(s[i+1])
    c3 = ord(s[i+2])
    if ((c3 - c2) == 1) and ((c2 - c1) == 1):
      return True
  return False
    
    


def inc(passwd):
  iol = lowest('iol', passwd)
  if iol is not None:
    passwd = replace(passwd, 'a', chr(ord(passwd[iol]) +1), iol)
    return passwd
    
  l = len(passwd)-1
  last = l
  carry = 0
  incremented = ''
  while l >= 0:
    c = passwd[l]
    if l == last:
      c = chr(ord(c) + 1)
    c = chr(ord(c) + carry)
    if c > 'z':
      c = 'a'
      carry = 1
    else:
      carry = 0
    incremented += c
    l -= 1
  return incremented[::-1]
  
def is_valid(passwd):
  if lowest('iol', passwd) is not None:
    return False
  if not re.match(r'(.)\1', passwd):
    return False
  return check_increasing(passwd)
  

passwd = 'hepxcrrq'


print(inc('pajotoiaater'))
cnt = 0
while True:
  passwd = inc(passwd)
  if is_valid(passwd):
    break
  cnt += 1
  if cnt%10000 == 0:
    print('   nope until -> %s' % passwd)

print(passwd)