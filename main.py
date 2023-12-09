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
def NewGame():
  valid = False
  while not valid: #replace with pygame and buttons instead of inputs
    try:
      db = pokersim.database()
      db.con_up()


      default = False
      if not input("Starting with default settings. £50 buy in, 2 opponents, medium bot difficulty. Type anything to customise:"):
        default = True
        break
      opponents = int(input("Enter number of computer opponents:")) # replace with pygame and specific buttons
      starting_chips = int(input("Enter starting chips:")) # default £50
      big_blind = int(input("Enter starting big blind:"))
      #difficulty ranges from easiest to hardest inclusive all including the previous difficulties
      valid = True
    except:
      pass 
  
  #game
  play_game = True
  while play_game:
    #save button available at start of every round


    if default:
      round = pokersim.new_round(default)
    else:
      round = pokersim.new_round(opponents + 1, starting_chips) #includes human
      
      

    round.ResetDeck()
    round.DrawCards()
    print(round.Deck())
    print(round.PickHistory())

    #end game if one player left or human out (optional)
    save = False
    print(round.players)
    if round.players < 2:
      play_game = False
  #round methods

print(pokersim.round1.Deck())

if __name__ == "__main__": # runs if file is being executed rather than imported #run pygame
  NewGame()
  #poker_game = PokerGame()
  #poker_game.play()
  pass


