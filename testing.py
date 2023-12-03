

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


def FindCombination():
  public = ['diamonds.1', 'spades.3', 'clubs.4', 'hearts.2', 'spades.2']
  hand = ['diamonds.11', 'clubs.11']
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

  def flush():
    for suit in allsuits:
      if suits.count(suit) >= 5:
        #print(f"{suit} floosh") # suit type doesn't matter
        return True
    return False


  def same_values(count):
    for value in values:
      if values.count(value) == count:
        return True
    return False

  def same_num(count): # 2 3 of a kinds is automatically a full house
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
    for i in range(len(values) - 1):
      if int(values[i]) + 1 == int(values[i + 1]):
        count += 1
        if count >= 4:
          return True
      else:
        count = 0
    return False 
  

  def full_house():
    try:
      # should be sorted already low-high
      if len(same_num(3)) == 2:
        print("fh")
      elif len(same_num(3)) == 1 and len(same_num(2)) > 0:
        return True
      else:
        return False
    except:
      return False
  
  # CH straight flush C royal flush
  if flush() and straight():
    print("straight flush") # add royal flush and return combination high

  # CH H 4 of a kind
  elif same_values(4):
    print("4 of kind")


  # CH CH full house
  elif full_house():
    print("full house")

  # CH flush

  # CH straight


  # CH H 3 of a kind


  # CH H 2 pair


  # CH H pair


  # H high card




FindCombination()


