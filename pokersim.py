import random
import os
import sqlite3
from sqlite3 import Error #


# one tag is useful comments
## two tags for code clips
### three tags for issues
# 3 tags at the end for testing, remove later ###
# cards ranked from Ace 2 3 ... 10 Jack Queen King
# use special behaviour of number 1 to define the high value of it / use ace as the highest value in the list
# randint is inclusive of both limits
# range is inclusive of first value only eg. 1,14 is 1-13
# to unpack a list use asterisk before variable print(*list)
# change to 2-14 for ace high



class new_round(): # money system, carry over chips,  beginning of round, sub class
  def __init__(self, *args): # players, starting_chips
    self.suits = ("hearts", "diamonds", "spades", "clubs")
    self.players = args[0]
    if len(args) == 1:  # default setup variables ## move to new_game
      self.starting_chips = 1000 # £20 chips 2 1 75 25, 5 of each but not mainstream values

    else:               # custom setup variables
      self.starting_chips = args[1]
    
  def ResetDeck(self):
    self._deck = dict()
    self._hands = dict()
    for suit in self.suits:
      self._deck[suit] = [value for value in range(2,15)]
      # 2 - 14
    self._pickHistory = []
    self.totalcards = 5 + (self.players * 2)


  def PickCard(self, *quantity): #returns the suit.value of card as a string - if given a number, returns a list of cards
    if len(quantity) == 0:
      repeats = 1
    else:
      repeats = quantity[0]
    
    cards = []
    for i in range(repeats):
      randsuit = self.suits[random.randint(0,3)]
      randvalue = random.choice(self._deck[randsuit])   #finds random value out of remaining cards
      card = randsuit + "." + str(randvalue)
      self._pickHistory.append(card) 
      self._deck[randsuit].pop(self._deck[randsuit].index(randvalue)) ##used to be -1
      #removes card from deck
      if repeats == 1:
        return card
      cards.append(card)
    return cards
    

  def Deck(self): #returns dictionary
    return self._deck


  def PickHistory(self): # returns in list
    #test function to be used later
    #when returning, use split(".") to separate
    # lastcard = self._pickHistory[-1] 
    return self._pickHistory

  #action methods to be moved into subclass later
  def DrawCards(self): # draws cards for all players, including public 5 and adds to dictionary
    self._hands["public"] = self.PickCard(5)
    for i in range(1, self.players + 1): #adjusted
      self._hands[i] = self.PickCard(2)


  def GetHand(self, player): #returns hand of player in list form (public is the first, player keys start at 1)
    return self._hands[player]


  def GetPublicStage(self, stage): # returns public cards, takes stage 1-3 but stage 1 returns list
    public = self._hands["public"]  

    if stage == 1:
      return public[:3] 
    elif stage == 2:
      return public[3]
    elif stage == 3:
      return public[4]
    else:                   #error checking, remove later ###
      print("stage invalid")
      raise Exception
  

  def FindCombination(self, hand): # return list [rank, ch, ch, h] for value comparison
    combined = self._hands["public"] + hand
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

      for i in range(len(unique_values) * 2 - 4):
        current = int(loopedlist[i]) + 1
        next = int(loopedlist[i + 1])
        
        if current == next or (current == 15 and next == 2): # ace is 14, so + 1 would be 15 to account for loopback A-2 14-2
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

    
    def output(): 
      CH = straight()
      isflush = flush()  
      #ensure every returned value is a list
      #CH straight flush
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
    return output()


  def FindWinner(self, playerCombinations): # iterate through lists, comparing largest value
    remainingPlayers = playerCombinations
    for i in range(1,len(max(playerCombinations))): #length of longest list
      values = []
      for player in remainingPlayers:
        values.append(player[i])

      locations = [index for index, value in enumerate(values) if value == max(values)] #finds highest value in all lists and returns all occurences
      if len(locations) == 1 or i == len(remainingPlayers[0]) - 1: # second term of the winning list
        break

      temp = []
      for num in locations:
        temp.append(remainingPlayers[num])
      remainingPlayers = temp
    
    winners = []
    for num in locations:
      winners.append(remainingPlayers[num][0])
    return winners

    
# make a system for money: pot, big_blind_value, isDealer, each player's _chips_, 3 playerAction fold raise call
#winner, list for remaining players that decreases down to winner(s) to split with
# chips_left, isDealer, cards, hasFolded, isAllIn, combination_rank, combination_high, high_card(if applicable) 
#database table bot_settings risk, difficulty, strategy

#class 
  #def FinalStageWinner(combinations):
  


# database connection
class database():
  def __init__(self, *args):
    if len(args) == 0:
      self.filename = "save.db"
    else: # might be redundant
      self.filename = args[0] + ".db"
  

  def con_up(self): # takes filename, performs first-time setup if necessary
    if os.path.exists(self.filename):
      self.needsSetup = False

      if input("Save file found! Restore it? y/n: ") == "n": ###replace pygame
        os.remove(self.filename) # deletes file for new creation
        self.needsSetup = True
    else:
      print("Creating new save file")
      self.needsSetup = True
  
    con = sqlite3.connect(self.filename) # creates file if not found

    # can take datetime as filename, but long and may be inconsistent
    ##from datetime import datetime, date, time
    ##filename = "" 
    ##
    ##for value in datetime.now():
    ##  filename += value 
    if self.needsSetup: # sqlite has no bool data type, only integer 0,1 but recognises True and False
      cursor = con.cursor()
      cursor.execute('''
    CREATE TABLE Tbl_round (
      player_id TEXT PRIMARY KEY,
      chips_left INTEGER NOT NULL,
      dealer INTEGER NOT NULL, --bool
      cards TEXT 
    )
''') # set types and relational database structure
    

    else: #parse load functions
      pass
    con.commit()
    con.close()

  # add database modify functions
  #def RaiseBet(self, player_id, bet_amount):
  #def 

  # SELECT chips FROM table WHERE player


#def __init__(self):
  #  new_round.__init__():

# for stage in range(4): # stage 0 nothing is shown
#   new turn   and limit options after first bet


class templatePlayer(new_round): # inherit new_round init # might need to make a database sqlite3
  pass #bot
  
db = database()
db.con_up()



round1 = new_round(3)

round1.ResetDeck()
round1.DrawCards()
print(round1.Deck())
print(round1.PickHistory())

showdownPlayers = [1,2,3]
playerCombinations = []
for player in showdownPlayers:    #draw winners from database
  playerCombinations.append( [player] + [ int(x) for x in round1.FindCombination(round1.GetHand(player)) ] ) # add player number

print(round1.FindWinner(playerCombinations))

