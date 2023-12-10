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
      total_players_left = int(input("Enter number of computer opponents:")) + 1 #includes human, replace with pygame and specific buttons
      chips_left = int(input("Enter starting chips:")) # default £50
      big_blind = int(input("Enter starting big blind:"))
      #difficulty ranges from easiest to hardest inclusive all including the previous difficulties
      #remember to add to Player() call below
      valid = True
    except:
      pass 
  
  if default:
    total_players_left = 3
    chips_left = 5000 #£50 buy in chips interval bet of 0.5, for aesthetic only can be calculated easily, 5 chips 5,2,1,50 blinds left 2 of dealer
    big_blind = 100 #small blind is always half of big
  
  
  #game
  first_time = True

  play_game = True # new round
  while play_game: #quit if one player left/saving/human out
    #read to and write out every iteration 
    #save button available at start of every round
    #first time setup variable default checked
    round = pokersim.new_round(total_players_left)
    #create player object dictionary
    if first_time:
      first_time = False
      player_dict = dict()
      for player_id_value in range(1, total_players_left + 1): ###replace with actual players left
        player_dict["player_" + str(player_id_value)] = pokersim.Player([player_id_value, chips_left, big_blind]) #add 
    
    #deal cards for remaining players
    for player_id in player_dict:
      player_dict[player_id].NewCards(round.GetHand(int(player_id.split("_")[-1]) ))
      player_dict[player_id].ResetBet()

    
    #charge blinds later


    #cycle through players in order circular queue?
    current_player = "player_1" #start on random player every new game
    print(player_dict[current_player].GetChoice())
    #if "AllIn" or True:
    #if returnedbet > currentbet:
    #   singlebet = currentbet + returnedbet
    #    reraised = True
    #scenario if raised after you to call again
    #function to return if previously bet
    #pot += currentbet + newbet
    #scenario if bet raised twice before reaching you


    for i in range(1, round.players + 1):# testing function
      print(round.GetHand(i)) 


    #money system

    #actions check raise fold
    for j in range(round.players - 1): #for all the bots
      pass #assign player class

    #end game if one player left or human out (optional)
    #player_dict - bustPlayers
    save = False
    play_game = False #temp
    if round.players < 2:
      play_game = False
    
    


if __name__ == "__main__": # runs if file is being executed rather than imported #run pygame
  NewGame()
  #poker_game = PokerGame()
  #poker_game.play()
  


