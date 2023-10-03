import random

# ranked
# testsave


class new_round():
  def __init__(self, players):
    self._players = players
    self._suit = ("hearts","diamonds","spades","clubs")
    self._deck = dict()
    for suit in self._suit:
      self._deck[suit] = [value for value in range(14)]
      
  def Pick_card(self):
    randsuit = random.randint(1,4)
    randvalue = random.randint(1,len(#))
    print(randsuit, randvalue)
    

new_round(5).Pick_card()
