import pokersim

# nea
def NewGame(players, buyIn, startingblinds):
  valid = False
  while not valid:
    try:
      players = int(input("Enter number of players:")) # replace with pygame and specific buttons
      buyIn = int(input("Enter buy in value for each player"))

      valid = True
    except:
      pass 

print(pokersim.round1.Deck())