
'''
letters = ["s", "d" , "c", "h"]
numbers = [2,3,5,7]
dictionary = dict()
for l in letters:
  dictionary[l] = [1,2,3,4,5,6]

#dictonary2 = {k:v for (k,v) in letters,numbers}
print(dictionary)

dictionary["d"].pop(1)

    # can take datetime as filename, but long and may be inconsistent
    ##from datetime import datetime, date, time
    ##filename = "" 
    ##
    ##for value in datetime.now():
    ##  filename += value 

# dictionary hearts:[1,2,3,4], diamond:[1,2,3,4]
# dictonary = {k:v for (k,v) in }
#print(dictionary["d"].remove(2))
#dictionary["d"].pop(1)
print(dictionary["d"])
print(dictionary)

list = [None,None,None]
print(len(list))
#for k in dictionary:
#  dictionary[k] = set(dictionary[k])
players = 3
list = {}
j = 0
for i in range(0, players*2, players):
  j += 1
  list[i] = j
print(list)
# for a in d.values()
# a.remove(4)       except value error
#print(dictionary.values())
#print(dictionary.items())

a = [1,2,3,4]
p = 2
print(a[:-1])
'''
'''
def FindCombination(public, hand): # return list [rank, ch, ch, h] for value comparison
  combined = public + hand
  suits, values = [], []
  allsuits = ("hearts", "diamonds", "spades", "clubs") # possibly replace

  for card in combined:
    split = card.split(".")
    suits.append(split[0])
    values.append(split[-1]) 
  values = sorted(values, key=int)

  def flush():
    for suit in allsuits:
      if suits.count(suit) >= 5: # suit type doesn't matter
        flush_values = []
        for card in combined:
          if suit[0] == card[0]: # match first letter
            flush_values.append(card.split(".")[-1]) # append value of card
        return [sorted(flush_values, key=int)[-1]]
    return False


  def same_num(count): 
    combination_highs = []
    for value in values:
      if values.count(value) == count: # IS PRECISE
        combination_highs.append(value)
        
    if len(combination_highs) != 0:
      return sorted(set(combination_highs), key=int)
    else:
      return False


  def straight():
    count = 0
    unique_values = sorted(set(values), key=int)
    loopedlist = unique_values + unique_values
    CH = []

    for i in range(len(unique_values) + 4):
      current = int(loopedlist[i]) + 1
      next = int(loopedlist[i + 1])
      
      if current == next or (current == 14 and next == 1): # king is 13, so + 1 would be 14 to account for loopback K-A 13-1
        count += 1
      else:
        count = 0
      if count >= 4:
        CH.append(next)

    if len(CH) != 0: # return the highest straight if multiple
      return [max(CH)]
    return False 


  def full_house():
    try:
      # should be sorted already low-high
      same_num3 = same_num(3)
      same_num2 = same_num(2)

      if len(same_num3) == 2:  # 2 3 of a kinds is automatically a full house
        return same_num3.reverse()
      
      if len(same_num3) == 1 and len(same_num2) > 0:
        return same_num3 + [same_num2[-1]]
      return False
    except:
      return False
  

  def high_card(quantity, CH): # takes how many high cards, existing CH in list form
    remaining = []
    for card in combined:
      if card.split(".")[-1] not in CH:
        remaining.append(card.split(".")[-1])
    result = sorted(set(remaining), key=int)[::-1] # sorted from high-low for later comparison
    return result[:quantity]

  #ensure every returned value is a list
  # CH straight flush
  CH = straight()
  isflush = flush()  
  if CH != False and isflush != False:
    if CH[0] == 1: # royal flush
      return [10]
    else:
      return [9] + CH   # return combination high

  # CH H 4 of a kind
  CH = same_num(4)
  if CH != False:
    H = high_card(1, CH)
    return [8] + CH + H

  # CH CH full house
  CH = full_house() 
  if CH != False:
    return [7] + CH

  # CH flush
  CH = flush()
  if CH != False:
    return [6] + CH
  
  # CH straight
  CH = straight()
  if CH != False:
    return [5] + CH

  # CH H 3 of a kind
  CH = same_num(3)
  if CH != False:
    return [4] + CH
  
  CH = same_num(2)
  # H high card
  if CH == False: 
    H = high_card(5, [])
    return [1] + H

  # CH CH H 2 pair
  if len(CH) >= 2:
    H = high_card(1, CH)
    return [3] + CH + H 

  # CH H pair
  if len(CH) == 1:
    H = high_card(3, CH)
    return [2] + CH + H
  
  else:
    return False

public = ['spades.3', 'hearts.1', 'diamonds.8', 'hearts.4', 'spades.10']
hand = ['spades.7', 'spades.6']
print([int(x) for x in FindCombination(public, hand)]) # force int
'''



