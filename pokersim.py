import random

# cards ranked from Ace 2 3 ... 10 Jack Queen King
# use special behaviour of number 1 to define the high value of it / use ace as the highest value in the list
# randint is inclusive of both limits
# range is inclusive of first value only eg. 1,14 is 1-13

class new_round():
  def __init__(self, players):
    self._players = players
    self.suit = ("hearts","diamonds","spades","clubs")
    self.deck = dict()
    for suit in self.suit:
      self.deck[suit] = [value for value in range(1,14)]
      # 1 - 13
    self._pickHistory = []
    
  def Pick_card(self):
    randsuit = self.suit[random.randint(0,3)]
    randvalue = random.choice(self.deck[randsuit])
    #find random value out of remaining cards
    self._pickHistory.append(randsuit + str(randvalue))
    # when returning, use string :-1 to get card value
    #t
    print(randsuit, randvalue)
    print(self.deck)
    print(self.deck[randsuit].index(randvalue))
    #/t
    return self.deck[randsuit].pop(self.deck[randsuit].index(randvalue)) ### sort this out, used to be -1
    #self.deck.index(randvalue) to fetch actual index of the randvalue
    
  def Deck(self):
    return self.deck

  def PickHistory(self):
    #test function
    return self._pickHistory


  #move methods into subclass
  def DrawPublic(self):
    for i in range(5):
      global Public
      Public = []
      Public.append(self.Pick_card())
    return Public




round1 = new_round(5)


print(round1.DrawPublic())
print(round1.Deck())
print(round1.PickHistory())

# fix card popping with ascending values of the same suit messing with returned value
# have a list of values containing actual length of list
# find a way to ensure you know where the value of the suit is in case of a card being picked
# eg if two cards are picked how would you know which index 5 is
