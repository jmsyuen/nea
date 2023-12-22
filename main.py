import pokersim
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
  def loop(iterator, current_index, forward): # turns list into circular list, looping back and can reverse, returns new index
    if forward == False: #reverse
      if current_index <= 0:
        current_index = len(iterator) - 1
      else:
        current_index -= 1
      
    else:
      if current_index >= len(iterator) - 1:
        current_index = 0
      else:
        current_index += 1
    return current_index


  def round_stage(stage): #returns nothing to continue
    nonlocal pot
    round_player_index = current_round_player_index
    bet_matched = False #changes to true if all checked with no bet
    raised = False
    highest_bet = 0
    first_loop = True
    for player_id in player_dict:
      player_dict[player_id].ResetStageBet()
    
    if stage > 0: #show stage cards
      print(round.GetPublicStage(stage))
    elif stage == 0:
      big_blind_player_id = round_players[loop(player_dict, round_player_index, False)]
      small_blind_player_id = round_players[loop(player_dict, loop(player_dict, round_player_index, False), False)]
      print(f"big blind: {big_blind_player_id}, small blind: {small_blind_player_id}")
      # charge blinds, and add to pot and highest_bet
      highest_bet = player_dict[big_blind_player_id].Charge(big_blind)
      player_dict[small_blind_player_id].Charge(small_blind)
      pot += big_blind + small_blind    


    def all_other_players_all_in():
      return all(player_dict[player_id].AllIn for player_id in round_players if player_id != current_player_id)

    
    while len(round_players) > 1 and bet_matched == False: #iterate players in round_stage
      current_player_id = round_players[round_player_index]
      previous_charge = player_dict[current_player_id].PreviousCharge()
      print(f"{current_player_id} move")
      action = player_dict[current_player_id].GetChoice(highest_bet) #returns value if bet
      print(action)
      

      if type(action) == tuple: #allin
        first_loop = False
        action = action[1]

      if type(action) == int: #value has been returned  
        if action + previous_charge == highest_bet: # called
          first_loop = False
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

      if all_other_players_all_in():
        return round_players



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
  while not valid: ####replace with pygame and buttons instead of inputs
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
  while play_game: # iterate rounds
    #read to and write out every iteration 
    pot = 0
    small_blind = big_blind // 2
    #create player object dictionary
    if first_time:
      first_time = False
      player_dict = dict()
      for player_id_value in range(1, total_players_left + 1): ###replace with actual players left
        player_dict["player_" + str(player_id_value)] = pokersim.Player(chips_left) #add 
      current_round_player_index = random.randrange(0,len(player_dict)) #start on random player every new game
      current_game_player_index = current_round_player_index  #for full rotation of players to increase blinds
      #human always player_1
      current_round_player_index = 0 ###for testing ease REMOVE LATER
      
    
    round = pokersim.new_round(total_players_left, player_dict)

    #deal cards for remaining players
    round_players = []
    for player_id in player_dict:
      round_players.append(player_id)
      player_dict[player_id].NewCards(round.GetHand(player_id)) ###int(player_id.split("_")[-1]) 
      player_dict[player_id].ResetAllIn()
      print(f"{player_id} cards: {round.GetHand(player_id)}") ####testing function
      ###print(round.GetHand("player_1")) #get human uncomment when remove testing function

    
    #iterate stages and return list of finalists
    for stage in range(4):
      finalists = round_stage(stage)
      if type(finalists) == list:
        break
    
    #calculate winners from finalists
    if finalists is None:
      finalists = round_players
    
    if len(finalists) == 1:
      winners = finalists
    
    playerCombinations = []
    for finalist in finalists:    #draw winners from database
      #finalist_value = int(finalist.split("_")[-1])
      print(f"{finalist}:{round.GetHand(finalist)}")
      playerCombinations.append( [finalist] + [ int(x) for x in round.FindCombination(round.GetHand(finalist) + round.GetHand("public")) ] ) # get combination highs and append to list
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
            combination = "Straight"
          elif combination == 6:
            combination = "Flush"
          elif combination == 7:
            combination = "Full house"
            combination_high += ", " + str(value_to_name(player[3]))
          elif combination == 8:
            combination = "Four of a kind"
          elif combination == 9:
            combination = "Straight Flush"
          elif combination == 10:
            combination = "Royal Flush"
          
    print(f"winner: {winners} with a {combination_high} {combination}")
              
    
    #split pot  
    winnings = pot // len(winners)
    for winner in winners:
      print(player_dict[winner].Collect(winnings))

    
    #remove bust players
    for player in list(player_dict):
      if player_dict[player].ChipsLeft() == 0:
        total_players_left -= 1
        round_players.remove(player)
        player_dict.pop(player)
      

    ####replace with if save button is pressed in pygame
    save = input("Save? y/N:")
    #end game if one player left or human out (optional)
    if len(player_dict) < 2: ###or "player_1" not in round.players
      play_game = False
      print(f"{round_players[0]} remains.")

    elif len(save) != 0:
      play_game = False
      #write out
    
    current_round_player_index += 1 #iterate blinds
    if current_round_player_index > len(player_dict) - 1: 
      current_round_player_index = 0
    if current_round_player_index == current_game_player_index: #if full cycle of players, double blinds
      big_blind *= 2
      print("Blinds doubled")
    
    


if __name__ == "__main__": # runs if file is being executed rather than imported #run pygame
  NewGame()

  