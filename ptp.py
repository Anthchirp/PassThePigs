from __future__ import absolute_import, division, print_function

import collections
import random

# Possible roll outcomes
# S = Sum score
# T = Turn score
# Return: deltaT, End of Turn
def E1(S, T): return (1, False) # dot and non-dot
def E2(S, T): return (5, False) # single Trotter, Razorback
def E3(S, T): return (10, False) # Snouter; Trotter & Razorback
def E4(S, T): return (15, False) # Snouter and Trotter or Razorback; Jowler
def E5(S, T): return (20, False) # double Trotter or Razorback; Jowler and Trotter or Razorback
def E6(S, T): return (25, False) # Jowler and Snouter
def double_snouter(S, T): return (40, False) 
def double_jowler(S, T): return (60, False)
def pig_out(S, T): return (-T, True)
def making_bacon(S, T): return (-S-T, True)
# Roll probabilities from https://doi.org/10.1080/10691898.2006.11910593 tables 3 and 4, but not 7
throw = 23 * [making_bacon] + 1279 * [pig_out] + 1304 * [E1] + 2337 * [E2] + 508 * [E3] + 171 * [E4] + 373 * [E5] + 2 * [E6] + 2 * [double_snouter] + 1 * [double_jowler]

# Strategies:
# * named 'strategy_'
# * first argument is total score up to that point in time, including round score
# * second argument is score accumulated so far in this round
# * return value is 'Keep playing?'

def strategy_stop_at_10(game_score, round_score):
  return round_score < 10

def strategy_stop_at_11(game_score, round_score):
  return round_score < 11

def strategy_stop_at_15(game_score, round_score):
  return round_score < 15

def strategy_stop_at_17(game_score, round_score):
  return round_score < 17

def strategy_stop_at_19(game_score, round_score):
  return round_score < 19

def strategy_stop_at_20(game_score, round_score):
  return round_score < 20

def strategy_stop_at_21(game_score, round_score):
  return round_score < 21

def strategy_stop_at_22(game_score, round_score):
  return round_score < 22

def strategy_stop_at_23(game_score, round_score):
  return round_score < 23

def strategy_stop_at_50(game_score, round_score):
  return round_score < 50

#def strategy_stop_at_15_hold_at_choke_points(game_score, round_score):
 # if game_score >= 90 and (game_score - round_score) < 90: return False
 # if game_score >= 80 and (game_score - round_score) < 80: return False
 # return round_score < 15

#def strategy_stop_at_15_slow_past_85(game_score, round_score):
#  return round_score < 15 and game_score < 85

def strategy_stop_at_17_slow_past_85(game_score, round_score):
  return round_score < 17 and game_score < 85

def strategy_flip_coin(game_score, round_score):
  return random.random() < 0.5

def play_turn(S, strategy):
  '''Given a game score so far and a decision strategy, play a turn and return the new game score'''
  T = 0
  while True:
    gain, done = throw[random.randint(0, 5999)](S, T)
    if done:
      return S + T + gain
    T = T + gain
    game_score = S + T
    if game_score >= 100 or not strategy(game_score, T):
      return game_score

def game(strategy1, strategy2):
  '''Play two strategies against one another.
     Returns True if strategy1 wins, False if strategy2 wins
  '''
  S1, S2 = 0, 0
  while True:
    S1 = play_turn(S1, strategy1)
    if S1 >= 100: return True
    S2 = play_turn(S2, strategy2)
    if S2 >= 100: return False

strategies = {name: globals()[name] for name in dir() if name.startswith('strategy_')}

# Play all strategy combinations 2000 times each
score_table = {
  (s1, s2): collections.Counter(game(strategies[s1], strategies[s2]) for round in range(2000))
  for s1 in strategies
  for s2 in strategies
  if s1 != s2
}

successes = {s: 0 for s in strategies}
for pair, outcomes in score_table.items():
  successes[pair[0]] += outcomes[True]
  successes[pair[1]] += outcomes[False]
for entry in sorted(successes.items(), key=lambda s: -s[1]):
  print("%%%ds: %%d wins" % max(map(len, strategies)) % entry)