#!/usr/bin/python3


start = '1113122113'

def say_it(s):
  prev = None
  cnt = 0
  result = ''
  for c in s:
    if prev is not None and prev != c:
      result = result + '%d%s' % (cnt, prev)
      cnt = 0
    cnt += 1
    prev = c
  result += '%d%s' % (cnt, prev)
  return result


for i in range(0, 50):
  start = say_it(start)
  if i == 39:
    print(len(start))
print(len(start))
