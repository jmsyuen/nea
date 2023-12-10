import pokersim, bot

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
      #remember to add to Player() call below
      valid = True
    except:
      pass 
  
  #game
  play_game = True
  while play_game: #quit if one player left/saving/human out
    #save button available at start of every round

    if default: #first time setup
      round = pokersim.new_round(3)
      #starting_chips assign players
    else:
      round = pokersim.new_round(opponents + 1) #includes human  
      starting_chips = 5000
      big_blind = 100
      

    
    player_dict = dict() #contains cards
    for player_id_value in range(1, round.players + 1):
      player_dict["player_" + str(player_id_value)] = pokersim.Player(round.GetHand(player_id_value), player_id_value, starting_chips, big_blind) #add 
    print(player_dict)
    #start on random player every new game
    
    round.DrawCards()
    current_player = "player_1"
    
    for i in range(1, round.players + 1):
      print(round.GetHand(i)) #hide player hands later

    #assign blinds later
    #money system

    #actions check raise fold
    for j in range(round.players - 1): #for all the bots
      pass #assign player class

    #end game if one player left or human out (optional)
    save = False
    play_game = False #temp
    if round.players < 2:
      play_game = False
  #round methods



if __name__ == "__main__": # runs if file is being executed rather than imported #run pygame
  NewGame()
  #poker_game = PokerGame()
  #poker_game.play()
  pass


