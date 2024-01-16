import random
import os
import sqlite3
from sqlite3 import Error #

# one tag is useful comments
## two tags for code clips
### three tags for issues
#### important notes or testing clips
# cards ranked from Ace 2 3 ... 10 Jack Queen King
# use special behaviour of number 1 to define the high value of it / use ace as the highest value in the list
# randint is inclusive of both limits
# range is inclusive of first value only eg. 1,14 is 1-13
# to unpack a list use asterisk before variable print(*list)
# changed to 2-14 for ace high
# * to unpack lists



class new_round(): # money system, carry over chips,  beginning of round, sub class
  def __init__(self, players, player_dict): # players, starting_chips
    self.suits = ("hearts", "diamonds", "spades", "clubs")
    self.players = players
    self.player_dict = player_dict
      
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
    for player_id in player_dict: #adjusted
      self.__hands[player_id] = self.PickCard(2)


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
  
  def GetHand(self, player_id): #returns hand of player in list form (public is the first, player keys start at 1)
    return self.__hands[player_id]


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
  

  def FindCombination(self, cards): # return list [rank, ch, ch, h] for value comparison
    combined = cards
    suits, values = [], []
    allsuits = ("hearts", "diamonds", "spades", "clubs") # repeated as inherited in bot()

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
        return sorted(set(combination_highs), key=int, reverse=True)
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
          return [10, 14]
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
        print("Creating new save file")
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


class Player(): 
  def __init__(self, chips_left): # takes hands, player_id/arguments including player_id
    self.chips_left = chips_left
    self.bot = False


  def NewCards(self, new_hand):
    self.__hand = new_hand

  def GetHand(self):
    return self.__hand

  
  def Charge(self, amount): #returns amount taken
    if amount > self.chips_left:
      return False
    self.total_stage_bet += amount
    self.chips_left -= amount
    return amount
    

  def Collect(self, amount):
    self.chips_left += amount
    return amount


  def ResetAllIn(self):
    self.AllIn = False


  def ResetStageBet(self):
    self.total_stage_bet = 0


  def PreviousCharge(self):
    if self.total_stage_bet > 0:
      return self.total_stage_bet
    return 0


  def ChipsLeft(self):
    return self.chips_left

  
  def GetChoice(self, highest_bet): #current bet to call #check if returned amount matches bet to determine a reraise
    #returns True to continue, False if folded, "AllIn" if has less than bet, total bet value if raise
    if self.AllIn: #persistent
      return "AllIn"
    
    if highest_bet == 0:
      if self.bot == True:
        choice = self.BotChoice(highest_bet, "fold check bet") ###
      else:
        choice = input("Fold(n), Check(y), 3.Bet(amount in 50p intervals):") ##set hard limit slider at remaining chips and 50p intervals

      if choice.isnumeric():
        choice = int(choice)
        if choice == self.chips_left:
          result = self.Charge(self.chips_left)
          self.AllIn = True
          return "AllIn", result
        
        result = self.Charge(choice) 
        ###TESTING
        if result == False: ### testing remove 4 lines later
          print("not enough chips(test)")
          return True
        ###TESTING
        return result
      
      if choice == "y": #check
        return True
      if choice == "n": #fold
        return False

    else: #bet has been made
      if highest_bet >= self.chips_left:
        if self.bot == True:
          choice = self.BotChoice(highest_bet, "fold allin") ###
        else:
          choice = input("All in (y) or fold(n)?:")

        if choice == "y":
          result = self.Charge(self.chips_left)
          self.AllIn = True
          return "AllIn", result
        else:
          return False
      
      elif highest_bet > 0:
        if self.bot == True:
          choice = self.BotChoice(highest_bet, "fold call raise") ###
        else:
          choice = input("Fold(n), Call(y) or raise extra:")

        previouscharge = self.PreviousCharge()
        if previouscharge != False:
          highest_bet -= previouscharge #deduct already input chips
        
        if choice == "y":
          self.Charge(highest_bet)
          return highest_bet
        elif choice == "n":
          return False
        else:
          extra_raise = int(choice)
          return self.Charge(highest_bet + extra_raise)  #new extra bet


