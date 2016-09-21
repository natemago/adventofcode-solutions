#!/usr/bin/python3

import json


def nsum(d_cnt):
  s = 0
  if isinstance(d_cnt, dict):
    for key, child in d_cnt.items():
      if child == 'red':
        s = 0
        break
      s += nsum(child)
  elif isinstance(d_cnt, list):
    for v in d_cnt:
      s += nsum(v)
  elif isinstance(d_cnt, int):
    s += d_cnt
  
  return s


with open('input') as f:
  content = f.read()
  
d_cnt = json.loads(content)
#print(d_cnt)
print(nsum(d_cnt))