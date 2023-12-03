import pokersim

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