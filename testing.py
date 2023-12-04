

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


def FindCombination(): # return list [rank, ch, ch, h] if applicable
  public = ['spades.1', 'spades.13', 'spades.12', 'spades.11', 'spades.10']
  hand = ['diamonds.4', 'clubs.4']
  combined = public + hand
  suits, values = [], []
  allsuits = ("hearts", "diamonds", "spades", "clubs")
  
  #def sort_values():


  for card in combined:
    #card.split(".")[-1] retrieves value of card
    split = card.split(".")
    suits.append(split[0])
    values.append(split[-1]) 
    print(suits, values)
  values = sorted(values, key=int)
  high_cards = values.reverse()

  def flush():
    for suit in allsuits:
      if suits.count(suit) >= 5:
        #print(f"{suit} floosh") # suit type doesn't matter
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
    for i in range(len(unique_values) - 1): 
      if int(unique_values[i]) + 1 == int(unique_values[i + 1]): # account for loopback K-A 13-1
        count += 1
        if count >= 4:
          return [unique_values[i + 1]]
      else:
        count = 0
    return False 
  

  def full_house():
    try:
      # should be sorted already low-high
      same_num3 = same_num(3)
      same_num2 = same_num(2)

      if len(same_num3) == 2:  # 2 3 of a kinds is automatically a full house
        return same_num3.reverse()
      
      elif len(same_num3) == 1 and len(same_num2) > 0:
        return same_num3 + [same_num2[-1]]
      else:
        return False
    except:
      return False
  

  def high_card(quantity, CH): # takes how many high cards, existing CH in list form
    remaining = []
    for card in combined:
      if card.split(".")[-1] not in CH:
        remaining.append(card.split(".")[-1])
    return sorted(set(remaining), key=int)[-quantity:]


  #ensure every returned value is a list
  # CH straight flush C royal flush
  CH = straight()
  flush_temp = flush()  
  if CH != False and flush_temp != False:
    if CH == 13: # royal flush
      return [10]
    return [9] + CH   # add royal flush and return combination high

  # CH H 4 of a kind
  CH = same_num(4)
  H = high_card(1, CH)
  if CH != False:
    return [8] + CH + H


  # CH CH full house
  CH = full_house() # elif outside of statement
  if CH != False:
    return [7] + CH

  # CH flush
  CH = flush()
  if CH != False:
    return [6] + CH
  
  # CH straight
  if straight():
    print("straight")

  # CH H 3 of a kind
  if same_num(3):
    print("3ofkind")

  # CH CH H 2 pair
  CH = same_num(2)
  if len(CH) >= 2:
    print(f"{CH[-2:]} two pair") # reverse this list
  # CH H pair
  if len(CH) == 1:
    print(f"{CH} pair high")

  # H high card
  if len(CH) == 0:
    print(f"{high_cards[0]}High card")

  else:
    print("random error")


print([int(x) for x in FindCombination()]) # force int


