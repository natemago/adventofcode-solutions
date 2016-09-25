#!/usr/bin/python3

import queue

SPELLS = [
  ('MagicMissile', 53, False,0),
  ('Drain', 73, False,0),
  ('Shield', 113, True, 6),
  ('Poison', 173, True, 6),
  ('Recharge', 229, True, 5)]

_SPELLS = {
  'MagicMissile': SPELLS[0],
  'Drain': SPELLS[1],
  'Shield': SPELLS[2],
  'Poison': SPELLS[3],
  'Recharge': SPELLS[4],
}

DEBUG = False
BREAK_AT_FIRST = True
MAX_MOVE = 12
BACKTRACK = False

def log(*args):
  if DEBUG:
    print(*args)


def magic_missile(player, boss):
  #hit_points, damage, armor, mana = player
  b_hit_points, b_damage = boss
  #return (hit_points, damage+4, armor, mana)
  return (player, (b_hit_points-4,b_damage))
  
def drain(player, boss):
  hit_points, damage, armor, mana = player
  b_hit_points, b_damage = boss
  return ((hit_points+2, damage, armor, mana),(b_hit_points-2,b_damage))

def shield(player, boss, event):
  hit_points, damage, armor, mana = player
  if event == 'start':
    log('Shield provides increased armor by 7')
    return ((hit_points, damage, armor+7, mana), boss)
  elif event == 'end':
    log('Shield ended. Armor reduced by 7')
    return ((hit_points, damage, armor-7, mana), boss)
  else:
    log('Shield provides increased armor by 7')
    return (player,boss)

def poison(player,boss, event):
  hit_points, damage = boss
  if event =='end':
    log('Poison wears off')
  if event != 'start':
    log('Poison deals 3 damage to boss')
    return (player, (hit_points-3,damage))
  else:
    return player,boss
    
def recharge(player, boss, event):
  hit_points, damage, armor, mana = player
  if event != 'start':
    log('Recharge provides 101 mana')
    return ((hit_points, damage, armor, mana+101), boss)
  else:
    return player,boss
  
SPELLS_HNDS = {
  'MagicMissile': magic_missile,
  'Drain': drain
}

EFFECTS_HNDS = {
  'Shield': shield,
  'Poison': poison,
  'Recharge': recharge
}

def play_move(spell, active_effects, player, boss):
  winner = None
  name, cost, is_effect, lasts_for = spell
  effects = []
  log(' -- Player Turn --')
  log(' - Player has %d hit points, %d armor, %d mana' % (player[0],player[2],player[3]))
  log(' - Boss has %d hit points, %d damage' % boss)
  log('Player casts %s.'%name)
  if is_effect:
    player, boss = EFFECTS_HNDS[name](player, boss, 'start')
    effects.append((name, lasts_for))
  else:
    player,boss = SPELLS_HNDS[name](player, boss)
  
 
  for effect, turns in active_effects:
    if effect == name:
      continue
    turns -= 1
    if not turns:
      player, boss = EFFECTS_HNDS[effect](player, boss, 'end')
    else:
      player, boss = EFFECTS_HNDS[effect](player, boss, 'turn')
      effects.append((effect, turns))
  
  hp,dam,arm,mana = player
  player = (hp,dam,arm,mana-cost)
  
  if (mana - cost) < 0:
    winner = 'boss'
  if not winner and boss[0] <= 0:
    winner = 'player'
  
  if winner:
    log('Winner:', winner)
    return winner, player, boss, effects
  
  active_effects = effects
  effects = []
  
  log()
  log(' -- Boss Turn --')
  log(' - Player has %d hit points, %d armor, %d mana' % (player[0],player[2],player[3]))
  log(' - Boss has %d hit points, %d damage' % boss)
  for effect, turns in active_effects:
    turns -= 1
    
    if not turns:
      player, boss = EFFECTS_HNDS[effect](player, boss, 'end')
    else:
      player, boss = EFFECTS_HNDS[effect](player, boss, 'turn')
      effects.append((effect, turns))
   
  #winner, player, boss =  player_vs_boss(player, boss, cost)
  
  hp,dam,arm,mana = player
  player = (hp - max(boss[1] - player[2], 1), dam, arm, mana)
  
  if not winner and boss[0] <=0:
    winner = 'player'
  if not winner and player[0] <=0:
    winner = 'boss'
  
  
  if winner:
    log('Winner:', winner)
  
  log('-------------------------------------')
  return winner, player, boss, effects

  

def player_vs_boss(player, boss, cost):
  p_hit_points, p_damage, p_armor, p_mana = player
  b_hit_points, b_damage = boss
  
  p_hit_points -= max(b_damage-p_armor, 1)
  #b_hit_points -= max(p_damage, 1)
  
  winner = None
  
  
  #p_mana -= cost
  if p_mana <= 0:
    winner = 'boss'
  else:
    
    if b_hit_points <= 0:
      winner = 'player'
    elif p_hit_points <= 0:
      winner = 'boss'
  return winner, (p_hit_points, p_damage, p_armor, p_mana), (b_hit_points, b_damage)


def spell_in_active_effects(spell, active_effects):
  if len(active_effects):
    for ac in active_effects:
      if ac[0] == spell:
        return (True, ac[1])
    return (False, None)
  else:
    return (False, None)

def can_cast_spell(spell,active_effects,player):
  if player[3]- spell[1] <= 0:
    return False
  is_in, turns = spell_in_active_effects(spell, active_effects)
  if is_in:
    if turns == 1:
      return True
    return False
  else:
    return True

q = queue.Queue()

# hit points, damage, armor, mana
player = (50, 0, 0, 500)
boss = (71, 10)
#player = (10, 0, 0, 250)
#boss= (14,8)

# -------------------------
if DEBUG and False:
  player = (10, 0, 0, 250)
  boss= (14, 8)
  effects = []
  for spell in [_SPELLS[s] for s in ['Recharge','Shield','Drain','Poison','MagicMissile'] ]:
    winner, player, boss, effects = play_move(spell, effects, player, boss)
    



  import sys
  sys.exit()
# -------------------------

min_cost = None

for spell in SPELLS:
  backtrack = spell[0] if BACKTRACK else ''
  q.put((spell, 1, [], player, boss, 0, backtrack))
  
while not q.empty():
  spell, move, active_effects, player, boss, cost, backtrack= q.get()
  if BACKTRACK:
    backtrack += '->' + spell[0]
  cost += spell[1]
  
  winner, player, boss, active_effects = play_move(spell, active_effects, player, boss)
  #print(move,'->', spell, player, boss)
  if winner:
    # do check here
    print('%d %s\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b' %(move, winner), end='')
    if winner == 'player':
      #print('*******')
      print('player at cost: ', cost, ' (',min_cost,') over ', backtrack)
      if BREAK_AT_FIRST:
        raise Exception('Cost %d' % cost)
      if min_cost is None or cost < min_cost:
        min_cost = cost
      
    continue
  
  if move+1 > MAX_MOVE:
    continue
  for spell in SPELLS:
    if can_cast_spell(spell, active_effects, player):
      q.put((spell, move+1, active_effects, player, boss, cost, backtrack))


print('Min cost:', min_cost)
