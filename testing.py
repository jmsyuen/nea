
'''
letters = ["s", "d" , "c", "h"]
numbers = [2,3,5,7]
dictionary = dict()
for l in letters:
  dictionary[l] = [1,2,3,4,5,6]

#dictonary2 = {k:v for (k,v) in letters,numbers}
print(dictionary)

dictionary["d"].pop(1)


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
    return [0]

public = ['spades.3', 'hearts.1', 'diamonds.8', 'hearts.4', 'spades.10']
hand = ['spades.7', 'spades.6']
print([int(x) for x in FindCombination(public, hand)]) # force int




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