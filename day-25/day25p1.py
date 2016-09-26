#!/usr/bin/python3

def fn(prev):
  return (prev*252533)%33554393


def code_at(row, col):
  diag = [20151125]
  i = 1
  diag_number = row + col - 2
  while True:
    next = [fn(diag[-1])] # last from the top + 1
    for d in diag:
      next.append(fn(next[-1]))
    diag = next
    if i == diag_number:
      break
    i += 1
  return diag[col-1]

print('=======================')
print('Code at row 4, col 5 should be 10600672 - actual: ', code_at(4,5))
print('Code at row 2947, col 3029 is', code_at(2947,3029))
