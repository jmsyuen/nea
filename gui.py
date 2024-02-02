import pygame
import sys
import webbrowser
import time
#reduce flicker by reducing frame updates


WIDTH, HEIGHT = 414, 896 #logical point resolution of iphone 11
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#main colours
DARK_BEIGE = (204, 204, 183) #background
IVORY = (245,245,230)        #text box
OLIVE = (137, 137, 97)       #button hover 
LIGHT_GREY = (184, 184, 165) #button normal

#small card size 50x72px, big 100x144px
#includes padding of 20px around right and bottom sides
SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT = 70, 92  
BIG_CARD_WIDTH, BIG_CARD_HEIGHT = 120, 164  

#default values
menu = "main menu"
opponents = 3
bot_starting_chips = 5000 
max_difficulty = "medium" 

temporary_bet = 50   #might need to be 50
choice = False
temp_chips_left = False
temp_highest_bet = False
continue_choice = False

# start pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poker VS Bots")

# load images
small_card_images = []  # https://code.google.com/archive/p/vector-playing-cards/
big_card_images = []
back = [] #small, big
suits = ("hearts", "diamonds", "spades", "clubs")

for suit in suits:
  for value in range(2, 15):
    small_card_images.append(pygame.image.load(f"small_cards/{suit}.{value}.png"))  
    big_card_images.append(pygame.image.load(f"big_cards/{suit}.{value}.png"))

back.append(pygame.image.load(f"small_cards/back.png"))
back.append(pygame.image.load(f"big_cards/back.png"))

#screen locations of cards 
locations = dict() #size of cards followed by x and y of each
locations["public"] = tuple((40 + i * SMALL_CARD_WIDTH, 20) for i in range(5))
locations["player_1"] = [(20, HEIGHT - 162), (20 + BIG_CARD_WIDTH, HEIGHT - 162)]
for player_id_value in range(2,8):  #range of other opponents #player in players
  location1 = (20, 122 + (player_id_value-2) * SMALL_CARD_HEIGHT)
  location2 = (80, 122 + (player_id_value-2) * SMALL_CARD_HEIGHT)
  locations[f"player_{player_id_value}"] = [location1, location2]


#screen locations of info boxes
bot_info_locations = dict()

for i in range(6):
  x =  140
  y =  122 + i * SMALL_CARD_HEIGHT
  bot_info_locations[f"player_{i+2}"] = [x, y]
#two big cards at bottom left
#maybe big public cards at top 
#list of 9 other players with cards on right side
# reveal cards in succession by moving down 5px and flipping and up 5px again


