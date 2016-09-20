#!/usr/bin/python3

import re


class Op:
  def __init__(self, op, inputs, out):
    self.inputs = inputs
    self.out = out
    self.op = op
  
  def resolve(self, wires):
    print(' resolve %s with inputs %s' % (self.out, str(self.inputs)))
    all_resolved = True
    actual_inputs = []
    for inp in self.inputs:
      print ('   inp: %s' % str(inp))
      if inp is None:
        continue
      if isinstance(inp, int):
        actual_inputs.append(inp)
        continue
      
      val = wires[inp]
      if isinstance(val, Op):
        val = val.resolve(wires)
        if val is not None:
          actual_inputs.append(val)
        else:
          all_resolved = False
      else:
        actual_inputs.append(val)
    
    if all_resolved:
      try:
        out = self._calc_out(actual_inputs)
        wires[self.out] = out
        print('%s = %d' % (self.out, out) )
        return out
      except:
        print('Op -> %s [actual inputs: %s]' % (self, str(actual_inputs)))
        raise
    
    return None
  
  def _calc_out(self, inputs):
    if self.op is None:
      return inputs[0]
    if self.op == 'AND':
      return inputs[0] & inputs[1]
    if self.op == 'OR':
      return inputs[0] | inputs[1]
    if self.op == 'LSHIFT':
      return inputs[0] << inputs[1]
    if self.op == 'RSHIFT':
      return inputs[0] >> inputs[1]
    if self.op == 'NOT':
      return ~inputs[0]
  
  def __str__(self):
    return '%s %s' % (self.op, str(self.inputs))
  
  def __repr__(self):
    return self.__str__()
  
wires = {}


with open('input') as f:
  line = f.readline()
  while line:
    print(line)
    m = re.match('((?P<in1>\w+)\s+)?(?P<op>[A-Z]+)\s+(?P<in2>\w+)\s->\s(?P<target>\w+)', line)
    if not m:
      m = re.match('(?P<in1>\w+)\s+->\s+(?P<target>\w+)', line)
      
      
    in1 = m.group('in1')
    in2 = None
    op = None
    try:
      in2 = m.group('in2')
      op = m.group('op')
    except:
      pass
    
    target = m.group('target')
    
    if in1 and re.match('\d+', in1):
      in1 = int(in1)
    if in2 and re.match('\d+', in2):
      in2 = int(in2)
    
    inputs = []
    if in1 is not None:
      inputs.append(in1)
    inputs.append(in2)
    
    operation = Op(inputs=inputs, op=op, out=target)
    wires[target] = operation
    
    line = f.readline()

print(wires['a'])

wires['a'].resolve(wires)
print(wires['a'])
