#!/usr/bin/python3


import re

class Computer:
  def __init__(self, REGISTERS = None, mem=None):
    self.REGISTERS = REGISTERS or {
      'a': 0,
      'b': 0
    }
    self.PC = 0
    self.mem = mem or []
  
  def add(self, instr):
    self.mem.append(instr)
    print('MEM:', instr)
  
  def exec(self):
    try:
      while True:
        self.exec_next()
    except Exception as e:
      print(e)
  
  def exec_next(self):
    if self.PC >=0 and self.PC < len(self.mem):
      instr, reg, offset = self.mem[self.PC]
      
      if instr == 'hlf':
        self.REGISTERS[reg] //= 2
        self.PC += 1
      elif instr == 'tpl':
        self.REGISTERS[reg] *= 3
        self.PC += 1
      elif instr == 'inc':
        self.REGISTERS[reg] += 1
        self.PC += 1
      elif instr == 'jmp':
        pc = self.PC + offset
        if pc < 0 or pc > len(self.mem):
          raise Exception('HALT')
        self.PC = pc
      elif instr == 'jie':
        if self.REGISTERS[reg] % 2 == 0:
          pc = self.PC + offset
          if pc < 0 or pc > len(self.mem):
            raise Exception('HALT')
          self.PC = pc
        else:
          self.PC += 1
      elif instr == 'jio':
        if self.REGISTERS[reg] == 1:
          pc = self.PC + offset
          if pc < 0 or pc > len(self.mem):
            raise Exception('HALT')
          self.PC = pc
        else:
          self.PC += 1
      else:
        raise Exception('Invalid instruction' + instr)
    else:
      raise Exception('HALT')


mem = []
with open('input') as f:
  for line in f:
    m = re.match('(?P<instr>\w+) ((?P<reg>\w)(, )?)?(?P<offset>[+-]\d+)?', line.strip())
    instr = m.group('instr')
    reg = m.group('reg')
    offset = m.group('offset')
    
    if offset:
      offset = int(offset)
    
    mem.append((instr, reg, offset))

# -- Part 1
cmp = Computer(mem=mem)
cmp.exec()
print(cmp.REGISTERS['b'])

# -- Part 2
cmp = Computer(REGISTERS={'a':1,'b':0}, mem=mem)
cmp.exec()
print(cmp.REGISTERS['b'])