#core ui drawing functions
def DrawButton(text, box_colour, x, y, width, height, action): #draw buttons and execute function when pressed
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  hover_colour = OLIVE
  font = pygame.font.SysFont("courier", 15)
  #check if hover
  if x + width > mouse[0] > x and y + height > mouse[1] > y:
    pygame.draw.rect(screen, hover_colour, (x, y, width, height))
    if click[0] == 1:
      action()
  else:
    pygame.draw.rect(screen, box_colour, (x, y, width, height))

  #white border
  border_width = 1
  pygame.draw.rect(screen, WHITE, (x, y, width, height), border_width)

  #add text
  text_surface = font.render(text, True, WHITE)
  text_rect = text_surface.get_rect()
  #add text to centre
  text_rect.center = ((x + (width // 2)), (y + (height // 2)))
  screen.blit(text_surface, text_rect)


def DrawTextBox(text, text_colour, box_colour, font_size, x, y, width, height):
  font = pygame.font.SysFont("courier", font_size)
  
  pygame.draw.rect(screen, box_colour, (x, y, width, height))
  text_surface = font.render(text, True, text_colour)
  text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
  screen.blit(text_surface, text_rect)


def ClearScreen():
  screen.fill(DARK_BEIGE)  #background
  #pygame.display.flip()


def blank():  #dummy for greyed out button
  pass


def GetMenu():
  return menu


def ChangeMenu(new_menu):
  global menu
  menu = new_menu 


def MainMenu():
  ChangeMenu("main menu")


def StartGame():
  ChangeMenu("game")


def OpenWikipediaLink():
  webbrowser.open("https://en.wikipedia.org/wiki/Texas_hold_%27em")
  time.sleep(1) #prevents several instances opened at same time

#due to the way functions in buttons are run with no parameters, a lot of these will take up space
  
def set_1_opponents():
  global opponents
  opponents = 1
def set_2_opponents():
  global opponents
  opponents = 2
def set_3_opponents():
  global opponents
  opponents = 3
def set_4_opponents():
  global opponents
  opponents = 4
def set_5_opponents():
  global opponents
  opponents = 5
def set_6_opponents():
  global opponents
  opponents = 6

def set_easy_difficulty():
  global max_difficulty
  max_difficulty = "easy"
def set_medium_difficulty():
  global max_difficulty
  max_difficulty = "medium"
def set_hard_difficulty():
  global max_difficulty
  max_difficulty = "hard"

def set_5000_chips():
  global bot_starting_chips
  bot_starting_chips = 5000
def set_10000_chips():
  global bot_starting_chips
  bot_starting_chips = 10000
def set_20000_chips():
  global bot_starting_chips
  bot_starting_chips = 20000

def GetSettings():
  return [opponents + 1, max_difficulty, bot_starting_chips]


def Quit():
  pygame.quit()
  sys.exit()



#display menu functions
def ShowMainMenu():
  ClearScreen()
  DrawTextBox("Poker VS Bots", WHITE, DARK_BEIGE, 30, 0, 40, 414, 100)
  DrawButton("Settings", LIGHT_GREY, -5, 250, 420, 50, ShowSettings)
  DrawButton("Help", LIGHT_GREY, -5, 300, 420, 50, ShowHelp)
  DrawButton("Quit", LIGHT_GREY, -5, 350, 420, 50, Quit)
  DrawButton("New Game", LIGHT_GREY, -5, 200, 420, 50, StartGame)
  pygame.display.flip()
  

def ShowHelp():
  global menu
  menu = "help"
  topbox_ypos = 150 #easily change height of boxes while keeping them grouped
  ClearScreen()
  DrawTextBox("Help", BLACK, IVORY, 15, 0, 0, 414, 40)
  DrawTextBox("Welcome to Poker VS Bots!", BLACK, DARK_BEIGE, 20, 0, 40, 414, 100)
  DrawTextBox("This is a mobile game to play standard", BLACK, DARK_BEIGE, 14, 0, topbox_ypos, 414, 20)
  DrawTextBox("Texas Hold\'em poker against up to 1-6 other bots.", BLACK, DARK_BEIGE, 14, 0, topbox_ypos + 20, 414, 20)
  DrawTextBox("In Settings you can change how the bots behave,", BLACK, DARK_BEIGE, 14, 0, topbox_ypos + 40, 414, 20)
  DrawTextBox("choosing their difficulty and starting chips.", BLACK, DARK_BEIGE, 14, 0, topbox_ypos + 60, 414, 20)
  DrawTextBox("However, you will always start with 5000 chips.", BLACK, DARK_BEIGE, 14, 0, topbox_ypos + 80, 414, 20)
  DrawTextBox("Settings will persist between games once changed.", BLACK, DARK_BEIGE, 14, 0, topbox_ypos + 120, 414, 20)
  DrawTextBox("You can return to the menu after a round finishes,", BLACK, DARK_BEIGE, 14, 0, topbox_ypos + 140, 414, 20)
  DrawTextBox("but doing so will reset the game.", BLACK, DARK_BEIGE, 14, 0, topbox_ypos + 160, 414, 20)
  #DrawTextBox("", BLACK, DARK_BEIGE, 14, 0, 170, 414, 20)
  
  DrawButton("Wikipedia page", LIGHT_GREY, 0, 600, 414, 100, OpenWikipediaLink)
  DrawButton("Back", LIGHT_GREY, 0, HEIGHT - 100, 414, 100, MainMenu)
  pygame.display.flip()

  
def ShowSettings():
  global menu
  menu = "settings"
  ClearScreen()
  DrawTextBox("Settings", BLACK, IVORY, 15, 0, 0, 414, 40)
  DrawTextBox("You can only change settings before a game", BLACK, IVORY, 13, 0, 40, 414, 30)
  DrawButton("Back", LIGHT_GREY, 0, HEIGHT - 100, 414, 100, MainMenu)

  #number of opponents
  DrawTextBox(f"Number of opponents: {opponents}", BLACK, IVORY, 15, 0, HEIGHT - 760, 414, 40)
  DrawButton("1", LIGHT_GREY, 67, HEIGHT - 700, 30, 30, set_1_opponents)
  DrawButton("2", LIGHT_GREY, 117, HEIGHT - 700, 30, 30, set_2_opponents)
  DrawButton("3", LIGHT_GREY, 167, HEIGHT - 700, 30, 30, set_3_opponents)
  DrawButton("4", LIGHT_GREY, 217, HEIGHT - 700, 30, 30, set_4_opponents)
  DrawButton("5", LIGHT_GREY, 267, HEIGHT - 700, 30, 30, set_5_opponents)
  DrawButton("6", LIGHT_GREY, 317, HEIGHT - 700, 30, 30, set_6_opponents)
  #bot difficulty
  DrawTextBox(f"Maximum opponent difficulty: {max_difficulty}", BLACK, IVORY, 15, 0, HEIGHT - 650, 414, 40)
  DrawButton("Easy", LIGHT_GREY, 20, HEIGHT - 590, 100, 30, set_easy_difficulty)
  DrawButton("Medium", LIGHT_GREY, 160, HEIGHT - 590, 100, 30, set_medium_difficulty)
  DrawButton("Hard", LIGHT_GREY, 300, HEIGHT - 590, 100, 30, set_hard_difficulty)
  #buy in value
  DrawTextBox(f"Opponent starting chips: {bot_starting_chips}", BLACK, IVORY, 15, 0, HEIGHT - 540, 414, 40)
  DrawTextBox("(you always start with 5000)", BLACK, IVORY, 15, 0, HEIGHT - 510, 414, 30)
  DrawButton("5k", LIGHT_GREY, 20, HEIGHT - 460, 100, 30, set_5000_chips)
  DrawButton("10k", LIGHT_GREY, 160, HEIGHT - 460, 100, 30, set_10000_chips)
  DrawButton("20k", LIGHT_GREY, 300, HEIGHT - 460, 100, 30, set_20000_chips)


  pygame.display.flip()


#integration functions
def UpdatePot(pot):
  DrawTextBox(f"Pot {pot}", BLACK, IVORY, 15, WIDTH - 160, 122, 140, 30)


def UpdateBlinds(big_blind):
  DrawTextBox(f"Blinds {big_blind // 2}/{big_blind}", BLACK, IVORY, 14, WIDTH - 160, 152, 140, 30)


def UpdatePlayerChips(player_id, chips_left):
  if player_id == "player_1":
    DrawTextBox(f"Chips: {chips_left}", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 255, 140, 30)
  else:
    top_left_x = bot_info_locations[player_id][0]
    top_left_y = bot_info_locations[player_id][1]
    DrawTextBox(f"Chips:{chips_left}", BLACK, IVORY, 13, top_left_x, top_left_y + 48, 100, 24)


def draw_card(size, card, position): #takes card like spades.3, and xy position as tuple
  if card == "back":
    if size == "small":
      screen.blit(back[0], position)
    elif size == "big":
      screen.blit(back[1], position)
    
    pygame.display.flip()
    return

  suit, value = card.split(".")
  #map index 2-14 to 0-12, add offset of 13 for each suit
  list_index = int(value) - 2
  if suit == "diamonds":
    list_index += 13
  elif suit == "spades":
    list_index += 26
  elif suit == "clubs":
    list_index += 39

  if size == "small":
    screen.blit(small_card_images[list_index], position)
  elif size == "big":
    screen.blit(big_card_images[list_index], position)
  
  pygame.display.flip()
  return


def UpdatePlayerInfo(*args):   #player_id_value, prev_action, chips_left
  player_id_value = args[0]
  prev_action = args[1]
  if type(player_id_value) == str:
    player_id_value = player_id_value.split("_")[1]

  if str(player_id_value) == "1":  #catch and ignore showing prev_action for human player
    if len(args) > 2:
      chips_left = args[2]
      UpdatePlayerChips("player_1", chips_left)
      
    
  else:  
    top_left_x = bot_info_locations[f"player_{player_id_value}"][0]
    top_left_y = bot_info_locations[f"player_{player_id_value}"][1]
  
    if len(args) > 2:
      chips_left = args[2]
      DrawTextBox(f"Chips:{chips_left}", BLACK, IVORY, 13, top_left_x, top_left_y + 48, 100, 24)

    DrawTextBox(f"Player {player_id_value}", BLACK, IVORY, 13, top_left_x, top_left_y, 100, 24) #change string with player name  ###
    DrawTextBox(prev_action, BLACK, IVORY, 13, top_left_x, top_left_y + 24, 100, 24)  #two to be replaced with actual variables ###
  

#add revealing animation using time.sleep and solid colour text box of white then 2 shades of grey  
def ShowHand(*args):  #player_id in full string, cards as a list, if public choose stage
  player_id = args[0] 
  cards = args[1]
  if type(cards) == str:
    cards = [cards]
  #does not catch if only one card given - enter single item as a list
  position = 0

  if player_id == "public": #position card accordingly
    stage = args[2]
    
    if stage == 2:
      position = 3
    elif stage == 3:
      position = 4


  if player_id == "player_1":
    size = "big"
  else:
    size = "small"
  
  
  for card in cards:
    draw_card(size, card, locations[player_id][position])
    position += 1
    
  #locations as an xy tuple
    

def UpdateTurnIndicator(player_id):
  DrawTextBox("", BLACK, DARK_BEIGE, 20, 0, 120, 20, HEIGHT)  #clear bar on the side
  DrawTextBox(">", BLACK, DARK_BEIGE, 20, locations[player_id][0][0] - 20, locations[player_id][0][1], 20, 20)



#buttons - these cannot have arguments as they are executed

def GetChoice():  #different for every set of choices
  global choice
  actual_choice = str(choice)
  choice = False  #reset
  return actual_choice

#maybe set greyed out state for these 2 buttons
def increase_50():
  global temporary_bet, temp_chips_left
  temporary_bet += 50
  if temporary_bet > temp_chips_left:
    temporary_bet -= 50
  pygame.display.flip()
  time.sleep(0.1)
    
def decrease_50():
  global temporary_bet, temp_highest_bet
  temporary_bet -= 50
  if temporary_bet < temp_highest_bet:
    temporary_bet += 50
  pygame.display.flip()
  time.sleep(0.2)

  
def reset_temporary_bet():
  global temporary_bet
  temporary_bet = 50
  #min 50 (smallest bet possible)

def fold():
  global choice
  choice = "n"
def allin():
  global choice, temp_chips_left
  choice = str(temp_chips_left) #remanining chips, GetChoice requires values to be a string for isnumeric to work
def check():
  global choice
  choice = "y"

def confirm_bet():
  global choice, temporary_bet
  choice = temporary_bet
  



#get a choice out of the function names
def ShowCheckButtons(highest_bet, chips_left):

  global choice, temp_chips_left, temp_highest_bet
  temp_chips_left, temp_highest_bet = chips_left, highest_bet
  reset_temporary_bet()
  
  while choice == False:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Quit()
        
    DrawTextBox(f"Bet: {temporary_bet}", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
    DrawButton("Check", LIGHT_GREY, 20 + 80, HEIGHT - 205, 60, 30, check)
    
    DrawButton("All In", LIGHT_GREY, 20, HEIGHT - 205, 60, 30, allin)
    DrawButton("Fold", LIGHT_GREY, 20 + 80 + 80, HEIGHT - 205, 60, 30, fold)

    DrawButton("Clear Bet", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, reset_temporary_bet)
    DrawButton("- 50", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, decrease_50)
    DrawButton("+ 50", LIGHT_GREY, WIDTH - 80, HEIGHT - 105, 60, 30, increase_50)
    DrawButton("Confirm Raise", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, confirm_bet)

    pygame.display.flip()
  return GetChoice()


def ShowCallButtons(highest_bet, chips_left):

  global choice, temp_chips_left, temp_highest_bet, temporary_bet
  temp_chips_left, temp_highest_bet = chips_left, highest_bet
  temporary_bet = highest_bet


  while choice == False:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Quit()
    DrawTextBox(f"Bet: {temporary_bet}", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
    DrawButton("Call", LIGHT_GREY, 20 + 80, HEIGHT - 205, 60, 30, check)

    DrawButton("All In", LIGHT_GREY, 20, HEIGHT - 205, 60, 30, allin)
    DrawButton("Fold", LIGHT_GREY, 20 + 80 + 80, HEIGHT - 205, 60, 30, fold)

    DrawButton("Clear Bet", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, reset_temporary_bet)
    DrawButton("- 50", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, decrease_50)
    DrawButton("+ 50", LIGHT_GREY, WIDTH - 80, HEIGHT - 105, 60, 30, increase_50)
    DrawButton("Confirm Raise", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, confirm_bet)

    pygame.display.flip()

  return GetChoice()


def ShowAllInButtons(highest_bet, chips_left):

  global choice, temp_chips_left, temp_highest_bet, temporary_bet
  temp_chips_left, temp_highest_bet = chips_left, highest_bet
  temporary_bet = chips_left

  while choice == False:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Quit()
    #working buttons
    DrawTextBox(f"Bet: {temporary_bet}", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
    DrawButton("All In", LIGHT_GREY, 20, HEIGHT - 205, 60, 30, allin)
    DrawButton("Fold", LIGHT_GREY, 20 + 80 + 80, HEIGHT - 205, 60, 30, fold)
    #draw over in black to eliminate WHITE
    DrawTextBox("", WHITE, BLACK, 15, 20 + 80, HEIGHT - 205, 60, 30)
    DrawTextBox("", WHITE, BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30)
    DrawTextBox("", WHITE, BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30)
    DrawTextBox("", WHITE, BLACK, 15, WIDTH - 80, HEIGHT - 105, 60, 30)
    DrawTextBox("", WHITE, BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30)
    #grey out with buttons that do nothing
    DrawButton("Call", OLIVE, 20 + 80, HEIGHT - 205, 60, 30, blank)
    DrawButton("Clear Bet", OLIVE, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, blank)
    DrawButton("- 50", OLIVE, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, blank)
    DrawButton("+ 50", OLIVE, WIDTH - 80, HEIGHT - 105, 60, 30, blank)
    DrawButton("Confirm Raise", OLIVE, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, blank)

    pygame.display.flip()

  return GetChoice()


def AnnounceWinners(winners, combination, combination_high):
  DrawTextBox("Winning combination", BLACK, IVORY, 11, WIDTH - 160, 214, 140, 24)
  DrawTextBox(f"{combination}", BLACK, IVORY, 15, WIDTH - 160, 238, 140, 24)#
  DrawTextBox(f"{combination_high} high", BLACK, IVORY, 15, WIDTH - 160, 262, 140, 24)# 

  DrawTextBox("Winner(s)", BLACK, IVORY, 15, WIDTH - 160, 306, 140, 24)
  for i in range(len(winners)):  #winner in winners
    winner_value = winners[i][-1]
    DrawTextBox(f"Player {winner_value}", BLACK, IVORY, 15, WIDTH - 160, 330 + i * 24, 140, 24)#+24

def AnnounceRemainingPlayer(player_id):
  DrawTextBox(f"Player {player_id[-1]} remains.", BLACK, IVORY, 13, WIDTH - 160, HEIGHT - 375, 140, 24)
  DrawTextBox("", BLACK, IVORY, 13, WIDTH - 160, HEIGHT - 300, 140, 30)


def ClearRightSidebar():
  DrawTextBox("", BLACK, DARK_BEIGE, 15, WIDTH - 160, 214, 140, 420)




def AskContinueRound():
  global continue_choice
  actual_continue_choice = continue_choice
  continue_choice = False
  return actual_continue_choice
def continue_round():
  global continue_choice
  continue_choice = "y"
def exit_to_menu():
  global continue_choice
  MainMenu()
  continue_choice = "n"

def AskMainMenu(): #continue to next round or save
  DrawButton("Exit to menu", LIGHT_GREY, WIDTH - 160, HEIGHT - 340, 140, 30, exit_to_menu)
  DrawButton("Continue", LIGHT_GREY, WIDTH - 160, HEIGHT - 300, 140, 30, continue_round) 




def menu_button(): #maybe unused
  DrawButton("Menu", LIGHT_GREY, WIDTH - 79, HEIGHT - 305, 60, 30, MainMenu)


def DrawCardBacks(remaining_players_list):   #hide cards from previous round
  if "player_1" in remaining_players_list:  
    #big cards for human player
    draw_card("big", "back", locations["player_1"][0])
    draw_card("big", "back", locations["player_1"][1])
  
  #draw public cards at top
  for i in range(5):
    draw_card("small", "back", locations["public"][i])
  
  #list of players on left for right handed players on mobile
  for player_id in remaining_players_list:  #range of other opponents #player in players ########change this range
    if player_id == "player_1":
      continue
    draw_card("small", "back", locations[player_id][0])
    draw_card("small", "back", locations[player_id][1])

    #UpdatePlayerInfo(player_id_value, "", bot_remaining_chips) ###change to starting chips total_chips_left
    
  pygame.display.flip()


def RemoveBustPlayer(player_id): 
  first_card_x, first_card_y = locations[player_id][0][0], locations[player_id][0][1]
  if player_id == "player_1":
    DrawTextBox("", BLACK, DARK_BEIGE, 11, first_card_x, first_card_y, BIG_CARD_WIDTH*2 - 20, BIG_CARD_HEIGHT)
  else:
    DrawTextBox("", BLACK, DARK_BEIGE, 11, first_card_x, first_card_y, SMALL_CARD_WIDTH*2 + 80, SMALL_CARD_HEIGHT)
    #and remove info boxes


def DisplayHumanStats(player_object):
  top_left_x, top_left_y = locations["player_1"][0][0], locations["player_1"][0][1]
  #position relative to top left card
  player_object.ResetAllIn()

  DrawTextBox(f"Bust", BLACK, DARK_BEIGE, 15, top_left_x, top_left_y, 220, 20)
  DrawTextBox(f"", BLACK, DARK_BEIGE, 13, top_left_x, top_left_y + 20, 220, 20)
  DrawTextBox(f"{player_object.rounds_played} rounds played", BLACK, DARK_BEIGE, 15, top_left_x, top_left_y + 40, 220, 20)
  DrawTextBox(f"{player_object.lifetime_chips_wagered} chips wagered", BLACK, DARK_BEIGE, 15, top_left_x, top_left_y + 60, 220, 20)
  DrawTextBox(f"{player_object.lifetime_winnings} chips won", BLACK, DARK_BEIGE, 13, top_left_x, top_left_y + 80, 220, 20)
  DrawTextBox(f"Went all in {player_object.allin_count} times", BLACK, DARK_BEIGE, 13, top_left_x, top_left_y + 100, 220, 20)

  #remove buttons


def New_Game():  #testing displays
  #dynamic variables to be udpated
  UpdatePot(200000)
  UpdateBlinds(2000)
  UpdatePlayerChips("player_1", 5000)
  #fetch settings when new game is started
  
  #ShowAllInButtons(500, 5000)
  DrawTextBox(f"Bet: 50", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
  DrawButton("Call", LIGHT_GREY, 20 + 80, HEIGHT - 205, 60, 30, check)

  DrawButton("All In", LIGHT_GREY, 20, HEIGHT - 205, 60, 30, allin)
  DrawButton("Fold", LIGHT_GREY, 20 + 80 + 80, HEIGHT - 205, 60, 30, fold)

  DrawButton("Clear Bet", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, reset_temporary_bet)
  DrawButton("- 50", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, decrease_50)
  DrawButton("+ 50", LIGHT_GREY, WIDTH - 80, HEIGHT - 105, 60, 30, increase_50)
  DrawButton("Confirm Raise", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, confirm_bet)
  AskMainMenu()


  AnnounceWinners(["player_1", "player_2", "player_3", "player_4", "player_5", "player_6", "player_7"], "Three of a kind", 6)
  AnnounceRemainingPlayer("player_2")
  ShowHand("player_2", ["spades.3", "diamonds.9"])
  ShowHand("player_1", ["spades.14", "diamonds.14"])
  ShowHand("public", ["hearts.10", "hearts.11", "hearts.12"], 1)# stage is 1-3 first stage is nothing 
  ShowHand("public", ["hearts.13"], 2)
  UpdateTurnIndicator("player_1")


  pygame.display.flip()
  


if __name__ == "__main__":
  pygame.init()
  clock = pygame.time.Clock()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        Quit()
    
    menu = GetMenu()

    if menu == "game_lock":
      New_Game()
    else:  
      if menu == "main menu":
        ShowMainMenu()
      elif menu == "settings":
        ShowSettings()
      elif menu == "help":
        ShowHelp()
      elif menu == "game":
        ChangeMenu("game_lock")
        ClearScreen() 
        DrawCardBacks(6)
  
    clock.tick(30)  #frame limit


