import pokersim, bot
import random
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
    round_players = []
    for player_id in player_dict:
      round_players.append(player_id)
      player_dict[player_id].NewCards(round.GetHand(int(player_id.split("_")[-1]) ))
      player_dict[player_id].ResetAllIn()
    
    #charge blinds later


    #print(round.GetHand(1)) #get human uncomment when remove testing function
    for i in range(1, round.players + 1):# testing function
      print(f"player_{i} cards: {round.GetHand(i)}") 
    
    
    current_round_player_index = random.randrange(0,len(round_players)) #start on random player every new game
    current_round_player_index = 0 ###for testing ease REMOVE LATER
    
    pot = 0

    def round_stage(stage): #returns nothing to continue
      round_player_index = current_round_player_index
      bet_matched = False #changes to true if all checked with no bet
      raised = False
      highest_bet = 0
      first_loop = True
      for player_id in player_dict:
        player_dict[player_id].ResetStageBet()
      
      if stage > 0: #show stage cards
        print(round.GetPublicStage(stage))

      
      while len(round_players) > 1 and bet_matched == False: #iterate players in round_stage
        current_player_id = round_players[round_player_index]
        action = player_dict[current_player_id].GetChoice(highest_bet) #returns value if bet
        print(action)
        remaining_counter = len(round_players)
      
        if type(action) == int: #value has been returned  
          if action == highest_bet: # called
            pass
         
          elif action > highest_bet: #raised
            highest_bettor_index = round_player_index # loop back to highest_bettor
            highest_bet = action
            remaining_counter = len(round_players) 
          nonlocal pot
          pot += action #add to pot

          
        else: 
          if action == True or action == "AllIn": #check
            first_loop = False
            pass

          elif action == False: #fold
            round_players.remove(current_player_id) #removes based on value not index
            round_player_index -= 1


        if len(round_players) == 1: #one player left
          return round_players
        elif round_player_index > len(round_players): #loop back in a circle
          round_player_index = 0  
        
        else: #cycle if bet has been made
          round_player_index = (round_player_index + 1) % len(round_players)
          if remaining_counter > 0:
            remaining_counter -= 1
            
          elif remaining_counter == 0: #if a higher bettor exists 
            if highest_bet != 0 and round_player_index == highest_bettor_index: #if looped back to new bettor
              bet_matched = True
              break
            elif round_player_index == current_round_player_index: # continue after full circle made
              if first_loop == True:
                first_loop = False
              elif first_loop == False:
                break
            
           
          
          #add another loop for highest_bet, might break if highest bettor folds after raising###
      

    #iterate stages and return list of finalists
    for stage in range(4):
      finalists = round_stage(stage)
      if type(finalists) == list:
        print(finalists)
        break
    
    #calculate winners from finalists
    if finalists is None:
      finalists = round_players
    
    if len(finalists) == 1:
      winners = finalists
    else: 
      playerCombinations = []
      for finalist in finalists:    #draw winners from database
        finalist_value = int(finalist.split("_")[-1])
        print(f"{finalist}:{round.GetHand(finalist_value)}")
        playerCombinations.append( [finalist] + [ int(x) for x in round.FindCombination(round.GetHand(finalist_value)) ] ) # get combination highs and append to list
      winners = round.FindWinner(playerCombinations)  #compare values in the list and decide winner or draw
    print(f"winner: {winners}")
    
    #split pot  
    winnings = pot // len(winners)
    for winner in winners:
      print(player_dict[winner].Collect(winnings))


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
  


