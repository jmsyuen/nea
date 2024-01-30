import gui

import random
from itertools import combinations as MATHSFindCombination

# one tag is useful comments
## two tags for code clips
### three tags for issues
#### important notes or testing clips
# cards ranked from Ace 2 3 ... 10 Jack Queen King
# use special behaviour of number 1 to define the high value of it / use ace as the highest value in the list
# randint is inclusive of both limits
# range is inclusive of first value only eg. 1,14 is 1-13
# to unpack a list use asterisk before variable print(*list)
# changed to 2-14 for ace high
# * to unpack lists
# All methods start with uppercase


class new_round(): 
  def __init__(self, players, player_dict): 
    self.suits = ("hearts", "diamonds", "spades", "clubs")
    self.players = players
    self.player_dict = player_dict
    self.__deck = dict()
    self.__hands = dict()
    for suit in self.suits:
      self.__deck[suit] = [value for value in range(2,15)]  # 2 - 14, 11 is Jack, 13 is King and 14 is Ace
    self.__hands["public"] = self.Pick_Card(5)
    for player_id in player_dict: #adjusted
      self.__hands[player_id] = self.Pick_Card(2)


  def Pick_Card(self, *quantity): #returns the suit.value of card as a string - if given a number, returns a list of cards
    if len(quantity) == 0:
      repeats = 1
    else:
      repeats = quantity[0]
    
    cards = []
    for i in range(repeats):
      randsuit = self.suits[random.randint(0,3)]
      randvalue = random.choice(self.__deck[randsuit])   #finds random value out of remaining cards
      card = randsuit + "." + str(randvalue)
      self.__deck[randsuit].pop(self.__deck[randsuit].index(randvalue)) #removes card from deck
      if repeats == 1:
        return card
      cards.append(card)
    return cards
    

  def GetDeck(self): #returns dictionary
    return self.__deck ### testing function

  #action methods to be moved into subclass later
  def GetHand(self, player_id): #returns hand of player in list form (public is the first, player keys start at 1)
    return self.__hands[player_id]


  def GetPublicStage(self, stage): # returns public cards, takes stage 1-3 but stage 1 returns list
    public = self.__hands["public"]  

    if stage == 1:
      return public[:3] 
    elif stage == 2:
      return public[3]
    elif stage == 3:
      return public[4]
    elif stage == 4:
      return public
    else:                   #error checking, remove later ###
      print("stage invalid")
      raise Exception
  

  def FindCombination(self, cards): # return list [rank, ch, ch, h] for value comparison
    combined_cards = cards
    suits, values = [], []
    allsuits = ("hearts", "diamonds", "spades", "clubs") # repeated as inherited in bot()

    for card in combined_cards:
      split = card.split(".")
      suits.append(split[0])
      values.append(split[-1]) 
    values = sorted(values, key=int)

    def flush():
      for suit in allsuits:
        if suits.count(suit) >= 5: # suit type doesn't matter
          flush_values = []
          for card in combined_cards:
            if suit[0] == card[0]: # match first letter
              flush_values.append(card.split(".")[-1]) # append value of card
          return [sorted(flush_values, key=int)[-1]]
      return False


    def same_num(count): 
      combination_highs = []
      for value in values:
        if values.count(value) == count: # IS PRECISE
          combination_highs.append(value)
          
      if len(combination_highs) != 0:
        return sorted(set(combination_highs), key=int, reverse=True)  #set removes duplicate values and sorts ascending
      else:
        return False


    def straight():
      count = 0
      unique_values = sorted(set(values), key=int)
      loopedlist = unique_values + unique_values
      CH = []   #combination high (ranking of the combination name - see chart)

      for i in range(len(unique_values) * 2 - 4):
        current = int(loopedlist[i])
        next = int(loopedlist[i + 1])
        
        if current + 1 == next or (current + 1 == 15 and next == 2): # ace is 14, so + 1 would be 15 to account for loopback A->2 14->2
          count += 1
        else:
          count = 0
        if count >= 4:
          CH.append(next)

      if len(CH) != 0: # return the highest straight if multiple
        return [max(CH)]
      return False 


    def full_house():
      try:
        # already sorted low-high
        same_num3 = same_num(3)
        same_num2 = same_num(2)

        if len(same_num3) == 2:  # Two 3 of a kinds is automatically a full house
          return same_num3.reverse()
        
        if len(same_num3) == 1 and len(same_num2) > 0:
          return same_num3 + [same_num2[-1]]
        return False
      except:
        return False
    

    def high_card(quantity, CH): # takes how many high cards, existing CH in list form
      remaining = []
      for card in combined_cards:
        card_value = card.split(".")[-1]
        if card_value not in CH:
          remaining.append(card_value)
      result = sorted(set(remaining), key=int)[::-1] # sorted from high-low for later comparison
      return result[:quantity]

    
    def GetOutput(): # in a function to collapse easily
      CH = straight()
      isflush = flush()  
      #ensure every returned value is a list
      #CH straight flush
      if CH != False and isflush != False and CH == isflush:  #ensure flush and straight are same set of cards
        if CH[0] == 1: 
          return [10, 14] # royal flush
        else:
          return [9] + CH   # return combination high

      # CH H 4 of a kind
      CH = same_num(4)
      if CH != False:
        H = high_card(1, CH)
        return [8] + CH + H

      # CH CH full house
      CH = full_house() 
      if CH != False:
        return [7] + CH

      # CH flush
      CH = flush()
      if CH != False:
        return [6] + CH
      
      # CH straight
      CH = straight()
      if CH != False:
        return [5] + CH

      # CH H 3 of a kind
      CH = same_num(3)
      if CH != False:
        return [4] + CH
      
      CH = same_num(2)
      # H high card
      if CH == False: 
        H = high_card(5, [])
        return [1] + H

      # CH CH H 2 pair
      if len(CH) >= 2:
        H = high_card(1, CH)
        return [3] + CH + H 

      # CH H pair
      if len(CH) == 1:
        H = high_card(3, CH)
        return [2] + CH + H
      
      else:
        return False
    
    return GetOutput()


  def FindWinner(self, playerCombinations): # iterate through lists, comparing largest value
    remainingPlayers = list(playerCombinations)
    for i in range(1,len(max(playerCombinations))): #length of longest list
      values = []
      for player in remainingPlayers:
        values.append(player[i])

      locations = [index for index, value in enumerate(values) if value == max(values)] #finds highest value in all lists and returns all occurences
      if len(locations) == 1 or i == len(remainingPlayers[0]) - 1: # second term of the winning list
        break

      temp = []
      for num in locations:
        temp.append(remainingPlayers[num])
      remainingPlayers = temp
    
    winners = []
    for num in locations:
      winners.append(remainingPlayers[num][0])
    return winners


