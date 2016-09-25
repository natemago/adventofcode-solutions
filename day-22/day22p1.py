#!/usr/bin/python3

import queue

SPELLS = [
  ('MagicMissile', 53, False,0),
  ('Drain', 73, False,0),
  ('Shield', 113, True, 6),
  ('Poison', 173, True, 6),
  ('Recharge', 229, True, 5)]


def magic_missile(player):
  hit_points, damage, armor, mana = player
  return (hit_points, damage+4, armor, mana)

def drain(player):
  hit_points, damage, armor, mana = player
  return (hit_points+2, damage+2, armor, mana)

def shield(player, boss, event):
  hit_points, damage, armor, mana = player
  if event == 'start':
    return ((hit_points, damage, armor+7, mana), boss)
  elif event == 'end':
    return ((hit_points, damage, armor-7, mana), boss)
  else:
    return (player,boss)

def poison(player,boss, event):
  hit_points, damage = boss
  return (player, (hit_points-3,damage))

def recharge(player, boss, event):
  hit_points, damage, armor, mana = player
  return ((hit_points, damage, armor, mana+101), boss)

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
  name, cost, is_effect, lasts_for = spell
  if is_effect:
    player, boss = EFFECTS_HNDS[name](player, boss, 'start')
    active_effects[name] = lasts_for - 1
  else:
    player = SPELLS_HNDS[name](player)
  
  effects = {}
  remove_effects = []
  for effect, turns in active_effects.items():
    if effect == name:
      continue
    turns -= 1
    effects[effect] = turns
    if not turns:
      player, boss = EFFECTS_HNDS[effect](player, boss, 'end')
      remove_effects.append(effect)
    else:
      player, boss = EFFECTS_HNDS[effect](player, boss, 'turn')
    effects[effect] = turns
  
  active_effects.update(effects)
  
  for ef in remove_effects:
    del active_effects[ef]
  
  return player_vs_boss(player, boss, cost)

def player_vs_boss(player, boss, cost):
  p_hit_points, p_damage, p_armor, p_mana = player
  b_hit_points, b_damage = boss
  
  p_hit_points -= max(b_damage-p_armor, 1)
  b_hit_points -= max(p_damage, 1)
  
  winner = None
  
  
  p_mana -= cost
  if p_mana <= 0:
    winner = 'boss'
  else:
    if p_hit_points <= 0:
      winner = 'boss'
    if b_hit_points <= 0:
      winner = 'player'
  
  return winner, (p_hit_points, p_damage, p_armor, p_mana), (b_hit_points, b_damage)


def spell_in_active_effects(spell, active_effects):
  if len(active_effects):
    for ac in active_effects:
      if ac[0] == spell:
        return (True, ac[1])
    return (False, None)
  else:
    return (False, None)

def can_cast_spell(spell,active_effects):
  is_in, turns = spell_in_active_effects(spell, active_effects)
  if is_in:
    if turns == 1:
      return True
    return False
  else:
    return True

q = queue.Queue()

# hit points, damage, armor, mana
#player = (50, 0, 0, 500)
#boss = (71, 10)
player = (10, 0, 0, 250)
boss= (13,8)


for spell in SPELLS:
  q.put((spell, 1, {}, player, boss, 0))

while not q.empty():
  spell, move, active_effects, player, boss, cost = q.get()
  
  cost += spell[1]
  
  winner, player, boss = play_move(spell, active_effects, player, boss)
  print(spell, player, boss)
  if winner:
    # do check here
    #print('%d %s\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b' %(move, winner), end='')
    print(winner, 'wins')
    if winner == 'player':
      raise Exception(cost)
    continue
  
  for spell in SPELLS:
    if can_cast_spell(spell, active_effects):
      q.put((spell, move+1, active_effects, player, boss, cost))
  