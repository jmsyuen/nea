import random
import os
import sqlite3
from sqlite3 import Error


# one tag is useful comments
## two tags for code clips
### three tags for issues
# 3 tags at the end for testing, remove later ###
# cards ranked from Ace 2 3 ... 10 Jack Queen King
# use special behaviour of number 1 to define the high value of it / use ace as the highest value in the list
# randint is inclusive of both limits
# range is inclusive of first value only eg. 1,14 is 1-13
# to unpack a list use asterisk before variable print(*list)


class new_round():
  def __init__(self, *args): # players, buyIn
    self.suit = ("hearts","diamonds","spades","clubs")
    self._deck = dict()
    self._hands = dict()
    for suit in self.suit:
      self._deck[suit] = [value for value in range(1,14)]
      # 1 - 13
    self._pickHistory = []
    self.players = args[0]
    self.totalcards = 5 + (args[0] * 2)
    if len(args) == 1:  # default setup variables
      self.buyIn = 1000 # £20 chips 2 1 75 25, 5 of each but not mainstream values

    else:               # custom setup variables
      self.buyIn = args[1]
    
    
  def Pick_card(self, *quantity): #returns the suit;value of card as a string - if given a number, returns a list of cards
    if len(quantity) == 0:
      repeats = 1
    else:
      repeats = quantity[0]
    
    cards = []
    for i in range(repeats):
      randsuit = self.suit[random.randint(0,3)]
      randvalue = random.choice(self._deck[randsuit])
      #finds random value out of remaining cards
      card = randsuit + ";" + str(randvalue)
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
    #when returning, use split(";") to separate
    lastcard = self._pickHistory[-1]
    return self._pickHistory

  #action methods to be moved into subclass later
  def DrawCards(self): # draws cards for all players, including public 5 and adds to dictionary
    self._hands["public"] = self.Pick_card(5)
    for i in range(1, self.players + 1): #adjusted
      self._hands[i] = self.Pick_card(2)

  

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

# make a system for money: pot, big_blind_value, isDealer, each player's _chips_, 3 playerAction fold raise call
#winner, list for remaining players that decreases down to winner(s) to split with
# chips_left, isDealer, cards, hasFolded, isAllIn, combination_rank, combination_high, high_card(if applicable) 
#database table bot_settings risk, difficulty, strategy


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

      if input("Save file found! Restore it? y/n") == "n": ###replace pygame
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


class templatePlayer(new_round): # inherit new_round init # might need to make a database sqlite3
  pass
  
db = database()
db.con_up()



round1 = new_round(5)

round1.DrawCards()
print(round1.Deck())
print(round1.PickHistory())
print(round1.GetHand(1))
print(round1.GetPublicStage(1))
