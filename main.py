import pokersim

''' maybe move into pokersim.py, and create new sqlite file
import sqlite3
from sqlite3 import Error

def initiate_connection(path):
  con = None
  try:
    con = sqlite3.connect(path)
    print("connected")
  except Error as error:
    print(f"The error '{error}' occurred")

  return con
'''

#save file if found on first startup message
# print("Save file found! Restore it?")
# else reset 

#class new_game(): # new round, get chip carry over return # in main.py
  #bot difficulty select
  #round settings
  
  #pass


# nea
def NewGame(players, buyIn, startingblinds):
  valid = False
  while not valid:
    try:
      players = int(input("Enter number of players:")) # replace with pygame and specific buttons
      buyIn = int(input("Enter buy in value for each player"))

      valid = True
    except:
      pass 
  #game
  round = pokersim.new_round(players)

  round.ResetDeck()
  round.DrawCards()
  print(round.Deck())
  print(round.PickHistory())
  #round methods

print(pokersim.round1.Deck())

if __name__ == "__main__": # runs if file is being executed rather than imported #run pygame
  #poker_game = PokerGame()
  #poker_game.play()
  pass


