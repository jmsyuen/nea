import pygame
import sys
import webbrowser
import time
#reduce flicker by reducing frame updates


WIDTH, HEIGHT = 414, 896 #logical point resolution of iphone 11
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_GREY = (75, 75, 75)
#main colours
DARK_BEIGE = (204, 204, 183) #background
IVORY = (245,245,230)        #text box
OLIVE = (137, 137, 97)       #button hover 
LIGHT_GREY = (184, 184, 165) #button normal

#small card size 50x72px, big 100x144px
#includes padding of 20px around right and bottom sides
SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT = 70, 92  
BIG_CARD_WIDTH, BIG_CARD_HEIGHT = 120, 164  
#buttons
button_width, button_height = 40, 20
button_padding = 20
button_font_size = 15
button_font_colour = WHITE
button_fill_colour = BLACK
button_border_colour = WHITE
button_border_width = 1

#default values
menu = "main menu"
opponents = 3
bot_starting_chips = 5000 #5000 in intervals of 50, 5 chip types 5,2,1,50 blinds left 2 of dealer
difficulty = "medium" 
temporary_bet = 0


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
player_info_locations = dict()

for i in range(6):
  x =  140
  y =  122 + i * SMALL_CARD_HEIGHT
  player_info_locations[f"player_{i+2}"] = [x, y]
#two big cards at bottom left
#maybe big public cards at top 
#list of 9 other players with cards on right side
# reveal cards in succession by moving down 5px and flipping and up 5px again


#core ui drawing functions
def draw_button(text, box_colour, x, y, width, height, action): #draw buttons and execute function when pressed
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  hover_colour = OLIVE
  font = pygame.font.SysFont("courier", 15)
  #check if hover, might be redundant
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


def draw_text_box(text, text_colour, box_colour, font_size, x, y, width, height):
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


def open_wikipedia():
  webbrowser.open("https://en.wikipedia.org/wiki/Texas_hold_%27em")
  time.sleep(1) #prevents several instances opened at same time


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
  global difficulty
  difficulty = "easy"
def set_medium_difficulty():
  global difficulty
  difficulty = "medium"
def set_hard_difficulty():
  global difficulty
  difficulty = "hard"

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
  return [opponents + 1, difficulty, bot_starting_chips]


def quit():
  pygame.quit()
  sys.exit()



#display menu functions
def main_menu():
  ClearScreen()
  draw_text_box("Poker VS Bots", WHITE, DARK_BEIGE, 30, 0, 40, 414, 100)
  draw_button("Settings", LIGHT_GREY, 0, 250, 414, 50, settings)
  draw_button("Help", LIGHT_GREY, 0, 300, 414, 50, help)
  draw_button("Quit", LIGHT_GREY, 0, 350, 414, 50, quit)
  draw_button("Play", LIGHT_GREY, 0, 200, 414, 50, StartGame)
  pygame.display.flip()
  

def help():
  global menu
  menu = "help"
  ClearScreen()
  draw_text_box("Help", BLACK, IVORY, 15, 0, 0, 414, 40)
  draw_text_box("Welcome to Poker VS Bots!", BLACK, DARK_BEIGE, 20, 0, 40, 414, 100)
  draw_button("Wikipedia page", LIGHT_GREY, 0, 200, 414, 100, open_wikipedia)
  draw_button("Back", LIGHT_GREY, 0, HEIGHT - 100, 414, 100, MainMenu)
  pygame.display.flip()

  
def settings():
  global menu
  menu = "settings"
  ClearScreen()
  draw_text_box("Settings", BLACK, IVORY, 15, 0, 0, 414, 40)
  draw_text_box("You can only change settings before a game", BLACK, IVORY, 13, 0, 40, 414, 30)
  draw_button("Back", LIGHT_GREY, 0, HEIGHT - 100, 414, 100, MainMenu)

  #number of opponents
  draw_text_box(f"Number of opponents: {opponents}", BLACK, IVORY, 15, 0, HEIGHT - 760, 414, 40)
  draw_button("1", LIGHT_GREY, 67, HEIGHT - 700, 30, 30, set_1_opponents)
  draw_button("2", LIGHT_GREY, 117, HEIGHT - 700, 30, 30, set_2_opponents)
  draw_button("3", LIGHT_GREY, 167, HEIGHT - 700, 30, 30, set_3_opponents)
  draw_button("4", LIGHT_GREY, 217, HEIGHT - 700, 30, 30, set_4_opponents)
  draw_button("5", LIGHT_GREY, 267, HEIGHT - 700, 30, 30, set_5_opponents)
  draw_button("6", LIGHT_GREY, 317, HEIGHT - 700, 30, 30, set_6_opponents)
  #bot difficulty
  draw_text_box(f"Opponent difficulty: {difficulty}", BLACK, IVORY, 15, 0, HEIGHT - 650, 414, 40)
  draw_button("Easy", LIGHT_GREY, 20, HEIGHT - 590, 100, 30, set_easy_difficulty)
  draw_button("Medium", LIGHT_GREY, 160, HEIGHT - 590, 100, 30, set_medium_difficulty)
  draw_button("Hard", LIGHT_GREY, 300, HEIGHT - 590, 100, 30, set_hard_difficulty)
  #buy in value
  draw_text_box(f"Opponent starting chips: {bot_starting_chips}", BLACK, IVORY, 15, 0, HEIGHT - 540, 414, 40)
  draw_text_box("(you always start with 5000)", BLACK, IVORY, 15, 0, HEIGHT - 510, 414, 30)
  draw_button("5k", LIGHT_GREY, 20, HEIGHT - 460, 100, 30, set_5000_chips)
  draw_button("10k", LIGHT_GREY, 160, HEIGHT - 460, 100, 30, set_10000_chips)
  draw_button("20k", LIGHT_GREY, 300, HEIGHT - 460, 100, 30, set_20000_chips)


  pygame.display.flip()


