#!/usr/bin/python3

class LightsGrid:
  def __init__(self):
    self.lights = []
  
  def add_row(self, conf):
    self.lights.append([0] + [1 if c == '#' else 0 for c in conf] + [0])
  
  def end_conf(self):
    off_row = [0 for i in range(0, len(self.lights[0]))]
    self.lights = [off_row] + self.lights + [off_row]
    self.lights[1][1] = 1
    self.lights[1][-2] = 1
    self.lights[-2][1] = 1
    self.lights[-2][-2] = 1
  
  def _neighbours_sum(self, row, col):
    l = self.lights
    return sum(l[row-1][col-1:col+2]) + \
           sum(l[row][col-1:col+2]) + \
           sum(l[row+1][col-1:col+2]) - \
           l[row][col]
  
  def step(self):
    grid = []
    for i in range(0, len(self.lights)-2):
      row = self.lights[i + 1]
      calc = []
      for j in range(0, len(row)-2):
        s = self._neighbours_sum(i+1, j+1)
        l = self.lights[i+1][j+1]
        if l:
          if s in [2,3]:
            calc.append(1)
          else:
            calc.append(0)
        else:
          if s == 3:
            calc.append(1)
          else:
            calc.append(0)
      grid.append(calc)
    
    grid[0][0] = 1
    grid[0][-1] = 1
    grid[-1][0] = 1
    grid[-1][-1] = 1
    
    for i in range(0, len(grid)):
      self.lights[i+1] = [0] + grid[i] + [0]


lg = LightsGrid()

with open('input') as f:
  for line in f:
    lg.add_row(line.strip())

lg.end_conf()


for i in range(0,100):
  print('Step:',i+1)
  lg.step()

print('Total lights on:',sum([sum(r) for r in lg.lights]))

    
      
      