'''
def straight():
  # Duplicate the list to consider the possibility of wrapping around
  numbers = [8, 7, 11, 12, 13, 1, 2]
  extended_numbers = numbers + numbers
  max_value = -1  #ensure any value in the list is greater

  for i in range(len(extended_numbers) - 4):
    consecutive_values = extended_numbers[i:i+5]
    # Check if the sequence contains both 1 and 13

    if 1 in consecutive_values and 13 in consecutive_values:
      #max_value = max(max_value, max(consecutive_values))
      max_value = consecutive_values[-1]
    # Check if the sequence is consecutive without wrapping

    elif max(consecutive_values) - min(consecutive_values) == 4:
      max_value = max(max_value, max(consecutive_values))
  print(max_value)

straight()
'''

'''
hand = ["sadc", "asdf"]
list1 = [1,3,4,5]
var = 3
var2 = 4
var3 = 45

def abc(args):

  first,second,third,fourth = args
  print(first,second,third,fourth)

abc([hand, var, var2, var3])
'''
'''
list1 = False
print(type(list1))
if type(list1) == list:
	print("list")
'''

'''
    if type(args) != list:  # default setup variables 
      self.players = 3 # includes human
      self.starting_chips = 5000 #£50 buy in chips interval bet of 0.5, for aesthetic only can be calculated easily, 5 chips 5,2,1,50 blinds left 2 of dealer
      self.big_blind = 50 #small blind is always half of big
      #startingblinds 
    else:               # custom setup variables
      self.players, self.starting_chips, self.big_blind = args
'''

'''
def func(var):
	if var == 1:
		return 4,6
	else:
		return 4


result = func(1)

print(result)
if result[0] == 4:
	print("A")

if type(result) == tuple:
  a = result[1]
  result = result[0]
print(a, result)
'''


#from itertools import cycle

'''
def circular():
  while True:
    for connection in round_players:
      yield connection

cycle = circular()
print(next(cycle))
print(next(cycle))
'''
'''
round_players = ["player_1", "player_2", "player_3"]

def loop(iterator, current_index, forward):
  if forward == False: #reverse
    if current_index <= 0:
      current_index = len(iterator) - 1
    else:
      current_index -= 1
    
  else:
    if current_index >= len(iterator) - 1:
      current_index = 0
    else:
      current_index += 1

  return iterator[current_index]
print(loop(round_players, 3, True))
'''

'''
hand = ["hearts.14", "spades.14"]
#blackbox

class new_round(): # money system, carry over chips,  beginning of round, sub class
  def __init__(self, players, player_dict): # players, starting_chips
    self.suits = ("hearts", "diamonds", "spades", "clubs")
    self.players = players
    self.player_dict = player_dict
  def func(self):
    print(2)
  

class Player(): 
  def __init__(self, player_id_value, chips_left, big_blind): # takes hands, player_id/arguments including player_id
    self.player_id_value = player_id_value
    self.chips_left = chips_left
    self.big_blind = big_blind    


  def NewCards(self, new_hand):
    self.__hand = new_hand
    return self.__hand

  def GetHand(self):
    return self.__hand


class ExtendedPlayer(Player, new_round): 
  def __init__(self, player_id_value, chips_left, big_blind, a, b): # takes hands, player_id/arguments including player_id, and new variables a and b
    Player.__init__(self, player_id_value, chips_left, big_blind)
    self.a = a
    self.b = b


#  def NewCards(self, new_hand): # can be removed
#     return super().NewCards(new_hand) #used on its own

  def GetHand(self):
    return super().GetHand()
 

bot = ExtendedPlayer(1,2,3,4,5)
print(bot.NewCards(90))
print(bot.func())

# write a new function for the ExtendedPlayer class to return the variables a and b
# add more functions to enable the class to function and therefore allow thge user to

face_values = [face_value for face_value in range(11,15)]
print(face_values)

'''
'''
var = 34
output = f"player {var}"
print(output)


other_player_card_locations = []

for player_id_value in range(1,7):  #range of other opponents #player in players
  location1 = (20, 122 + (player_id_value-1) * self.SMALL_CARD_HEIGHT)
  location2 = (80, 122 + (player_id_value-1) * self.SMALL_CARD_HEIGHT)
  diction[f"player_{player_id_value}"] = [location1, location2]




self.player_info_locations = dict()

for player_id_value in range(6):
  x =  140
  y =  122 + i * self.SMALL_CARD_HEIGHT
  self.player_info_locations[f"player_{player_id_value}"] = [x, y]
'''
'''
def function1(num):
	print(num)


def bigfunc(funcname):
	funcname()

#change number of opponents
bigfunc(function1(3))
'''


list1 = [3,4,5]
a,b,c = list1
print(a,b,c)

def update_player_info(self, *args):
  player_id_value, prev_action, chips_left = args
  print(player_id_value, prev_action, chips_left)

update_player_info(3,"asdf", 3)