#integration functions
def update_pot(pot):
  draw_text_box(f"Pot {pot}", BLACK, IVORY, 15, WIDTH - 160, 122, 140, 30)


def update_blinds(big_blind):
  draw_text_box(f"Blinds {big_blind // 2}/{big_blind}", BLACK, IVORY, 14, WIDTH - 160, 152, 140, 30)


def update_chips(chips):
  draw_text_box(f"Chips: {chips}", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 255, 140, 30)


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


def update_player_info(*args):   #player_id_value, prev_action, chips_left
  player_id_value = args[0]
  prev_action = args[1]
  if type(player_id_value) == str:
    player_id_value = player_id_value.split("_")[1]

  if player_id_value == 1:  #ignore showing prev_action
    if len(args) > 2:
      chips_left = args[2]
      update_chips(chips_left)
      
    
  
  else:  
    top_left_x = player_info_locations[f"player_{player_id_value}"][0]
    top_left_y = player_info_locations[f"player_{player_id_value}"][1]
  
    if len(args) > 2:
      chips_left = args[2]
      draw_text_box(f"Chips:{chips_left}", BLACK, IVORY, 13, top_left_x, top_left_y + 48, 100, 24)

    draw_text_box(f"Player {player_id_value}", BLACK, IVORY, 13, top_left_x, top_left_y, 100, 24) #change string with player name  ###
    draw_text_box(prev_action, BLACK, IVORY, 13, top_left_x, top_left_y + 24, 100, 24)  #two to be replaced with actual variables ###
  


def show_hand(*args):  #player_id in full string, cards as a list, if public choose stage
  player_id = args[0] 
  cards = args[1]
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
    

def turn_indicator(player_id):
  draw_text_box(">", BLACK, DARK_BEIGE, 20, locations[player_id][0][0] - 20, locations[player_id][0][1], 20, 20)


#buttons ADD FUNCTIONS ###

def GetAction():  #different for every set of choices
  chosen = 0
  if chosen not in [temporary_bet, fold, check]:
    return 

def increase_50():
  #cannot be bigger than chips remaining
  #if
  temporary_bet += 50
def decrease_50():
  #cannot be less than highest_bet
  #if 
  pass
def fold():
  pass
def allin():
  pass
def check():
  pass
