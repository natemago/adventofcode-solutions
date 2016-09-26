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
  
  cast_only = False
  
  for effect, turns in active_effects:
    event = 'end' if turns == 1 else 'turn'
    player, boss = EFFECTS_HNDS[effect](player, boss, event)
    turns -= 1
    log('   > Timer is now %d'%turns)
    if turns > 0:
      # add it for next cycle
      effects.append((effect, turns))
    if name == effect:
      cast_only = True
      
  if is_effect:
    player, boss = EFFECTS_HNDS[name](player, boss, 'start')
    effects.append((name, lasts_for))
  else:
    player,boss = SPELLS_HNDS[name](player, boss)
  
  hp,dam,arm,mana = player
  player = (hp,dam,arm,mana-cost)
  
  if (mana - cost) <= 0:
    winner = 'boss'
    print('NOOO')
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
  
  #for effect, turns in active_effects:
  #  if turns == 0:
  #    player, boss = EFFECTS_HNDS[effect](player, boss, 'end')
  #  else:
  #    player, boss = EFFECTS_HNDS[effect](player, boss, 'turn')
  #    effects.append((effect, turns - 1))
  #    log('\t\ttimer: ', turns - 1)
  
  for effect, turns in active_effects:
    event = 'end' if turns == 1 else 'turn'
    player, boss = EFFECTS_HNDS[effect](player, boss, event)
    turns -= 1
    log('   > Timer is now %d'%turns)
    if turns > 0:
      # add it for next cycle
      effects.append((effect, turns))
  #winner, player, boss =  player_vs_boss(player, boss, cost)
  
  
  
  if not winner and boss[0] <=0:
    winner = 'player'
  if not winner and player[0] <=0:
    winner = 'boss'
  
  if not winner:
    hp,dam,arm,mana = player
    player = (hp - max(boss[1] - player[2], 1), dam, arm, mana)
  else:
    log('Winner:', winner)
  
  log('-------------------------------------')
  return winner, player, boss, effects



def spell_in_active_effects(spell, active_effects):
  if len(active_effects):
    for effect, turns in active_effects:
      if effect == spell[0]:
        return (True, turns)
    return (False, None)
  else:
    return (False, None)

def can_cast_spell(spell,active_effects,player):
  if player[3]- spell[1] <= 0:
    return False
  is_in, turns = spell_in_active_effects(spell, active_effects)
  if is_in:
    if turns <= 2:
      #print('Effect (%s) can be casted because on end turn' % str(spell))
      #if spell[0] in ['Recharge','Poison']:    
      return True
    return False
  else:
    return True



def get_cost(player, boss, debug=False, BACKTRACK=False, MAX_MOVE=None, BREAK_AT_FIRST=False):
  global DEBUG
  
  DEBUG = debug
  
  q = queue.Queue()
  min_cost = None
  final_backtrack = None
  
  
  for spell in SPELLS:
    backtrack = spell[0] if BACKTRACK else ''
    q.put((spell, 1, [], player, boss, 0, backtrack))
    
  while not q.empty():
    spell, move, active_effects, player, boss, cost, backtrack= q.get()
    cost += spell[1]
    
    winner, player, boss, active_effects = play_move(spell, active_effects, player, boss)
    
    if winner:
      # do check here
      print('%d %s\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b' %(move, winner), end='')
      if winner == 'player':
        print(move, ') player at cost: ', cost, ' (',min_cost,') over ', backtrack)
        if min_cost is None or cost < min_cost:
          min_cost = cost
          final_backtrack = backtrack
        if BREAK_AT_FIRST and min_cost:
          return min_cost, backtrack
      continue
    
    if MAX_MOVE and move+1 > MAX_MOVE:
      continue
    for spell in SPELLS:
      if can_cast_spell(spell, active_effects, player):
        if min_cost is not None and (cost+spell[1]) >= min_cost:
          continue
        bt = (backtrack + '->' + spell[0]) if BACKTRACK else ''
        q.put((spell, move+1, active_effects, player, boss, cost, bt))
    
  return min_cost, final_backtrack

def simulate(moves, player, boss, debug=True):
  global DEBUG
  DEBUG = debug
  effects = []
  for spell in [_SPELLS[s] for s in moves]:
    winner, player, boss, effects = play_move(spell, effects, player, boss)
    
  return winner, player, boss

def ok(exp, msg=''):
  if not exp:
    raise Exception(msg or 'Assertion failed')

# == Test Cases ==

#Test is_in
print("=============================")
print('Test 1 spell_in_active_effects')
is_in, turns = spell_in_active_effects(_SPELLS['Poison'], [('Shield',4),('Poison',3)])
ok(is_in == True, 'Should be in')
ok(turns == 3, 'Should have timer 3')
print('spell_in_active_effects - test 1 OK')

print("=============================")
print('Test 2 spell_in_active_effects')
is_in, turns = spell_in_active_effects(_SPELLS['Poison'], [('Shield',4),('Drain',3)])
ok(is_in == False, 'Should NOT be in')
ok(turns is None, 'Should NOT have timer')
print('spell_in_active_effects - test 2 OK')

print('==============================')
winner, player, boss = simulate(moves=['Poison', 'MagicMissile'], player=(10,0,0,250),boss=(13,8), debug=True)
ok('player' == winner, 'Winner is not player')
ok(player[0] == 2, 'Player should have 2 hit points')
ok(player[2] == 0, 'Player should have 0 armor')
ok(player[3] == 24, 'Player should have 24 mana')

ok(boss[0] == 0, 'Boss should have 0 points')
print('=============================')
print('Test case 1: OK')
print()

winner, player, boss = simulate(moves=['Recharge','Shield','Drain','Poison','MagicMissile'], player=(10,0,0,250),boss=(14,8), debug=True)
ok('player' == winner, 'Winner is not player')
ok(player[0] == 1, 'Player should have 1 hit point1')
ok(player[2] == 0, 'Player should have 0 armor')
ok(player[3] == 114, 'Player should have 114 mana')

ok(boss[0] == -1, 'Boss should have -1 points')
print('=============================')
print('Test case 2: OK')
print()

cost, backtrack = get_cost((10, 0, 0, 250),(13, 8), debug=False, BACKTRACK=True, BREAK_AT_FIRST=True)
ok(cost == 226, 'Cost should be 226, but got %s instead'%str(cost))
ok(backtrack == 'Poison->MagicMissile', 'Unexpected moves: %s'%str(backtrack))
print('=============================')
print('Test case 3: OK')
print()

cost, backtrack = get_cost((10, 0, 0, 250),(14, 8), debug=False, BACKTRACK=True, BREAK_AT_FIRST=True)
ok(cost == 641, 'Cost should be 641, but got %s instead'%str(cost))
ok(backtrack == 'Recharge->Shield->Drain->Poison->MagicMissile', 'Unexpected moves: %s'%str(backtrack))
print('=============================')
print('Test case 4: OK')
print()

# hit points, damage, armor, mana
#player = (50, 0, 0, 500)
#boss = (71, 10)



print('>> Starting search')
cost, backtrack = get_cost((50, 0, 0, 500),(71, 10), debug=False, BACKTRACK=True, BREAK_AT_FIRST=False)
#cost, backtrack = get_cost((50, 0, 0, 500),(58, 9), debug=False, BACKTRACK=True, BREAK_AT_FIRST=True)
print(cost, backtrack)

