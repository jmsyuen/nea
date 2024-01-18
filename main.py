import pokersim
import gui

import random
import pygame

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


  def round_stage(stage): 
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
      gui.show_hand("public", round.GetPublicStage(stage), stage)
    elif stage == 0:
      big_blind_player_id = round_players[loop(player_dict, round_player_index, False)]
      small_blind_player_id = round_players[loop(player_dict, loop(player_dict, round_player_index, False), False)]
      print(f"big blind: {big_blind_player_id}, small blind: {small_blind_player_id}")
      gui.update_player_info(big_blind_player_id, "Big Blind")
      gui.update_player_info(small_blind_player_id, "Small Blind")
      # charge blinds, and add to pot and highest_bet
      highest_bet = player_dict[big_blind_player_id].Charge(big_blind)
      player_dict[small_blind_player_id].Charge(small_blind)
      pot += big_blind + small_blind
      gui.update_pot(pot)


    while len(round_players) > 1 and bet_matched == False: #iterate players in round_stage
      current_player_id = round_players[round_player_index]
      previous_charge = player_dict[current_player_id].PreviousCharge()
      print(f"{current_player_id} move")
      gui.turn_indicator(current_player_id)
      
      action = player_dict[current_player_id].GetChoice(highest_bet) #returns value if bet
      print(action) # print into player info box
  
      
      if type(action) == tuple: #allin
        first_loop = False
        action = action[1]
        gui.update_player_info(current_player_id, "All In", player_dict[current_player_id].ChipsLeft())

      elif type(action) == int: #value has been returned  
        if action + previous_charge == highest_bet: # called
          first_loop = False
          gui.update_player_info(current_player_id, "Call", player_dict[current_player_id].ChipsLeft())
          #works as 0 also counted as False
        
        elif action + previous_charge > highest_bet: #raised
          highest_bettor_index = round_player_index # loop back to highest_bettor
          highest_bet = action + previous_charge
          raised = True 
          gui.update_player_info(current_player_id, f"Raise {action}", player_dict[current_player_id].ChipsLeft())
        pot += action #add to pot
        gui.update_pot(pot)

      elif action == True: #check
        first_loop = False
        gui.update_player_info(current_player_id, "Check", player_dict[current_player_id].ChipsLeft())

      elif action == "AllIn":
        first_loop = False
        gui.update_player_info(current_player_id, "All In", player_dict[current_player_id].ChipsLeft())
        
      elif action == False: #fold
        round_players.remove(current_player_id) #removes based on value not index
        round_player_index -= 1
        gui.update_player_info(current_player_id, "Fold", player_dict[current_player_id].ChipsLeft())
        

      if all(player_dict[player_id].AllIn for player_id in round_players if player_id != current_player_id):  #all other players are all in
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
        
    

 
  db = pokersim.database()
  db.con_up()
  
  print("Starting with default settings. £50 bot buy in, 3 opponents, medium bot difficulty.")
  #remember to add to Player() call below

  
  total_players_left, difficulty, bot_starting_chips = gui.GetSettings()
  gui.draw_game(bot_starting_chips, total_players_left - 1)
  big_blind_cycle = 0   #used to know when to double blinds every two cycles of players
  big_blind = 100
  gui.update_blinds(100)      #small blind is always half of big

  #initiate player and bot objects
  player_dict = dict()
  player_dict["player_1"] = pokersim.Player(5000)
  for player_id_value in range(2, total_players_left + 1):
    player_dict["player_" + str(player_id_value)] = pokersim.Bot(bot_starting_chips, difficulty) #add bots
  current_round_player_index = random.randrange(0,len(player_dict)) #start on random player every new game
  current_game_player_index = current_round_player_index  #for full rotation of players to increase blinds
  #human always player_1
  current_round_player_index = 0 ###for testing ease REMOVE LATER
  
  
  ### game  ###
  
  play_game = True # new round
  while play_game: # iterate rounds
    #read to and write out every iteration (database)
    pot = 0
    gui.update_pot(pot)
    small_blind = big_blind // 2    
      
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
      finalists = round_stage(stage)  #returns nothing to continue
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
    if current_round_player_index == current_game_player_index and big_blind < 1600 and big_blind_cycle != 0: #double blinds up to a maximum of 1600 every two cycles
      big_blind *= 2
      big_blind_cycle += 1
      print("Blinds doubled")
    
    pygame.display.flip()
    
    
    
    
    
    


if __name__ == "__main__": 
  pygame.init()
  clock = pygame.time.Clock()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        gui.quit()
    
    menu = gui.GetMenu()

    if menu == "game_lock":
      NewGame()
    else:  
      if menu == "main menu":
        gui.main_menu()
      elif menu == "settings":
        gui.settings()
      elif menu == "help":
        gui.help()
      elif menu == "game":
        gui.ChangeMenu("game_lock")
        gui.ClearScreen() 
        
  
    clock.tick(30)  #frame limit
  

  