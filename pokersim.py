import random

# one tag is useful comments
## two tags for code clips
### three tags for issues
# cards ranked from Ace 2 3 ... 10 Jack Queen King
# use special behaviour of number 1 to define the high value of it / use ace as the highest value in the list
# randint is inclusive of both limits
# range is inclusive of first value only eg. 1,14 is 1-13
# to unpack a list use asterisk before variable print(*list)


class new_round():
  def __init__(self, players):
    self.suit = ("hearts","diamonds","spades","clubs")
    self._deck = dict()
    self._hands = dict()
    for suit in self.suit:
      self._deck[suit] = [value for value in range(1,14)]
      # 1 - 13
    self._pickHistory = []
    self.players = players
    self.totalcards = 5 + (players * 2)
    
  def Pick_card(self, *quantity): #returns the suit;value of card as a string - if given a number, returns a list of cards
    if len(quantity) == 0:
      repeats = 1
    else:
      repeats = quantity[0]
    
    cards = []
    for i in range(repeats):
      randsuit = self.suit[random.randint(0,3)]
      randvalue = random.choice(self._deck[randsuit])
      #finds random value out of remaining cards
      card = randsuit + ";" + str(randvalue)
      self._pickHistory.append(card) 
      self._deck[randsuit].pop(self._deck[randsuit].index(randvalue)) ##used to be -1
      #removes card from deck
      if repeats == 1:
        return card
      cards.append(card)
    return cards
    ##self._deck.index(randvalue) to fetch actual index of the randvalue
    
  def Deck(self): #returns dictionary
    return self._deck

  def PickHistory(self): # returns in list
    #test function to be used later
    #when returning, use split(";") to separate
    lastcard = self._pickHistory[-1]
    return self._pickHistory
    #for nice format, have to split into card and number


  #action methods to be moved into subclass later
  def DrawCards(self):
    self._hands["public"] = self.Pick_card(5)
    for i in range(1, self.players + 1): #adjusted
      #dealt same way as in real life without burning cards
      self._hands[i] = self.Pick_card(2)
      
      #dict with hands, adding new key for every player
      # from 1- no.players and loop again to no.players*2
      # add public cards at end dictionary[-5]
      #deal hands here, then assign hands according to blind rotation
      
    
    print(self._hands)

  def FindHand(self, player): #returns hand with 2 cards
    
    return self._hands[player]



round1 = new_round(5)


print(round1.DrawCards())
print(round1.Deck())
round1.PickHistory()
print(round1.FindHand(2))

# fix card popping with ascending values of the same suit messing with returned value
# have a list of values containing actual length of list
# find a way to ensure you know where the value of the suit is in case of a card being picked
# eg if two cards are picked how would you know which index 5 is
