#!/usr/bin/python3

import math

def combinations(choice, elements, base):
  if choice == 1:
    for e in elements:
      yield base +[e]
  else:
    for i in range(0, len(elements) - choice + 1):
      yield from combinations(choice - 1, elements[i+1:], base + [elements[i]])


def play(player1, player2):
  p1_points, p1_damage, p1_armor = player1
  p2_points, p2_damage, p2_armor = player2
  
  p1_rate = 1 if p1_damage <= p2_armor else p1_damage - p2_armor
  p2_rate = 1 if p2_damage <= p1_armor else p2_damage - p1_armor
  #print(p1_rate, p2_rate)
  
  
  p1_hits = math.ceil(p2_points/p1_rate)
  p2_hits = math.ceil(p1_points/p2_rate)
  #print(p1_hits, p2_hits)
  
  return 1 if p1_hits <= p2_hits else 2


BOSS_POINTS = 103
PLAYER_POINTS = 100

WEAPONS = [(8,4,0),(10,5,0),(25,6,0),(40,7,0),(74,8,0)]
ARMOR = [(13,0,1),(31,0,2),(53,0,3),(75,0,4),(102,0,5),(0,0,0)]
RINGS = [(25,1,0),(50,2,0),(100,3,0),(20,0,1),(40,0,2),(80,0,3),(0,0,0),(0,0,0)]



boss = Player('boss', BOSS_POINTS, 9, 2)
player = Player('player', PLAYER_POINTS, 0, 0)


min_cost = None
max_cost = None


print(play((100,4,0),(103,9,2)))


for weapon in WEAPONS:
  weapon_cost, weapon_damage, weapon_armor = weapon
  for i in range(1, len(ARMOR)):
    for armors in combinations(i, ARMOR, []):
      for armor in armors:
        armor_cost, armor_damage, armor_armor = armor
        for j in [1,2]:
          for rings in combinations(j, RINGS, []):
            ring_cost = ring_damage = ring_armor = 0
            
            for ring in rings:
              rc,rd,ra = ring
              ring_cost += rc
              ring_damage += rd
              ring_armor += ra
              
            tot_cost = weapon_cost + armor_cost + ring_cost
            tot_armor = weapon_armor + armor_armor + ring_armor
            tot_damage = weapon_damage + armor_damage + ring_damage
              
            if play((PLAYER_POINTS, tot_damage, tot_armor),(BOSS_POINTS, 9, 2)) == 1:
              #print(weapon_cost, armor_cost, ring_cost)
              if min_cost is None or tot_cost < min_cost:
                min_cost = tot_cost
            else:
              if max_cost is None or tot_cost > max_cost:
                max_cost = tot_cost
              
print('Can win with at least: ',min_cost)
print('Will still lose eve with: ', max_cost)