class Bot(new_round, Player): #inherits functions of new_round 
  def __init__(self, chips_left, difficulty):
    Player.__init__(self, chips_left)
    self.risk = 0.5  #0-1 the probability threshold for a card to appear which would be accepted 
    self.difficulty = difficulty  #easy, med, hard - how genuinely smart the bot is
    #chance of fold/check/bet in ranges of probabilities
    #get and use highest_bet to determine next action
    #replace player objects in player_dict with bot() objects
    #use same GetAction() functions as player() class in order to implement later
    self.bot = True

  #carried over from player() class
  def NewCards(self, new_hand):
    self.__hand = new_hand


  def BotChoice(self, highest_bet, available_choices):
    #if difficulty, risk
    choice = self.Strategy1(highest_bet, available_choices)
    return choice


  def Calculate(self, stage): # more vars
    pass
    #calculate if next is a pair, a 
    #for every card not in currently known, calculate next card achieving that combination
    #therefore probability of each combination with the current hand
    #consider integration with pokersim findCombination() functions which will require importing

  def StartingHand(self): #outputs rankings of 1-53 with 1 highest #also take difficulty
    
    hand_attributes = []  #if onsuit, pair, high face value etc
    onsuit_rankings = []
    offsuit_rankings = []
    
    #split suit and values, sort value1 > value2
    suit1, value1 = self.__hand[0].split(".")
    suit2, value2 = self.__hand[1].split(".")
    if int(value1) > int(value2): #
      suit1, value1 = self.__hand[1].split(".")
      suit2, value2 = self.__hand[0].split(".")    
    value1, value2 = int(value1), int(value2) #force int

    #assign variables to match certain commbinations
    onsuit = False
    pair = False
    consecutive = False
    consecutive_potential = 0 #how many cards needed to be consecutive, or rank from 5 highest
    face_values = [face_value for face_value in range(11,15)]
    face_value_total = 0


    if suit1 == suit2:
      onsuit = True
    elif value1 == value2:
      pair = True
          
    if value1 - value2 == 1:
      consecutive = True
    elif value1 - value2 <= 4:
      consecutive_potential = value1 - value2
    if value1 in face_values:
      face_value_total += 1
    if value2 in face_values:
      face_value_total += 1
    
    hand_attributes.append((onsuit, pair, consecutive, consecutive_potential))
    
    #dict for how high ranges of pairs, consecutive



    def Ranking1(): #set rankings from table
      pass

    def Ranking2(): #calculate possible combinations
      pass
      


  def RollRisk(self, probability):
    pass  #change

  def Strategy1(self, highest_bet, available_choices): #equal chance of any option
    #pickrandom choice, pickrandom bet 
    choice = random.choice(available_choices.split(" "))
    
    if choice == "fold":
      return "n"
    if choice == "allin" or "call" or "check":
      return "y"

    if choice == "raise":
      raise_value = random.randrange(50, self.chips_left, 50) 
      #float(highest_bet)/float(self.chips_left)  #fraction of your money is the bet, use for later logic
      return raise_value


  def Strategy2(self, highest_bet, available_choices):
    if available_choices == "fold check raise":
      print("fold check raise")
      if True:  # bet
        return 10
      if True:  # check
        return "y"
      if True:  # fold
        return "n"
      
    elif available_choices == "fold allin":
      print("fold allin")
      if True:  # all in
        return "y"
      if True:  # fold
        return "n"
    elif available_choices == "fold call raise":
      print("fold call raise")
      if True:  # raise
        return 10
      if True:  # call
        return "y"
      if True:  # fold
        return "n"   
        


if __name__ == "__main__":
  
  hand = ["hearts.14", "spades.14"]
  bot1 = Bot(5000, 1, "easy")
  
  bot1.NewCards(hand)
  bot1.ResetAllIn()
  bot1.ResetStageBet()


  bot1.StartingHand()
  print(bot1.GetChoice(500))
  print(bot1.AllIn)
  print(bot1.Charge(100))






  '''
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
  '''