class Player(): 
  def __init__(self, chips_left): 
    self.chips_left = chips_left
    self.bot = False
    self.AllIn = False
    # extra stats - resets on object instantiation
    self.lifetime_chips_wagered = 0
    self.lifetime_winnings = 0
    self.allin_count = 0
    self.rounds_played = 0


  def SetNewHand(self, new_hand):
    self.__hand = new_hand
    self.rounds_played += 1


  def GetHand(self):
    return self.__hand

  
  def Charge(self, amount): #returns amount taken
    if amount > self.chips_left:
      return False
    elif amount == self.chips_left:
      self.AllIn = True
    self.total_stage_bet += amount
    self.lifetime_chips_wagered += amount
    self.chips_left -= amount
    return amount
    

  def CollectWinnings(self, amount):
    self.chips_left += amount
    self.lifetime_winnings += amount
    return amount


  def ResetAllIn(self):
    if self.AllIn == True:
      self.allin_count += 1
    self.AllIn = False
    

  def ResetStageBet(self):
    self.total_stage_bet = 0


  def GetPreviousCharge(self):
    if self.total_stage_bet > 0:
      return self.total_stage_bet
    return 0


  def GetChipsLeft(self):
    return self.chips_left

  
  def GetChoice(self, highest_bet, revealed_cards): #highest_bet to match
    #returns True to continue, False if folded, "AllIn" if has less than bet, total bet value if raise
    if self.AllIn: #persistent
      return "AllIn"
    
    if highest_bet == 0:
      if self.bot == True:
        choice = self.GetBotChoice(highest_bet, "fold check bet", revealed_cards) 
      else:
        #choice = input("Fold(n), Check(y), 3.Bet(amount in 50p intervals):") 
        choice = gui.ShowCheckButtons(highest_bet, self.chips_left)

      if str(choice).isnumeric():
        choice = int(choice)
        if choice == self.chips_left:
          result = self.Charge(self.chips_left)
          self.AllIn = True
          return "AllIn", result
        
        result = self.Charge(choice) 
        ###TESTING
        if result == False: ### testing remove 4 lines later
          print("not enough chips(test)")
          return True
        ###TESTING
        return result
      
      if choice == "y": #check
        return True
      if choice == "n": #fold
        return False

    else: #bet has been made
      if highest_bet >= self.chips_left:
        if self.bot == True:
          choice = self.GetBotChoice(highest_bet, "fold allin", revealed_cards) 
        else:
          #choice = input("All in (y) or fold(n)?:")
          choice = gui.ShowAllInButtons(highest_bet, self.chips_left)

        if choice == "n":
          return False
        else:
          result = self.Charge(self.chips_left)
          self.AllIn = True
          return "AllIn", result
      
      elif highest_bet > 0:
        if self.bot == True:
          choice = self.GetBotChoice(highest_bet, "fold call raise", revealed_cards) 
        else:
          #choice = input("Fold(n), Call(y) or raise extra:")
          choice = gui.ShowCallButtons(highest_bet, self.chips_left)

        previouscharge = self.GetPreviousCharge()
        if previouscharge != False:
          highest_bet -= previouscharge #deduct already input chips
        
        if choice == "y":
          self.Charge(highest_bet)
          return highest_bet
        elif choice == "n":
          return False
        else:
          extra_raise = int(choice) 
          if extra_raise  == self.chips_left:  #check if returned amount matches bet to determine a reraise
            self.AllIn = True
            result = self.Charge(extra_raise)  #new extra bet
            return "AllIn", result
          else: 
            result = self.Charge(highest_bet + extra_raise)  
            return result   #new highest_bet

  


