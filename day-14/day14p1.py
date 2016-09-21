#!/usr/bin/python3

import re

from math import floor

class Reindeer:
  def __init__(self, name, speed, race_time, rest_time):
    self.name = name
    self.speed = speed
    self.per_cycle_speed = speed*race_time
    self.cycle_time = race_time + rest_time
    self.race_time = race_time
    self.rest_time = rest_time
  
  def get_distance_after(self, time):
    dist = floor(time/self.cycle_time)*self.per_cycle_speed
    if time%self.cycle_time:
      leftover_time = time - (floor(time/self.cycle_time)*self.cycle_time)
      if leftover_time >= self.race_time:
        dist += self.race_time*self.speed
      else:
        dist += leftover_time*self.speed
    return dist


reindeers = []

with open('input') as f:
  line = f.readline()
  
  while line:
    line = line.strip()
    
    m = re.match('(?P<name>\w+) can fly (?P<speed>\d+) km/s for (?P<race_time>\d+) seconds, but then must rest for (?P<rest_time>\d+) seconds.', line)
    name = m.group('name')
    speed = int(m.group('speed'))
    race_time = int(m.group('race_time'))
    rest_time = int(m.group('rest_time'))
    
    reindeers.append(Reindeer(name=name, speed=speed, race_time=race_time, rest_time=rest_time))
    
    
    line = f.readline()
    


winner = max(reindeers, key=lambda r: r.get_distance_after(2503))


print(winner.name, winner.get_distance_after(2503))
    