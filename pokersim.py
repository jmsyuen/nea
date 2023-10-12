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
# find a way to ensure you know where the value of the suit is in case of a card being picked
# eg if two cards are picked how would you know which index 5 is