class Bot(new_round, Player): #inherits functions of new_round 
  def __init__(self, chips_left, max_difficulty):
    Player.__init__(self, chips_left)
    self.bot = True
    self.difficulties = ["easy", "medium", "hard"] #how smart the bot is
    self.difficulty = self.difficulties[random.randint(0, self.difficulties.index(max_difficulty))]  #chooses randomly from max_difficulty and below
    self.suits = ("hearts", "diamonds", "spades", "clubs")
    self.odds= {1:0.501177, #6 dp probabilities of every combination, pulled from ggpoker.co.uk
                2:0.422569,
                3:0.047539,
                4:0.021128,
                5:0.003925,
                6:0.001965,
                7:0.001441,
                8:0.000240,
                9:0.000014,
                10:0.000002}
    
    #risk does not affect easy as it chooses a random choice regardless
    if self.difficulty == "medium": 
      self.risk_threshold = 0.01  #0-1 the probability threshold for a card to appear which would be accepted 
    elif self.difficulty == "hard":
      self.risk_threshold = 0.005

    #scrapped system of 10 strategies
    #a new strategy chosen each new round
    #strategy may take into account card hand, public cards, chips left, a bet to match, self risk, self difficulty, and any strategic plans. 
    #each difficulty has its own set of strategies
    

  def SetNewHand(self, new_hand):
    self.__hand = new_hand


  def GetBotChoice(self, highest_bet, available_choices, public_cards):  # strategy for each of the 4 stages
    #choose from strategies based on difficulty and risk
    self.highest_bet = highest_bet
    self.available_choices = available_choices.split(" ")
    self.public_cards = public_cards
    self.known_cards = self.public_cards + self.__hand
    print(self.public_cards)  ###TESTING REMOVE
    self.current_combination_list = [int(x) for x in new_round.FindCombination(self, self.known_cards)]
    #get stage
    if len(public_cards) == 0:
      self.stage = 0
    elif len(public_cards) == 3:
      self.stage = 1
    elif len(public_cards) == 4:
      self.stage = 2
    elif len(public_cards) == 5:
      self.stage = 3
    
    print(f"bot {self.difficulty} difficulty")  # terminal debugging

    if self.difficulty == "easy":
      choice = self.GetEasyStrategyChoice()
    elif self.difficulty == "medium":
      choice = self.GetMediumStrategyChoice()
    elif self.difficulty == "hard":
      choice = self.GetHardStrategyChoice()
    
    return choice

  #conversion functions
  def Convert_Value_To_Letter(self, value):  #convert to compare against pre-defined list in SetStartingHandRankings()
    if value < 10:
      return str(value)
    elif value == 10:
      return "T"
    elif value == 11:
      return "J"
    elif value == 12:
      return "Q"
    elif value == 13:
      return "K"
    elif value == 14:
      return "A"

  def Convert_Hand(self, value1, value2, isonsuit):  #takes AKo as a string and returns 14, 13, offsuit
    string = self.Convert_Value_To_Letter(value1) + self.Convert_Value_To_Letter(value2)
    if isonsuit == False:
      string += "o"
    return string
    


  #strategy logic functions
  def Roll_Risk(self):   #maximium allowed difference in probabilities
    risk = random.randrange(0, self.risk_threshold * 10000) / 10000   #rounded to 4dp
    return risk

  #stage 0 two starting cards
  def DecodeStartingHand(self): #outputs rankings of 1-53 with 1 highest #also take difficulty  
    #split suit and values, sort value1 > value2
    self.suit1, self.value1 = self.__hand[0].split(".")
    self.suit2, self.value2 = self.__hand[1].split(".")
    if int(self.value1) > int(self.value2): #
      self.suit1, self.value1 = self.__hand[1].split(".")
      self.suit2, self.value2 = self.__hand[0].split(".")    
    self.value1, self.value2 = int(self.value1), int(self.value2) #force int

    #assign variables to match certain combinations
    self.onsuit = False
    pair = False
    consecutive_potential = False #how many cards needed to be consecutive, or rank from 5 highest
    face_values = [face_value for face_value in range(10,15)]   #includes 10 as also very good
    face_value_total = 0

    if self.suit1 == self.suit2:
      self.onsuit = True
    elif self.value1 == self.value2:
      pair = True
          
    if self.value1 - self.value2 <= 4:
      consecutive_potential = self.value1 - self.value2
    if self.value1 in face_values:
      face_value_total += 1
    if self.value2 in face_values:
      face_value_total += 1
    
    self.hand_attributes = (self.onsuit, face_value_total, pair, consecutive_potential) #last two cannot both have values
    return self.hand_attributes

  
  def SetStartingHandRankings(self): #complete 169 possible combinations - by default hands are suited unless specified with "o"
    self.DecodeStartingHand()
    self.top10 = ["AA", "KK", "QQ", "AK", "AQ", "JJ", "KQ", "AJ", "AKo", "TT", "99", "88", "77", "AQo", "AT", "AJo", "KJ", "KQo", "KT", "QJ", "QT"]
    #best 10% of hands (21 types)
    converted_hand = self.Convert_Hand(self.value1, self.value2, self.onsuit)
    self.istop10 = False
    if converted_hand in self.top10:
      self.istop10 = True
      self.top10index = self.top10.index(converted_hand)

    self.good_traits = 0   #count how many are true and bet accordingly
    if self.hand_attributes[0] == True:
      self.good_traits += 1
    if self.hand_attributes[1] >= 1:
      self.good_traits += 1
    if self.hand_attributes[2] == True or self.hand_attributes[3] > 0:
      self.good_traits += 1
      

  #stage 1 three cards shown and stage 2 fourth card is shown
  def Calculate_Combinations_Probability(self, num_cards, forOpponent): # predict combination for next card shown - add probabilities for every card unknown - ONLY AFTER FLOP
    if num_cards < 1 or num_cards > 3:
      raise ValueError("Computation will run too long. (Max 3)")
    
    remaining_cards = [] # list containing all remaining cards
    for suit in self.suits:
      for value in range(2,15):
        remaining_cards.append(f"{suit}.{value}")  
    for card in self.known_cards:
      remaining_cards.remove(card)
      
    #test each possible upcoming set of cards
    #combination ONLY done after the flop #max 2 cards as would take too long 51C2 = 1275, 51C3 = 20825
    all_test_tuples = list( MATHSFindCombination(remaining_cards, num_cards))  #contains lists of combinations 
    all_test_combinations = []
      
    if forOpponent == True:
      self.known_cards.remove(self.__hand[0])
      self.known_cards.remove(self.__hand[1])

    for j in range(len(all_test_tuples)): #every possible combination of remaining hands
      all_test_combinations.append( [j] + [int(x) for x in new_round.FindCombination(self, self.known_cards + list(all_test_tuples[j]))] )
    
    combination_ranks = []  
    for list1 in all_test_combinations:  #take the second value out of each list (combination rank eg. value of high card, flush, etc - #highest out of 1-10)
      combination_ranks.append(list1[1])
    
    #calculated values to compare
    rank_appearances = dict()   # count of how many times each combination could occur
    for num in range(1,11):
      rank_appearances[num] = round(combination_ranks.count(num) / len(combination_ranks), 4)
    
    most_likely_combination = max(rank_appearances, key=rank_appearances.get)
    temp_rank_appearances = dict(rank_appearances)
    for key in rank_appearances:
      if rank_appearances[key] == 0.0:
        del temp_rank_appearances[key]
    best_possible_combination = max(temp_rank_appearances)
        
    current_combination = self.current_combination_list[0]
    return [current_combination, rank_appearances[current_combination]], [most_likely_combination, rank_appearances[most_likely_combination]], [best_possible_combination, rank_appearances[best_possible_combination]]
    #return current combination, most likely and best each with corresponding probabilities
    #if probability is higher than global statistics then bet #implement with risk
    

  #stage 3 all cards revealed
  def Compare_To_Opponent_Probabilities(self, current_combination, most_likely_combination, best_possible_combination):  #calculate probabilities of combinations using only public cards to predict what others have
    opponent_current, opponent_most_likely, opponent_best = self.Calculate_Combinations_Probability(2, True)
    if opponent_current[0] > current_combination[0]:
      best_action = 0
    elif opponent_most_likely[0] > most_likely_combination[0]:
      best_action = 1
    elif opponent_best[0] > best_possible_combination[0] and opponent_best[1] > best_possible_combination[1]:
      best_action = 2
    elif abs(opponent_current[0] - current_combination[0]) < 2:
      best_action = 3
    else:
      best_action = 4
    return best_action
    #find probability of higher one being found in last stage
    

  def Get_Random_Bet_Amount(self, best_action): #determined by strategy and size of chips
    #(still randrange and high includes allin) ranges overlap to make it harder to pick up patterns
    

    if best_action == 2: #bet low
      if self.chips_left < 50:  #go all in if not enough chips for min bet
        return self.chips_left
      return random.randrange(50, self.chips_left // 3, 50) #0 - lower third
    elif best_action == 3: #bet medium
      if self.chips_left < self.chips_left // 5:
        return self.chips_left
      return random.randrange(self.chips_left // 5, self.chips_left // (4/3), 50) #fifth to 3/4
    elif best_action == 4: #bet high
      if self.chips_left < self.chips_left // (5/3):
        return self.chips_left
      return random.randrange(self.chips_left // (5/3), self.chips_left, 50) #3/5 to allin


  #strategies for each difficulty
  def GetEasyStrategyChoice(self): #equal uniform distribution of choices in each choice
    #pickrandom choice, pickrandom bet 
    choice = random.choice(self.available_choices)
    
    if choice == "fold":
      return "n"
    elif choice == "allin" or choice == "call" or choice == "check":
      return "y"

    #elif choice == "raise" or choice == "bet":
    else:
      raise_value = random.randrange(50, self.chips_left, 50) 
      return raise_value


  def GetMediumStrategyChoice(self):
    rolled_risk = self.Roll_Risk() #how risky bot is willing to be
    best_action = False
    #action is ranked from 0-4 for comparison    fold, check, bet low, bet medium, bet high

    #determine a course of action
    if self.stage == 0:
      self.SetStartingHandRankings()
      if self.top10:   #"bet high"
        best_action = 4
      elif self.good_traits == 3: #"bet medium"
        best_action = 3
      elif self.good_traits == 2: #"bet low"
        best_action = 2
      elif self.good_traits == 1: #"check"
        best_action = 1
      elif self.good_traits == 0: #"fold"
        best_action = 0
    
    elif self.stage == 1 or self.stage == 2:
      current_combination, most_likely_combination, best_possible_combination =  self.Calculate_Combinations_Probability(3 - self.stage, False)
      
      if abs(current_combination[1] - best_possible_combination[1]) < rolled_risk:  #within risk tolerance
        best_action = 4
      elif abs(most_likely_combination[1] - current_combination[1]) < rolled_risk or current_combination[0] == best_possible_combination[0]:
        best_action = 3
      elif most_likely_combination[1] > self.odds[current_combination[0]] or most_likely_combination[1] > self.odds[most_likely_combination[0]]:  #greater than global stats
        best_action = 2
      elif current_combination[1] > self.odds[current_combination[0]]:
        best_action = 1
      else:
        best_action = 0

    #similar to prev stages but takes into account possible opponent cards
    elif self.stage == 3:
      current_combination, most_likely_combination, best_possible_combination =  self.Calculate_Combinations_Probability(1, False)
      best_action = self.Compare_To_Opponent_Probabilities(current_combination, most_likely_combination, best_possible_combination)


    #check if conditions are met for choices else fold
    if self.available_choices == ["fold", "check", "bet"]:
      print("fold check bet")
      if best_action >= 2:  # bet
        return self.Get_Random_Bet_Amount(best_action)
      if best_action == 1:  # check
        return "y"
      else:  # fold
        return "n"
      
      
    elif self.available_choices == ["fold", "allin"]:
      print("fold allin")
      if best_action >= 4:  # all in  at least a bet high
        return "y"
      else:  # fold
        return "n"
      
      
    elif self.available_choices == ["fold", "call", "raise"]:
      print("fold call raise")
      if best_action >= 3:  # raise   at least a bet medium
        return self.Get_Random_Bet_Amount(best_action)
      if best_action >= 2:  # call  at least a bet low
        return "y"
      else:  # fold
        return "n"   
      

  def GetHardStrategyChoice(self):  #hard takes into account card values instead of just combinations
    #ranks every hand from lowest to highest and has cutoff point to fold at start
    rolled_risk = self.Roll_Risk() #approx half of medium strategy
    best_action = False
    #determine a course of action
    if self.stage == 0:
      self.SetStartingHandRankings()
      if self.istop10 and self.top10index < 3:
        best_action = 4
      elif self.istop10 and self.hand_attributes[1] == 2 and self.good_traits >= 2:  #face value and one other good trait
        best_action = 2
      elif self.good_traits >= 2:
        best_action = 1
      else:
        best_action = 0
    
    elif self.stage == 1 or self.stage == 2:
      current_combination, most_likely_combination, best_possible_combination =  self.Calculate_Combinations_Probability(3 - self.stage, False)
      
      if abs(current_combination[1] - best_possible_combination[1]) < rolled_risk:  #within risk tolerance
        best_action = 4
      elif abs(most_likely_combination[1] - current_combination[1]) < rolled_risk or current_combination[0] == best_possible_combination[0]:
        best_action = 3
      elif most_likely_combination[1] > self.odds[current_combination[0]] or most_likely_combination[1] > self.odds[most_likely_combination[0]]:  #greater than global stats
        best_action = 2
      elif current_combination[1] > self.odds[current_combination[0]]:
        best_action = 1
      else:
        best_action = 0

    #similar to prev stages but takes into account possible opponent cards
    elif self.stage == 3:
      best_action = self.Compare_To_Opponent_Probabilities(current_combination, most_likely_combination, best_possible_combination)

    ##import choices from med strategy
    #return a choice      
    if self.available_choices == ["fold", "check", "bet"]:
      print("fold check bet")
      if best_action >= 2:  # bet
        return self.Get_Random_Bet_Amount(best_action)
      if best_action == 1:  # check
        return "y"
      else:  # fold
        return "n"
      
      
    elif self.available_choices == ["fold", "allin"]:
      print("fold allin")
      if best_action >= 4:  # all in  at least a bet high
        return "y"
      else:  # fold
        return "n"
      
      
    elif self.available_choices == ["fold", "call", "raise"]:
      print("fold call raise")
      if best_action >= 4:  # raise   at least a bet high
        return self.Get_Random_Bet_Amount(best_action)
      if best_action >= 3:  # call  at least a bet medium
        return "y"
      else:  # fold
        return "n"   
    
    

if __name__ == "__main__":  #for testing
  
  temp_round = new_round(3, {"player_1: "})
  temp_round



  hand = ["hearts.14", "spades.14"]
  bot1 = Bot(5000, "medium")
  
  bot1.SetNewHand(hand)
  bot1.ResetAllIn()
  bot1.ResetStageBet()
  for i in range(10):
    print(bot1.GetBotChoice(0, "fold check bet", ["spades.4", "spades.3", "spades.2"]))

  print()
  print(bot1.difficulty)
  print(bot1.DecodeStartingHand())
  print(bot1.Calculate_Combinations_Probability(2, False))
  print(bot1.SetStartingHandRankings())
  print(bot1.Roll_Risk())


