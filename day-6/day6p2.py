#!/usr/bin/python3

import re


class LightsGrid:
  
  def __init__(self, rows, cols):
    self.grid = self._generate_grid(rows, cols)
  
  
  def _generate_grid(self, rows, cols):
    grid = []
    for i in range(0, rows):
      grid.append([0 for x in range(0, cols)])
    return grid
  
  def turn_on(self, start, end):
    for i in range(start[0], end[0]+1):
      for j in range(start[1], end[1]+1):
        self.grid[i][j] += 1
  
  def turn_off(self, start, end):
    for i in range(start[0], end[0]+1):
      for j in range(start[1], end[1]+1):
        self.grid[i][j] -= 1
        if self.grid[i][j] < 0:
          self.grid[i][j] = 0
   
  def toggle(self, start, end):
    for i in range(start[0], end[0]+1):
      for j in range(start[1], end[1]+1):
        self.grid[i][j] += 2
    
  def total_on(self):
    t = [sum(row) for row in self.grid]
    return sum(t)
   

grid = LightsGrid(1000, 1000)

with open('input') as f:
  line = f.readline()
  while(line):
    m = re.match('(?P<cmd>\w+\s*[^\d]*)\s(?P<start>\d+,\d+).*\s(?P<end>\d+,\d+)', line)
    cmd = m.group('cmd').strip()
    start = m.group('start')
    end = m.group('end')
    start = [int(s) for s in start.split(',')]
    end = [int(s) for s in end.split(',')]
    
    if cmd == 'turn on':
      grid.turn_on(start, end)
    elif cmd == 'turn off':
      grid.turn_off(start, end)
    else:
      grid.toggle(start, end)
    
    line = f.readline()

  
  
print(grid.total_on())
  
  
  
  