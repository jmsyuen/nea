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
# changed to 2-14 for ace high
# * to unpack lists



class new_round(): # money system, carry over chips,  beginning of round, sub class
  def __init__(self, players): # players, starting_chips
    self.suits = ("hearts", "diamonds", "spades", "clubs")
    self.players = players
      
  #def ResetDeck(self):
    self.__deck = dict()
    self.__hands = dict()
    for suit in self.suits:
      self.__deck[suit] = [value for value in range(2,15)]
      # 2 - 14
    self.__pickHistory = []
    self.totalcards = 5 + (self.players * 2)

  #def DrawCards(self): # draws cards for all players, including public 5 and adds to dictionary
    self.__hands["public"] = self.PickCard(5)
    for i in range(1, self.players + 1): #adjusted
      self.__hands[i] = self.PickCard(2)


  def PickCard(self, *quantity): #returns the suit.value of card as a string - if given a number, returns a list of cards
    if len(quantity) == 0:
      repeats = 1
    else:
      repeats = quantity[0]
    
    cards = []
    for i in range(repeats):
      randsuit = self.suits[random.randint(0,3)]
      randvalue = random.choice(self.__deck[randsuit])   #finds random value out of remaining cards
      card = randsuit + "." + str(randvalue)
      self.__pickHistory.append(card) 
      self.__deck[randsuit].pop(self.__deck[randsuit].index(randvalue)) ##used to be -1
      #removes card from deck
      if repeats == 1:
        return card
      cards.append(card)
    return cards
    

  def Deck(self): #returns dictionary
    return self.__deck #testing function


  def PickHistory(self): # returns in list
    #test function to be used later
    #when returning, use split(".") to separate
    # lastcard = self.__pickHistory[-1] 
    return self.__pickHistory

  #action methods to be moved into subclass later
  
  def GetHand(self, player): #returns hand of player in list form (public is the first, player keys start at 1)
    return self.__hands[player]


  def GetPublicStage(self, stage): # returns public cards, takes stage 1-3 but stage 1 returns list
    public = self.__hands["public"]  

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
    combined = self.__hands["public"] + hand
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



# database connection should go in main.py
class database(): #takes save file name 
  def __init__(self, *args):
    if len(args) == 0: 
      self.filename = "save.db"
    else: # might be redundant
      self.filename = args[0] + ".db"
  

  def con_up(self): # takes filename, performs first-time setup if necessary
    if os.path.exists(self.filename):
      self.needsSetup = False

      if input("Save file found! Restore it? y/N: ") != "y": ###replace pygame
        os.remove(self.filename) # deletes file for new creation, need to restart sqlite explorer to view
        self.needsSetup = True
    else:
      print("Creating new save file")
      self.needsSetup = True
  
    con = sqlite3.connect(self.filename) # creates file if not found


    if self.needsSetup: # sqlite has no bool data type, only integer 0,1 but recognises True and False
      cursor = con.cursor() # save data and fetch between new rounds
      cursor.execute('''
    CREATE TABLE Tbl_players (
      player_id TEXT PRIMARY KEY,
      chips_left INTEGER NOT NULL,
      dealer INTEGER NOT NULL --bool
    )
''') # set types and relational database structure
      
      #can add more
      cursor.execute('''
    CREATE TABLE Tbl_bot_settings (
      bot_id TEXT PRIMARY KEY,
      risk INTEGER NOT NULL,
      difficulty INTEGER NOT NULL,
      strategies TEXT                   
    )
''') # strategies may be list

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


class Player(): 
  def __init__(self, args): # takes hands, player_id/arguments including player_id
    self.player_id_value, self.chips_left, self.big_blind = args    


  def NewCards(self, new_hand):
    self.__hand = new_hand

  def GetHand(self):
    return self.__hand

  
  def Charge(self, amount): #returns amount taken
    if amount > self.chips_left:
      return False
    self.total_round_bet += amount
    self.chips_left -= amount
    return amount
    

  def Collect(self, amount):
    self.chips_left += amount
    return amount


  def ResetBet(self):
    self.total_round_bet = 0
    self.AllIn = False


  def PreviousCharge(self):
    if self.total_round_bet > 0:
      return self.total_round_bet
    return False

  
  def GetChoice(self, bet): #current bet to call #check if returned amount matches bet to determine a reraise
    #returns True to continue, False if folded, "AllIn" if has less than bet, total bet value if raise
    if self.AllIn: #persistent
      return "AllIn"
    
    if bet == 0:
      choice = input("Fold(n), Check(y), 3.Bet(amount in 50p intervals):") ##set hard limit slider at remaining chips and 50p intervals
      if choice.isnumeric():
        if choice == self.chips_left:
          result = self.Charge(self.chips_left)
          self.AllIn = True
          return result
        
        result = self.Charge(int(choice)) 
        ###TESTING
        if result == False: ### testing remove 4 lines later
          print("not enough chips(test)")
        ###TESTING
        return result
      
      if choice == "y": #check
        return True
      if choice == "n": #fold
        return False

    else: #bet has been made
      if bet >= self.chips_left:
        choice = input("All in (y) or fold(n)?:")
        if choice == "y":
          self.Charge(self.chips_left)
          self.AllIn = True
          return "AllIn"
        else:
          return False
      
      elif bet > 0:
        choice = input("Fold(n), Call(y) or raise extra:")

        previouscharge = self.PreviousCharge()
        if previouscharge != False:
          bet -= previouscharge #deduct already input chips
        
        if choice == "y":
          self.Charge(bet)
          return True
        elif choice == "n":
          return False
        else:
          choice = int(choice)
          return self.Charge(bet + choice)  #new extra bet




if __name__ == "__main__":
  db = database()
  db.con_up()
  round1 = new_round(3)

  print(round1.Deck())
  print(round1.PickHistory())

  showdownPlayers = [1,2,3]
  playerCombinations = []
  for player in showdownPlayers:    #draw winners from database
    playerCombinations.append( [player] + [ int(x) for x in round1.FindCombination(round1.GetHand(player)) ] ) # add player number

  print(round1.FindWinner(playerCombinations))

