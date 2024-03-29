import pokersim
import gui

import random
import time
import pygame

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

  
  def Convert_Value_To_Name(value): # convert card values to their name
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

  def Convert_Combination_To_Name(combination):
    if combination == 1:
      return "High Card"
    elif combination == 2:
      return "Pair"
    elif combination == 3:
      return "Two Pair"
    elif combination == 4:
      return "3 of a kind"
    elif combination == 5:
      return "Straight"
    elif combination == 6:
      return "Flush"
    elif combination == 7:
      return "Full house"
    elif combination == 8:
      return "Four of a kind"
    elif combination == 9:
      return "Straight Flush"
    elif combination == 10:
      return "Royal Flush"

  def Play_Round_Stage(stage): 
    nonlocal pot, current_round_player_index
    if current_round_player_index > len(round_players) - 1:
      current_round_player_index = len(round_players) - 1
    round_player_index = current_round_player_index
  
    bet_matched = False #changes to true if all checked with no bet
    raised = False
    highest_bet = 0
    first_loop = True
    player_iterations = 0
    for player_id in player_dict:
      player_dict[player_id].ResetStageBet()
    

    if stage > 0: #show stage cards
      print(round.GetPublicStage(stage))
      gui.ShowHand("public", round.GetPublicStage(stage), stage)
      
      revealed_cards = []
      for i in range(1, stage + 1):
        if type(round.GetPublicStage(i)) != list:
          revealed_cards.append(round.GetPublicStage(i))
        else:
          revealed_cards += list(round.GetPublicStage(i))

    elif stage == 0:
      big_blind_player_id = round_players[loop(player_dict, round_player_index, False)]
      small_blind_player_id = round_players[loop(player_dict, loop(player_dict, round_player_index, False), False)]
      print(f"big blind: {big_blind_player_id}, small blind: {small_blind_player_id}")
      gui.UpdatePlayerInfo(big_blind_player_id, "Big Blind")
      gui.UpdatePlayerInfo(small_blind_player_id, "Small Blind")
      # charge blinds, and add to pot and highest_bet
      highest_bet = player_dict[big_blind_player_id].Charge(big_blind)
      player_dict[small_blind_player_id].Charge(small_blind)
      pot += big_blind + small_blind
      gui.UpdatePot(pot)
      revealed_cards = []


    while len(round_players) > 1 and bet_matched == False and player_iterations < 25: #iterate players in Play_Round_Stage
      player_iterations += 1
      current_player_id = round_players[round_player_index]
      previous_charge = player_dict[current_player_id].GetPreviousCharge()
      print(f"{current_player_id} move")
      gui.UpdateTurnIndicator(current_player_id)
      gui.UpdatePlayerInfo(current_player_id, "Thinking..")
      

      action = player_dict[current_player_id].GetChoice(highest_bet, revealed_cards) #returns value if bet
      print(action) # print into player info box
      pygame.display.flip()
      pygame.time.wait(random.randint(5,10) * 100) #time in ms
  
      ##logic to decode action
      if type(action) == tuple: #allin
        first_loop = False
        action = action[1]  # action here is extra raise
        if action > 0:
          highest_bet += action
          highest_bettor_index = round_player_index 
          raised = True 
        gui.UpdatePlayerInfo(current_player_id, "All In", player_dict[current_player_id].GetChipsLeft())
        pot += action #add to pot
        gui.UpdatePot(pot)

      elif type(action) == int: #value has been returned  
        if action + previous_charge == highest_bet: # called
          first_loop = False
          gui.UpdatePlayerInfo(current_player_id, "Call", player_dict[current_player_id].GetChipsLeft())
          #works as 0 also counted as False
        
        elif action + previous_charge > highest_bet: #raised
          highest_bettor_index = round_player_index # loop back to highest_bettor
          raised = True 
          highest_bet = action + previous_charge
          gui.UpdatePlayerInfo(current_player_id, f"Raise {action}", player_dict[current_player_id].GetChipsLeft())
        pot += action #add to pot
        gui.UpdatePot(pot)

      elif action == True: #check
        first_loop = False
        gui.UpdatePlayerInfo(current_player_id, "Check", player_dict[current_player_id].GetChipsLeft())

      elif action == "AllIn":
        first_loop = False
        gui.UpdatePlayerInfo(current_player_id, "All In", player_dict[current_player_id].GetChipsLeft())
        
      elif action == False: #fold
        round_players.remove(current_player_id) #removes based on value not index
        round_player_index -= 1
        if current_round_player_index > len(round_players) - 1:
          current_round_player_index = len(round_players) - 1
        gui.UpdatePlayerInfo(current_player_id, "Fold", player_dict[current_player_id].GetChipsLeft())
        

      if all(player_dict[player_id].AllIn for player_id in round_players if player_id != current_player_id):  
        #if all other players are all in
        return round_players



      #iterate players
      if len(round_players) == 1: #one player left
        print("WIN BY FOLD")
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
              bet_matched = True
              break
      pygame.display.flip()
        
    
  # - new game setup - #
  
  print("Starting with default settings. 3 opponents, £50 bot buy in, medium bot difficulty.")
  #remember to add to Player() call below

  
  total_players_left, difficulty, bot_starting_chips = gui.GetSettings()
  big_blind_cycle = 0         #used to know when to double blinds every two cycles of players
  big_blind = 100
  gui.UpdateBlinds(100)       #small blind is always half of big
  temp_bust_players = []

  #initiate player and bot objects
  player_dict = dict()
  player_dict["player_1"] = pokersim.Player(5000)
  for player_id_value in range(2, total_players_left + 1):
    player_dict["player_" + str(player_id_value)] = pokersim.Bot(bot_starting_chips, difficulty) #add bots
  current_round_player_index = random.randrange(0,len(player_dict)) #start on random player every new game
  current_game_player_index = current_round_player_index  #for full rotation of players to increase blinds

  #current_round_player_index = 0 ###human starts for testing REMOVE LATER
  #list(player_dict.keys()) #show who is left
  
  
  # - game - #
  
  play_game = True # new round
  while play_game: # iterate rounds
    # - new round setup - #
    pot = 0
    gui.UpdatePot(pot)
    small_blind = big_blind // 2
  
    round = pokersim.new_round(total_players_left, player_dict)

    #deal cards for remaining players
    #hide old cards
    round_players = []
    for player_id in player_dict:
      round_players.append(player_id)
      player_dict[player_id].SetNewHand(round.GetHand(player_id)) ##int(player_id.split("_")[-1]) 
      player_dict[player_id].ResetAllIn()
      print(f"{player_id} cards: {round.GetHand(player_id)}") ###testing function
      gui.UpdatePlayerChips(player_id, player_dict[player_id].GetChipsLeft())
      gui.UpdatePlayerInfo(player_id, "")
  
    gui.DrawCardBacks(round_players)
    if "player_1" in player_dict:
      gui.ShowHand("player_1", round.GetHand("player_1"))
    gui.ClearRightSidebar()
    gui.ClearHumanCombination()
    
    for player in temp_bust_players:
      if player != "player_1":
        gui.RemoveBustPlayer(player)
        

    #iterate stages and return list of finalists
    for stage in range(4):
      finalists = Play_Round_Stage(stage)  #returns nothing to continue
      if type(finalists) == list:
        break
    
    #calculate winners from finalists
    if finalists is None:
      finalists = round_players
    
    if len(finalists) == 1:
      winners = finalists
      
    
    gui.ShowHand("public", round.GetHand("public"), 0)
    playerCombinations = []
    for finalist in finalists:    #draw winners from database
      print(f"{finalist}:{round.GetHand(finalist)}")
      gui.ShowHand(finalist, round.GetHand(finalist))
      
      player_combination_list = [finalist] + [ int(x) for x in round.FindCombination(round.GetHand(finalist) + round.GetHand("public")) ]
      playerCombinations.append(player_combination_list) # get combination highs and append to list
      gui.ShowFinalCombination(finalist, Convert_Combination_To_Name(player_combination_list[1]))

      pygame.display.flip()
      pygame.time.wait(500)
    
    winners = round.FindWinner(playerCombinations)  #compare values in the list and decide winner or draw
    pygame.display.flip()
    #output combinations with their values
    for winner in winners:
      for player in playerCombinations:
        if player[0] == winner:
          combination = player[1]
          combination_high = str(Convert_Value_To_Name(player[2]))

          if combination == 3:
            combination_high += ", " + str(Convert_Value_To_Name(player[3])) 
          elif combination == 7:
            combination_high += ", " + str(Convert_Value_To_Name(player[3]))

          combination_name = Convert_Combination_To_Name(combination)
          #convert to combination names
          
    print(f"winner: {winners} with a {combination_high} {combination_name}")
    gui.AnnounceWinners(winners, combination_name, combination_high)
    

    #split pot  
    winnings = pot // len(winners)
    for winner in winners:
      print(player_dict[winner].CollectWinnings(winnings))

    #remove bust players
    temp_bust_players = []
    for player in list(player_dict):
      if player_dict[player].GetChipsLeft() == 0:
        temp_bust_players.append(player)
        if player == "player_1":
          gui.DisplayHumanStats(player_dict[player])
        total_players_left -= 1
        round_players.remove(player)
        player_dict.pop(player)
        
      
    
    current_round_player_index += 1 #iterate blinds
    if current_round_player_index > len(player_dict) - 1: 
      current_round_player_index = 0
    if current_round_player_index == current_game_player_index and big_blind < 1600 and big_blind_cycle != 0: 
      #double blinds up to a maximum of 1600 every two cycles
      big_blind *= 2
      big_blind_cycle += 1
      print("Blinds doubled")
    
    pygame.display.flip()

    ####end of round
    #end game if one player left or human out (optional)
    if len(player_dict) < 2: 
      play_game = False
      print(f"{round_players[0]} remains.")
      gui.AnnounceRemainingPlayer(finalists[0])
      gui.MainMenu()

    #save = input("Save? y/N:")
    pygame.display.flip()
    continue_round = gui.AskContinueRound()
    while continue_round == False:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          gui.Quit()

      gui.AskMainMenu()
      continue_round = gui.AskContinueRound()
      pygame.display.flip()
    
    
    if continue_round == "n":
      play_game = False
      ###database write out

    pygame.display.flip()
    


if __name__ == "__main__": 
  pygame.init()
  clock = pygame.time.Clock()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        gui.Quit()
    
    menu = gui.GetMenu()

    if menu == "game_lock":
      NewGame()
    else:  
      if menu == "main menu":
        gui.ShowMainMenu()
      elif menu == "settings":
        gui.ShowSettings()
      elif menu == "help":
        gui.ShowHelp()
      elif menu == "game":
        gui.ChangeMenu("game_lock")
        gui.ClearScreen() 
        
  
    clock.tick(30)  #frame limit
  

  