#get a choice out of the function names
def fold_check_bet():
  #show bet amount, minimum value £0.50 to prevent raising nothing
  draw_text_box("Bet: 50", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
  draw_button("Check", LIGHT_GREY, 20 + 80, HEIGHT - 205, 60, 30, blank)
  
  draw_button("All In", LIGHT_GREY, 20, HEIGHT - 205, 60, 30, blank)
  draw_button("Fold", LIGHT_GREY, 20 + 80 + 80, HEIGHT - 205, 60, 30, blank)

  draw_button("Clear Bet", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, blank)
  draw_button("- 50", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, blank)
  draw_button("+ 50", LIGHT_GREY, WIDTH - 80, HEIGHT - 105, 60, 30, blank)
  draw_button("Confirm Raise", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, blank)


def fold_call_bet(highest_bet):
  draw_text_box(f"Bet: {highest_bet}", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
  draw_button("Call", LIGHT_GREY, 20 + 80, HEIGHT - 205, 60, 30, blank)

  draw_button("All In", LIGHT_GREY, 20, HEIGHT - 205, 60, 30, blank)
  draw_button("Fold", LIGHT_GREY, 20 + 80 + 80, HEIGHT - 205, 60, 30, blank)

  draw_button("Clear Bet", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, blank)
  draw_button("- 50", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, blank)
  draw_button("+ 50", LIGHT_GREY, WIDTH - 80, HEIGHT - 105, 60, 30, blank)
  draw_button("Confirm Raise", LIGHT_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, blank)
  

def fold_all_in(highest_bet):
  draw_text_box(f"Bet: {highest_bet}", BLACK, IVORY, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
  draw_button("All In", LIGHT_GREY, 20, HEIGHT - 205, 60, 30, blank)
  draw_button("Fold", LIGHT_GREY, 20 + 80 + 80, HEIGHT - 205, 60, 30, blank)
  #draw over in black to eliminate WHITE
  draw_text_box("", WHITE, BLACK, 15, 20 + 80, HEIGHT - 205, 60, 30)
  draw_text_box("", WHITE, BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30)
  draw_text_box("", WHITE, BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30)
  draw_text_box("", WHITE, BLACK, 15, WIDTH - 80, HEIGHT - 105, 60, 30)
  draw_text_box("", WHITE, BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30)
  #grey out with buttons that do nothing
  draw_button("Call", OLIVE, 20 + 80, HEIGHT - 205, 60, 30, blank)
  draw_button("Clear Bet", OLIVE, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, blank)
  draw_button("- 50", OLIVE, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, blank)
  draw_button("+ 50", OLIVE, WIDTH - 80, HEIGHT - 105, 60, 30, blank)
  draw_button("Confirm Raise", OLIVE, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, blank)


def announce_winners(winners, combination, combination_high):
  draw_text_box("Winning combination", BLACK, IVORY, 11, WIDTH - 160, 422, 140, 24)
  draw_text_box(f"{combination}", BLACK, IVORY, 15, WIDTH - 160, 446, 140, 24)#
  draw_text_box(f"{combination_high} high", BLACK, IVORY, 15, WIDTH - 160, 470, 140, 24)# 

  draw_text_box("Winner(s)", BLACK, IVORY, 15, WIDTH - 160, 214, 140, 24)
  for i in range(len(winners)):  #winner in winners
    draw_text_box(f"{winners[i]}", BLACK, IVORY, 15, WIDTH - 160, 238 + i * 24, 140, 24)


def show_finalist_cards(hands, finalists): #using a dictionary of player_id:cards
  for player_id in finalists:
    show_hand(hands[player_id], player_id)


'''
def menu_confirm(): #continue to next round or save #may be unused
  draw_text_box("Save and exit?", BLACK, WHITE, 11, WIDTH - 160, HEIGHT - 375, 140, 24)
  draw_button("Yes", BLACK, WIDTH - 80, HEIGHT - 345, 60, 30, MainMenu)
  draw_button("No", BLACK, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 345, 60, 30, blank)  #hide prompt 
'''

def menu_button():
  draw_button("Menu", LIGHT_GREY, WIDTH - 79, HEIGHT - 305, 60, 30, MainMenu)


def draw_game(bot_starting_chips, opponents):   #first time draw
  #5 small cards at top
  for i in range(5):
    draw_card("small", "back", locations["public"][i])
  
  #list of players on left for right handed players on mobile
  for player_id_value in range(2, 2 + opponents):  #range of other opponents #player in players ########change this range
    player_id = f"player_{player_id_value}"
    draw_card("small", "back", locations[player_id][0])
    draw_card("small", "back", locations[player_id][1])

    update_player_info(player_id_value, "", bot_starting_chips) ###change to starting chips total_chips_left
  
  #big cards bottom left
  draw_card("big", "back", locations["player_1"][0])
  draw_card("big", "back", locations["player_1"][1])
  
  pygame.display.flip()


def New_Game():  #testing displays
  #dynamic variables to be udpated
  update_pot(200000)
  update_blinds(2000)
  update_chips(5000)
  #fetch settings when new game is started
  
  fold_all_in(500)
  announce_winners(["player_1", "player_3"], "Three of kind", 6)
  show_hand("player_2", ["spades.3", "diamonds.9"])
  show_hand("player_1", ["spades.14", "diamonds.14"])
  show_hand("public", ["hearts.10", "hearts.11", "hearts.12"], 1)# stage is 1-3 first stage is nothing 
  show_hand("public", ["hearts.13"], 2)
  turn_indicator("player_1")
  menu_button()

  pygame.display.flip()
  


if __name__ == "__main__":
  pygame.init()
  clock = pygame.time.Clock()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
    
    menu = GetMenu()

    if menu == "game_lock":
      New_Game()
    else:  
      if menu == "main menu":
        main_menu()
      elif menu == "settings":
        settings()
      elif menu == "help":
        help()
      elif menu == "game":
        ChangeMenu("game_lock")
        ClearScreen() 
        draw_game(5000, 4)
  
    clock.tick(30)  #frame limit


