import random

# ranked


class new_round():
  def __init__(self, players):
    self._players = players
    self._suit = ("hearts","diamonds","spades","clubs")
    self._value = [2,3,4,5,6,7,8,9,10,"j","q","k",1]
    self._cards = dict(for suit in self._suit)
    for i in self._suit:
      
  def Pick_card(self):
    randsuit = random.randint(1,4)
    randvalue = random.randint(1,len(self._value))
    print(randsuit, randvalue)
    

new_round(5).Pick_card()
