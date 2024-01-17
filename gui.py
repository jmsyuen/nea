import pygame
import sys
import webbrowser
import time
#reduce flicker by reducing frame updates

class ui():
  def __init__(self):
    #origin at top left
    
    self.WIDTH, self.HEIGHT = 414, 896 #logical point resolution of iphone 11
    self.WHITE = (255, 255, 255)
    self.GREEN = (0, 128, 0)
    self.RED = (255, 0, 0)
    self.BLACK = (0, 0, 0)
    self.DARK_GREY = (75, 75, 75)
    #main colours
    self.DARK_BEIGE = (204, 204, 183) #background
    self.IVORY = (245,245,230)        #text box
    self.OLIVE = (137, 137, 97)       #button hover 
    self.LIGHT_GREY = (184, 184, 165) #button normal
    
    #small card size 50x72px, big 100x144px
    #includes padding of 20px around right and bottom sides
    self.SMALL_CARD_WIDTH, self.SMALL_CARD_HEIGHT = 70, 92  
    self.BIG_CARD_WIDTH, self.BIG_CARD_HEIGHT = 120, 164  
    #buttons
    self.button_width, self.button_height = 40, 20
    self.button_padding = 20
    self.button_font_size = 15
    self.button_font_colour = self.WHITE
    self.button_fill_colour = self.BLACK
    self.button_border_colour = self.WHITE
    self.button_border_width = 1

    #default values
    self.menu = "main menu"
    self.opponents = 3
    self.bot_starting_chips = 5000 #5000 in intervals of 50, 5 chip types 5,2,1,50 blinds left 2 of dealer
    self.difficulty = "medium" 
    self.temporary_bet = 0


    # start pygame window
    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    pygame.display.set_caption("Poker VS Bots")

    # load images
    self.small_card_images = []  # https://code.google.com/archive/p/vector-playing-cards/
    self.big_card_images = []
    self.back = [] #small, big
    self.suits = ("hearts", "diamonds", "spades", "clubs")
    
    for suit in self.suits:
      for value in range(2, 15):
        self.small_card_images.append(pygame.image.load(f"small_cards/{suit}.{value}.png"))  
        self.big_card_images.append(pygame.image.load(f"big_cards/{suit}.{value}.png"))

    self.back.append(pygame.image.load(f"small_cards/back.png"))
    self.back.append(pygame.image.load(f"big_cards/back.png"))

    #screen locations of cards 
    self.locations = dict() #size of cards followed by x and y of each
    self.locations["public"] = tuple((40 + i * self.SMALL_CARD_WIDTH, 20) for i in range(5))
    self.locations["player_1"] = [(20, self.HEIGHT - 162), (20 + self.BIG_CARD_WIDTH, self.HEIGHT - 162)]
    for player_id_value in range(2,8):  #range of other opponents #player in players
      location1 = (20, 122 + (player_id_value-2) * self.SMALL_CARD_HEIGHT)
      location2 = (80, 122 + (player_id_value-2) * self.SMALL_CARD_HEIGHT)
      self.locations[f"player_{player_id_value}"] = [location1, location2]
    

    #screen locations of info boxes
    self.player_info_locations = dict()

    for i in range(6):
      x =  140
      y =  122 + i * self.SMALL_CARD_HEIGHT
      self.player_info_locations[f"player_{i+2}"] = [x, y]
    #two big cards at bottom left
    #maybe big public cards at top 
    #list of 9 other players with cards on right side
    # reveal cards in succession by moving down 5px and flipping and up 5px again


  #core ui drawing functions
  def draw_button(self, text, box_colour, x, y, width, height, action): #draw buttons and execute function when pressed
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hover_colour = self.OLIVE
    font = pygame.font.SysFont("courier", 15)
    #check if hover, might be redundant
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
      pygame.draw.rect(self.screen, hover_colour, (x, y, width, height))
      if click[0] == 1:
        action()
    else:
      pygame.draw.rect(self.screen, box_colour, (x, y, width, height))

    #white border
    border_width = 1
    pygame.draw.rect(self.screen, self.WHITE, (x, y, width, height), border_width)

    #add text
    text_surface = font.render(text, True, self.WHITE)
    text_rect = text_surface.get_rect()
    #add text to centre
    text_rect.center = ((x + (width // 2)), (y + (height // 2)))
    self.screen.blit(text_surface, text_rect)


  def draw_text_box(self, text, text_colour, box_colour, font_size, x, y, width, height):
    font = pygame.font.SysFont("courier", font_size)
    
    pygame.draw.rect(self.screen, box_colour, (x, y, width, height))
    text_surface = font.render(text, True, text_colour)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    self.screen.blit(text_surface, text_rect)


  def ClearScreen(self):
    self.screen.fill(self.DARK_BEIGE)  #background
    #pygame.display.flip()


  def blank(self):  #dummy for greyed out button
    pass


  def GetMenu(self):
    return self.menu
  

  def ChangeMenu(self, menu):
    self.menu = menu 


  def MainMenu(self):
    self.ChangeMenu("main menu")
  

  def StartGame(self):
    self.ChangeMenu("game")


  def open_wikipedia(self):
    webbrowser.open("https://en.wikipedia.org/wiki/Texas_hold_%27em")
    time.sleep(1) #prevents several instances opened at same time


  def set_1_opponents(self):
    self.opponents = 1
  def set_2_opponents(self):
    self.opponents = 2
  def set_3_opponents(self):
    self.opponents = 3
  def set_4_opponents(self):
    self.opponents = 4
  def set_5_opponents(self):
    self.opponents = 5
  def set_6_opponents(self):
    self.opponents = 6
  
  def set_easy_difficulty(self):
    self.difficulty = "easy"
  def set_medium_difficulty(self):
    self.difficulty = "medium"
  def set_hard_difficulty(self):
    self.difficulty = "hard"

  def set_5000_chips(self):
    self.bot_starting_chips = 5000
  def set_10000_chips(self):
    self.bot_starting_chips = 10000
  def set_20000_chips(self):
    self.bot_starting_chips = 20000

  def GetSettings(self):
    return [self.opponents + 1, self.difficulty, self.bot_starting_chips]


  def quit(self):
    pygame.quit()
    sys.exit()



  #display menu functions
  def main_menu(self):
    self.ClearScreen()
    self.draw_text_box("Poker VS Bots", self.WHITE, self.DARK_BEIGE, 30, 0, 40, 414, 100)
    self.draw_button("Settings", self.LIGHT_GREY, 0, 250, 414, 50, self.settings)
    self.draw_button("Help", self.LIGHT_GREY, 0, 300, 414, 50, self.help)
    self.draw_button("Quit", self.LIGHT_GREY, 0, 350, 414, 50, self.quit)
    self.draw_button("Play", self.LIGHT_GREY, 0, 200, 414, 50, self.StartGame)
    pygame.display.flip()
    

  def help(self):
    self.menu = "help"
    self.ClearScreen()
    self.draw_text_box("Help", self.BLACK, self.IVORY, 15, 0, 0, 414, 40)
    self.draw_text_box("Welcome to Poker VS Bots!", self.BLACK, self.DARK_BEIGE, 20, 0, 40, 414, 100)
    self.draw_button("Wikipedia page", self.LIGHT_GREY, 0, 200, 414, 100, self.open_wikipedia)
    self.draw_button("Back", self.LIGHT_GREY, 0, self.HEIGHT - 100, 414, 100, self.MainMenu)
    pygame.display.flip()

    
  def settings(self):
    self.menu = "settings"
    self.ClearScreen()
    self.draw_text_box("Settings", self.BLACK, self.IVORY, 15, 0, 0, 414, 40)
    self.draw_text_box("You can only change settings before a game", self.BLACK, self.IVORY, 13, 0, 40, 414, 30)
    self.draw_button("Back", self.LIGHT_GREY, 0, self.HEIGHT - 100, 414, 100, self.MainMenu)

    #number of opponents
    self.draw_text_box(f"Number of opponents: {self.opponents}", self.BLACK, self.IVORY, 15, 0, self.HEIGHT - 760, 414, 40)
    self.draw_button("1", self.LIGHT_GREY, 67, self.HEIGHT - 700, 30, 30, self.set_1_opponents)
    self.draw_button("2", self.LIGHT_GREY, 117, self.HEIGHT - 700, 30, 30, self.set_2_opponents)
    self.draw_button("3", self.LIGHT_GREY, 167, self.HEIGHT - 700, 30, 30, self.set_3_opponents)
    self.draw_button("4", self.LIGHT_GREY, 217, self.HEIGHT - 700, 30, 30, self.set_4_opponents)
    self.draw_button("5", self.LIGHT_GREY, 267, self.HEIGHT - 700, 30, 30, self.set_5_opponents)
    self.draw_button("6", self.LIGHT_GREY, 317, self.HEIGHT - 700, 30, 30, self.set_6_opponents)
    #bot difficulty
    self.draw_text_box(f"Opponent difficulty: {self.difficulty}", self.BLACK, self.IVORY, 15, 0, self.HEIGHT - 650, 414, 40)
    self.draw_button("Easy", self.LIGHT_GREY, 20, self.HEIGHT - 590, 100, 30, self.set_easy_difficulty)
    self.draw_button("Medium", self.LIGHT_GREY, 160, self.HEIGHT - 590, 100, 30, self.set_medium_difficulty)
    self.draw_button("Hard", self.LIGHT_GREY, 300, self.HEIGHT - 590, 100, 30, self.set_hard_difficulty)
    #buy in value
    self.draw_text_box(f"Opponent starting chips: {self.bot_starting_chips}", self.BLACK, self.IVORY, 15, 0, self.HEIGHT - 540, 414, 40)
    self.draw_text_box("(you always start with 5000)", self.BLACK, self.IVORY, 15, 0, self.HEIGHT - 510, 414, 30)
    self.draw_button("5k", self.LIGHT_GREY, 20, self.HEIGHT - 460, 100, 30, self.set_5000_chips)
    self.draw_button("10k", self.LIGHT_GREY, 160, self.HEIGHT - 460, 100, 30, self.set_10000_chips)
    self.draw_button("20k", self.LIGHT_GREY, 300, self.HEIGHT - 460, 100, 30, self.set_20000_chips)


    pygame.display.flip()


  #integration functions
  def update_pot(self, pot):
    self.draw_text_box(f"Pot {pot}", self.BLACK, self.IVORY, 15, self.WIDTH - 160, 122, 140, 30)


  def update_blinds(self, big_blind):
    self.draw_text_box(f"Blinds {big_blind // 2}/{big_blind}", self.BLACK, self.IVORY, 14, self.WIDTH - 160, 152, 140, 30)
  

  def update_chips(self, chips):
    self.draw_text_box(f"Chips: {chips}", self.BLACK, self.IVORY, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 255, 140, 30)

  
  def draw_card(self, size, card, position): #takes card like spades.3, and xy position as tuple
    if card == "back":
      if size == "small":
        self.screen.blit(self.back[0], position)
      elif size == "big":
        self.screen.blit(self.back[1], position)
      
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
      self.screen.blit(self.small_card_images[list_index], position)
    elif size == "big":
      self.screen.blit(self.big_card_images[list_index], position)
    
    pygame.display.flip()
    return


  def update_player_info(self, *args):   #player_id_value, prev_action, chips_left
    player_id_value = args[0]
    prev_action = args[1]
    if type(player_id_value) == str:
      player_id_value = player_id_value.split("_")[1]

    if player_id_value == 1:  #ignore showing prev_action
      if len(args) > 2:
        chips_left = args[2]
        self.update_chips(chips_left)
        
      
   
    else:  
      top_left_x = self.player_info_locations[f"player_{player_id_value}"][0]
      top_left_y = self.player_info_locations[f"player_{player_id_value}"][1]
    
      if len(args) > 2:
        chips_left = args[2]
        self.draw_text_box(f"Chips:{chips_left}", self.BLACK, self.IVORY, 13, top_left_x, top_left_y + 48, 100, 24)

      self.draw_text_box(f"Player {player_id_value}", self.BLACK, self.IVORY, 13, top_left_x, top_left_y, 100, 24) #change string with player name  ###self.
      self.draw_text_box(prev_action, self.BLACK, self.IVORY, 13, top_left_x, top_left_y + 24, 100, 24)  #two to be replaced with actual variables ###
    


  def show_hand(self, *args):  #player_id in full string, cards as a list, if public choose stage
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
      self.draw_card(size, card, self.locations[player_id][position])
      position += 1
      
    #self.locations as an xy tuple
      
  
  def turn_indicator(self, player_id):
    self.draw_text_box(">", self.BLACK, self.DARK_BEIGE, 20, self.locations[player_id][0][0] - 20, self.locations[player_id][0][1], 20, 20)


#buttons ADD FUNCTIONS ###
  
  def GetAction(self):  #different for every set of choices
    chosen = 0
    if chosen not in [self.temporary_bet, self.fold, self.check]:
      return 

  def increase_50(self):
    #cannot be bigger than chips remaining
    #if
    temporary_bet += 50
  def decrease_50(self):
    #cannot be less than highest_bet
    #if 
    pass
  def fold(self):
    pass
  def allin(self):
    pass
  def check(self):
    pass
  
  #get a choice out of the function names
  def fold_check_bet(self):
    #show bet amount, minimum value £0.50 to prevent raising nothing
    self.draw_text_box("Bet: 50", self.BLACK, self.IVORY, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("Check", self.LIGHT_GREY, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    
    self.draw_button("All In", self.LIGHT_GREY, 20, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Fold", self.LIGHT_GREY, 20 + 80 + 80, self.HEIGHT - 205, 60, 30, self.blank)

    self.draw_button("Clear Bet", self.LIGHT_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30, self.blank)
    self.draw_button("- 50", self.LIGHT_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("+ 50", self.LIGHT_GREY, self.WIDTH - 80, self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("Confirm Raise", self.LIGHT_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30, self.blank)


  def fold_call_bet(self, highest_bet):
    self.draw_text_box(f"Bet: {highest_bet}", self.BLACK, self.IVORY, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("Call", self.LIGHT_GREY, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)

    self.draw_button("All In", self.LIGHT_GREY, 20, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Fold", self.LIGHT_GREY, 20 + 80 + 80, self.HEIGHT - 205, 60, 30, self.blank)

    self.draw_button("Clear Bet", self.LIGHT_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30, self.blank)
    self.draw_button("- 50", self.LIGHT_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("+ 50", self.LIGHT_GREY, self.WIDTH - 80, self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("Confirm Raise", self.LIGHT_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30, self.blank)
    

  def fold_all_in(self, highest_bet):
    self.draw_text_box(f"Bet: {highest_bet}", self.BLACK, self.IVORY, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("All In", self.LIGHT_GREY, 20, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Fold", self.LIGHT_GREY, 20 + 80 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    #draw over in black to eliminate self.WHITE
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 20 + 80, self.HEIGHT - 205, 60, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, self.WIDTH - 80, self.HEIGHT - 105, 60, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30)
    #grey out with buttons that do nothing
    self.draw_button("Call", self.OLIVE, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Clear Bet", self.OLIVE, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30, self.blank)
    self.draw_button("- 50", self.OLIVE, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("+ 50", self.OLIVE, self.WIDTH - 80, self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("Confirm Raise", self.OLIVE, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30, self.blank)


  def announce_winners(self, winners, combination, combination_high):
    self.draw_text_box("Winning combination", self.BLACK, self.IVORY, 11, self.WIDTH - 160, 422, 140, 24)
    self.draw_text_box(f"{combination}", self.BLACK, self.IVORY, 15, self.WIDTH - 160, 446, 140, 24)#
    self.draw_text_box(f"{combination_high} high", self.BLACK, self.IVORY, 15, self.WIDTH - 160, 470, 140, 24)# 

    self.draw_text_box("Winner(s)", self.BLACK, self.IVORY, 15, self.WIDTH - 160, 214, 140, 24)
    for i in range(len(winners)):  #winner in winners
      self.draw_text_box(f"{winners[i]}", self.BLACK, self.IVORY, 15, self.WIDTH - 160, 238 + i * 24, 140, 24)


  def show_finalist_cards(self, hands, finalists): #using a dictionary of player_id:cards
    for player_id in finalists:
      self.show_hand(hands[player_id], player_id)


  '''
  def menu_confirm(self): #continue to next round or save #may be unused
    self.draw_text_box("Save and exit?", self.BLACK, self.WHITE, 11, self.WIDTH - 160, self.HEIGHT - 375, 140, 24)
    self.draw_button("Yes", self.BLACK, self.WIDTH - 80, self.HEIGHT - 345, 60, 30, self.MainMenu)
    self.draw_button("No", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 345, 60, 30, self.blank)  #hide prompt 
  '''

  def menu_button(self):
    self.draw_button("Menu", self.LIGHT_GREY, self.WIDTH - 79, self.HEIGHT - 305, 60, 30, self.MainMenu)


  def draw_game(self, bot_starting_chips, opponents):   #first time draw
    #5 small cards at top
    for i in range(5):
      self.draw_card("small", "back", self.locations["public"][i])
    
    #list of players on left for right handed players on mobile
    for player_id_value in range(2, 2 + opponents):  #range of other opponents #player in players ########change this range
      player_id = f"player_{player_id_value}"
      self.draw_card("small", "back", self.locations[player_id][0])
      self.draw_card("small", "back", self.locations[player_id][1])

      self.update_player_info(player_id_value, "", bot_starting_chips) ###change to starting chips total_chips_left
    
    #big cards bottom left
    self.draw_card("big", "back", self.locations["player_1"][0])
    self.draw_card("big", "back", self.locations["player_1"][1])
    
    pygame.display.flip()


  def New_Game(self):  #testing displays
    #dynamic variables to be udpated
    self.update_pot(200000)
    self.update_blinds(2000)
    self.update_chips(5000)
    #fetch settings when new game is started
    
    self.fold_all_in(500)
    self.announce_winners(["player_1", "player_3"], "Three of kind", 6)
    self.show_hand("player_2", ["spades.3", "diamonds.9"])
    self.show_hand("player_1", ["spades.14", "diamonds.14"])
    self.show_hand("public", ["hearts.10", "hearts.11", "hearts.12"], 1)# stage is 1-3 first stage is nothing 
    self.show_hand("public", ["hearts.13"], 2)
    self.turn_indicator("player_1")
    self.menu_button()

    pygame.display.flip()
    


if __name__ == "__main__":
  ui = ui()
  pygame.init()
  clock = pygame.time.Clock()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        ui.quit()
    
    menu = ui.GetMenu()

    if menu == "game_lock":
      ui.New_Game()
    else:  
      if menu == "main menu":
        ui.main_menu()
      elif menu == "settings":
        ui.settings()
      elif menu == "help":
        ui.help()
      elif menu == "game":
        ui.ChangeMenu("game_lock")
        ui.ClearScreen() 
        ui.draw_game(5000, 4)
  
    clock.tick(30)  #frame limit


