import random

# ranked
# testsave
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
  # def New_deck(self):
    
  def Pick_card(self):
    randsuit = self.suit[random.randint(0,3)]
    randvalue = random.randint(1,len(self.deck[randsuit]))
    # remaining cards in suit
    print(randsuit, randvalue)
    return self.deck[randsuit].pop(randvalue - 1)
    
  def Deck(self):
    return self.deck

round1 = new_round(5)
print(round1.Pick_card())
print(round1.Deck())
# find a way to return the popped value at l23
# find a way to have a deck that doesn't reset every time function is called
# find a way to call one instance and refer back to that instance without resetting
