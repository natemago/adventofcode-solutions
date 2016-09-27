#!/usr/bin/python3

from collections import namedtuple

Player = namedtuple('Player', ['hp','mana','armor'])
Boss   = namedtuple('Boss',['hp', 'damage'])


# name, cost, is_effect, turns
SPELLS = [
  ('M',  53, False, 0), # missile
  ('D',  73, False, 0), # drain
  ('S', 113,  True, 6), # shield
  ('P', 173,  True, 6), # poison
  ('R', 229,  True, 5)  # recharge
]

"""
Table of effect active for each timer value

Timer           Shield      Recharge    Poison
   6(CASTS)       1           N/A         0 
   5              1            0          1 
   4              1            1          1 
   3              1            1          1 
   2              1            1          1 
   1              1            1          1   
   0              0            1          1 
"""

EFFECTS_ACTIVE = {
  'S': [ 0, 1, 1, 1, 1, 1, 1],
  'R': [ 1, 1, 1, 1, 1, 0],
  'P': [ 1, 1, 1, 1, 1, 1, 0]
}


def cast_spell(spell_name, player, boss, timer, event='turn'):
  if spell_name == 'M':
    return player, Boss(boss.hp-4, boss.damage)
  elif spell_name == 'D':
    return Player(player.hp + 2, player.mana, player.armor), Boss(boss.hp - 2, boss.damage)
  elif spell_name == 'S':
    if EFFECTS_ACTIVE['S'][timer]:
      return Player(player.hp, player.mana, 7), boss
    else:
      return Player(player.hp, player.mana, 0), boss
  elif spell_name == 'P':
    if EFFECTS_ACTIVE['P'][timer]:
      return player, Boss(boss.hp - 3, boss.damage)
    return player, boss
    
  else: # recharge
    if EFFECTS_ACTIVE['R'][timer]:
      return Player(player.hp, player.mana + 101, player.armor), boss
    return player, boss

def player_turn(spell, player, boss, effects):
  # 1. Check if can cast spell
  #    1.1 Has enough mana
  #    1.2 Not in active effects
  # 2. Apply effects
  # 3. Cast spell/effect
  # 4. Check if boss dead
  
  name, cost, is_effect, turns = spell
  
  # 1
  if player.mana < cost:
    return None, player, boss, effects
  if effects.get(name):
    if effects[name] > 1:
      return None, player, boss, effects
  
  active_effects = {}
  for effect, timer in effects.items():
    event = 'end' if timer == 1 else 'turn'
    player, boss = cast_spell(effect, player, boss, timer, event)
    timer -= 1
    if timer >= 0:
      active_effects[effect] = timer
  
  event = 'start' if is_effect else 'turn'
  player, boss = cast_spell(name, player, boss, turns, event)
  if is_effect:
    active_effects[name] = turns - 1
  
  player = Player(player.hp, player.mana - cost, player.armor)
  
  winner = None
  
  if boss.hp <= 0:
    winner = 'player'
  
  return winner, player, boss, active_effects

def boss_turn(player, boss, effects):
  # 1. apply effects
  # 2. check if player is winner
  # 2. take hp from player
  # 3. check for winner
  active_effects = {}
  for effect, timer in effects.items():
    event = 'end' if timer == 1 else 'turn'
    player, boss = cast_spell(effect, player, boss, timer, event)
    timer -= 1
    if timer >= 0:
      active_effects[effect] = timer
  

  if boss.hp <= 0:
    return 'player', player, boss, active_effects
  
  winner = None
  player = Player(player.hp - max(boss.damage - player.armor, 1), player.mana, player.armor)
  if player.hp <= 0:
    winner = 'boss'
  return winner, player, boss, active_effects

def game_cycle(spell, player, boss, effects):
  winner, player, boss, effects = player_turn(spell, player, boss, effects)
  if winner:
    return winner, player, boss, effects
  return boss_turn(player, boss, effects)



def explore_game_space_bfs(player, boss, spells):
  from queue import Queue
  
  min_cost = None
  spells_casted = None
  
  q = Queue()
  
  for spell in spells:
    q.put((spell, spell[1], player, boss, {}, spell[0]))
  
  while not q.empty():
    spell, cost, player, boss, effects, backtrack = q.get()
    #print(spell, cost)
    winner, player, boss, effects = game_cycle(spell, player, boss, effects)
      
    
    if winner:
      if winner == 'player':
        if min_cost is None:
          print('Found the first possible solution: ', cost, ' -> ', backtrack)
          min_cost = cost
          spells_casted = backtrack
        else:
          if cost < min_cost:
            print('Found a better solution: ', cost, '->', backtrack)
            min_cost = cost
            spells_casted = backtrack
      continue
    
    for spell in spells:
      if spell[1] >= player.mana:
        continue
      if min_cost and cost + spell[1] > min_cost: # don't bother exploring this strategy
        continue
      q.put((spell, cost + spell[1], player, boss, effects, backtrack + ':' + spell[0]))  
  return min_cost, spells_casted

def simulate_play(spells, player, boss):
  effects = {}
  for spell in spells:
    spell = [s for s in SPELLS if s[0] == spell][0]
    winner, player, boss, effects = game_cycle(spell, player, boss, effects)
    print(spell, winner, player, boss, effects)


cost, backtrack = explore_game_space_bfs(Player(50, 500, 0), Boss(71, 10), SPELLS)
if cost:
  print('Win with at least %d using the following moves: %s' % (cost, backtrack))
else:
  print('Player cannot win with this setup')



