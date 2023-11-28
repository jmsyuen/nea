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

# database connection

class database():
  def __init__(self, *args):
    if len(args) == 0:
      self.filename = "data.db"
      self.needsSetup = True
    else:
      self.filename = args[0] + ".db"
      self.needsSetup = False
  


    

  def con_up(self): # takes filename, performs first-time setup if necessary
    con = sqlite3.connect(self.filename)
    
    # can take datetime as filename, but long and may be inconsistent
    ##from datetime import datetime, date, time
    ##filename = "" 
    ##
    ##for value in datetime.now():
    ##  filename += value
    if self.needsSetup:
      cursor = con.cursor()
      cursor.execute("CREATE TABLE main (tables TEXT, players TEXT)") # set types and relational database structure

    else: #parse load functions
      pass

    

  #try:
  #  sqlite3.function
  #except Error as error:
  #  print(f"The error '{error}' occurred")

  def con_close(self):
    if os.path.exists(self.filename):
      os.remove(self.filename)
    else:
      print("The file does not exist")
  
  # add database modify functions
  



# make a system for money: pot, blind_value, each player's _chips_, 3 actions fold raise call


#def __init__(self):
  #  new_round.__init__():


class templatePlayer(new_round): # inherit new_round init # might need to make a database sqlite3
  pass
  
db = database()
db.con_up()
db.con_close()


round1 = new_round(5)

round1.DrawCards()
print(round1.Deck())
print(round1.PickHistory())
print(round1.GetHand(1))
print(round1.GetPublicStage(1))
