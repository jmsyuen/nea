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
  #functions
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
      previous_charge = player_dict[current_player_id].PreviousCharge()
      action = player_dict[current_player_id].GetChoice(highest_bet) #returns value if bet
      print(action)
      nonlocal pot

      if type(action) == tuple: #allin
        first_loop = False
        action = action[1]

      if type(action) == int: #value has been returned  
        if action + previous_charge == highest_bet: # called
          pass  #works as 0 also counted as False
        
        elif action + previous_charge > highest_bet: #raised
          highest_bettor_index = round_player_index # loop back to highest_bettor
          highest_bet = action + previous_charge
          raised = True
        pot += action #add to pot


          

      elif action == True or action == "AllIn": #check
        first_loop = False
        

      elif action == False: #fold
        round_players.remove(current_player_id) #removes based on value not index
        round_player_index -= 1


      #iterate players
      if len(round_players) == 1: #one player left
        return round_players
      elif round_player_index > len(round_players): #loop back in a circle
        round_player_index = 0  
      
      else: #cycle if bet has been made
        round_player_index = (round_player_index + 1) % len(round_players)  
        if raised == True: #if a higher bettor exists 
          if highest_bet != 0 and round_player_index == highest_bettor_index: #if looped back to new bettor
            bet_matched = True
            raised = False
        
        else: 
          if round_player_index == current_round_player_index: # continue after full circle made
            if first_loop == True:
              first_loop = False
            elif first_loop == False:
              break
        #add another loop for highest_bet, might break if highest bettor folds after raising###
    

  def value_to_name(value): # convert card values to their name
    #convert face values to names
    if value == 14:
      return "Ace"
    elif value == 13:
      return "King"
    elif value == 12:
      return "Queen"
    elif value == 11:
      return "Jack"
    else:
      return value




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
    #human always player_1

    
    pot = 0



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
    
    

    #output combinations with their values
    for winner in winners:
      for player in playerCombinations:
        if player[0] == winner:
          combination = player[1]
          combination_high = str(value_to_name(player[2]))
          
          #convert to combination names
          if combination == 1:
            combination = "High Card"
          elif combination == 2:
            combination = "Pair"
          elif combination == 3:
            combination = "Two Pair"
            combination_high += ", " + str(value_to_name(player[3]))
          elif combination == 4:
            combination = "Three of a kind"
          elif combination == 5:
            combination = "high Straight"
          elif combination == 6:
            combination = "high Flush"
          elif combination == 7:
            combination = "Full house"
            combination_high += ", " + str(value_to_name(player[3]))
          elif combination == 8:
            combination = "Four of a kind"
          elif combination == 9:
            combination = "high Straight Flush"
          elif combination == 10:
            combination = "Royal Flush"
          
          
    print(f"winner: {winners} with a {combination_high} {combination}")
              
    
    #split pot  
    winnings = pot // len(winners)
    for winner in winners:
      print(player_dict[winner].Collect(winnings))


    
    #player_dict - bustPlayers
    for player in player_dict:
      if player_dict[player].ChipsLeft() == 0:
        total_players_left -= 1
        players_to_remove = []
    
    for player in players_to_remove:
      player_dict.pop(player)

    ##replace with if save button is pressed
    save = input("Save? y/N:")
    #end game if one player left or human out (optional)
    if len(round_players) < 2: #or "player_1" not in round.players
      play_game = False
      print(f"{round_players[0]} remains.")
    elif len(save) != 0:
      play_game = False
      #write out
    
    


if __name__ == "__main__": # runs if file is being executed rather than imported #run pygame
  NewGame()
  #poker_game = PokerGame()
  #poker_game.play()
  