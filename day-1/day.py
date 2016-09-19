#!/usr/bin/python3

with open('input') as f:
  tape = f.read()

total = len(tape)
up = len(tape.replace(')', ''))

print(2*up - total)

floor = 0
position = 0
for c in tape:
  position += 1
  if c is '(':
    floor += 1
  else:
    floor -= 1
  
  if floor < 0:
    print(position)
    break