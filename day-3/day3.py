#!/usr/bin/python3


def poslabel(pos):
  return '%d:%d' % (pos[0],pos[1])

class Santa:
  
  INSTRUCTIONS = {
    '^': [0, 1], # up
    '<': [-1, 0], # left
    'v': [0,-1], # down
    '>': [1, 0] # right
  }
  
  def __init__(self, pos=None):
    self.pos = pos or [0,0]
    self.visited = {}
    self.visited[poslabel(self.pos)] = 1
    
    
  def move(self, inst):
    dif = Santa.INSTRUCTIONS[inst]
    self.pos = [self.pos[0] + dif[0], self.pos[1] + dif[1]]
    
    vlabel = poslabel(self.pos)
    if not self.visited.get(vlabel):
      self.visited[vlabel] = 1
    else:
      self.visited[vlabel] = self.visited[vlabel] + 1
  
  def total_visited(self):
    return len(self.visited)



with open('input') as f:
  instructions = f.read()


santa = Santa()
robo_santa = Santa()

inst_cnt = 1
for inst in instructions:
  if inst_cnt%2 == 1:
    santa.move(inst)
  else:
    robo_santa.move(inst)
  inst_cnt += 1



total = {}
total.update(santa.visited)
total.update(robo_santa.visited)

print(len(total))
print(santa.total_visited())
print(robo_santa.total_visited())


