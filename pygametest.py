import pygame
import sys
import webbrowser

import random
import time


class ui():
  def __init__(self):
    #origin at top left
    
    self.WIDTH, self.HEIGHT = 414, 896 #logical point resolution of iphone 11
    self.WHITE = (255, 255, 255)
    self.GREEN = (0, 128, 0)
    self.RED = (255, 0, 0)
    self.BLACK = (0, 0, 0)
    self.GREY = (105, 105, 105)
    self.DARK_GREY = (75, 75, 75)
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

    self.menu = "main menu"


    # Initialize Pygame window
    self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
    pygame.display.set_caption("Poker VS Bots")

    # Load card images
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
    hover_colour = self.GREY
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
    self.screen.fill(self.BLACK)  #background
    pygame.display.flip()


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
    time.sleep(1)


  def quit(self):
    pygame.quit()
    sys.exit()



  #display menu functions
  def main_menu(self):
    self.ClearScreen()
    self.draw_text_box("Poker VS Bots", self.WHITE, self.BLACK, 30, 0, 40, 414, 100)
    self.draw_button("Settings", self.BLACK, 0, 250, 414, 50, self.settings)
    self.draw_button("Help", self.BLACK, 0, 300, 414, 50, self.help)
    self.draw_button("Quit", self.BLACK, 0, 350, 414, 50, self.quit)
    self.draw_button("Play", self.BLACK, 0, 200, 414, 50, self.StartGame)
    pygame.display.flip()
    


  def help(self):
    self.menu = "help"
    self.ClearScreen()
    self.draw_text_box("Welcome to Poker VS Bots!", self.WHITE, self.BLACK, 20, 0, 40, 414, 100)
    self.draw_button("Wikipedia page", self.BLACK, 0, 200, 414, 100, self.open_wikipedia)
    self.draw_button("Back", self.BLACK, 0, self.HEIGHT - 100, 414, 100, self.MainMenu)
    pygame.display.flip()

    
  def settings(self):
    self.menu = "settings"
    self.ClearScreen()
    self.draw_button("Back", self.BLACK, 0, self.HEIGHT - 100, 414, 100, self.MainMenu)
    pygame.display.flip()


  #integration functions
  def update_pot(self, pot):
    self.draw_text_box(f"Pot: {pot}", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 122, 140, 30)

  
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


  def draw_player_info(self, player_id_value, prev_action, chips_left):
    top_left_x = self.player_info_locations[f"player_{player_id_value}"][0]
    top_left_y = self.player_info_locations[f"player_{player_id_value}"][1]

    self.draw_text_box(f"Player {player_id_value}", self.BLACK, self.WHITE, 13, top_left_x, top_left_y, 100, 24) #change string with player name  ###self.
    self.draw_text_box(prev_action, self.BLACK, self.WHITE, 13, top_left_x, top_left_y + 24, 100, 24)  #two to be replaced with actual variables ###
    self.draw_text_box(f"Chips:{chips_left}", self.BLACK, self.WHITE, 13, top_left_x, top_left_y + 48, 100, 24)


  def flip_card(self, size, new_card, position):  #position as an xy tuple
    self.draw_card(size, new_card, position)
    

#buttons ADD FUNCTIONS ###      
  def fold_check_bet(self):
    #show bet amount, minimum value £0.50 to prevent raising nothing
    self.draw_text_box("Bet: £0.50", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("Check", self.BLACK, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    
    self.draw_button("All In", self.BLACK, 20, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Fold", self.BLACK, 20 + 80 + 80, self.HEIGHT - 205, 60, 30, self.blank)

    self.draw_button("Clear Bet", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30, self.blank)
    self.draw_button("- 50p", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("+ 50p", self.BLACK, self.WIDTH - 80, self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("Confirm Raise", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30, self.blank)


  def fold_call_bet(self, highest_bet):
    self.draw_text_box(f"Bet: {highest_bet}", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("Call", self.BLACK, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)

    self.draw_button("All In", self.BLACK, 20, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Fold", self.BLACK, 20 + 80 + 80, self.HEIGHT - 205, 60, 30, self.blank)

    self.draw_button("Clear Bet", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30, self.blank)
    self.draw_button("- 50p", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("+ 50p", self.BLACK, self.WIDTH - 80, self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("Confirm Raise", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30, self.blank)
    

  def fold_all_in(self, highest_bet):
    self.draw_text_box(f"Bet: {highest_bet}", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("All In", self.BLACK, 20, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Fold", self.BLACK, 20 + 80 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    #draw over in black to eliminate self.WHITE
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 20 + 80, self.HEIGHT - 205, 60, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, self.WIDTH - 80, self.HEIGHT - 105, 60, 30)
    self.draw_text_box("", self.WHITE, self.BLACK, 15, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30)
    #grey out with buttons that do nothing
    self.draw_button("Call", self.DARK_GREY, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Clear Bet", self.DARK_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30, self.blank)
    self.draw_button("- 50p", self.DARK_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("+ 50p", self.DARK_GREY, self.WIDTH - 80, self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("Confirm Raise", self.DARK_GREY, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30, self.blank)


  def show_winners(self, winners, combination, combination_high):
    self.draw_text_box("Winning combination", self.BLACK, self.WHITE, 11, self.WIDTH - 160, 422, 140, 24)
    self.draw_text_box(f"{combination}", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 446, 140, 24)#
    self.draw_text_box(f"{combination_high} high", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 470, 140, 24)# 

    self.draw_text_box("Winner(s)", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 214, 140, 24)
    for i in range(len(winners)):  #winner in winners
      self.draw_text_box(f"{winners[i]}", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 238 + i * 24, 140, 24)


  def ask_save(self): #continue to next round or save #may be unused
    self.draw_text_box("Save and exit?", self.BLACK, self.WHITE, 11, self.WIDTH - 160, self.HEIGHT - 375, 140, 24)
    self.draw_button("Yes", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 345, 60, 30, self.MainMenu)
    self.draw_button("No", self.BLACK, self.WIDTH - 80, self.HEIGHT - 345, 60, 30, self.blank)


  def draw_game(self):
    #first time draw
    

    #5 small cards at top
    for i in range(5):
      self.draw_card("small", "back", self.locations["public"][i])
    
    #list of players on left for right handed players on mobile
    for player_id_value in range(2, 8):  #range of other opponents #player in players ########change this range
      player_id = f"player_{player_id_value}"
      self.draw_card("small", "back", self.locations[player_id][0])
      self.draw_card("small", "back", self.locations[player_id][1])

      self.draw_player_info(player_id_value, "Check test", 5000) ###change to starting chips total_chips_left
    
    #big cards bottom left
    self.draw_card("big", "back", self.locations["player_1"][0])
    self.draw_card("big", "back", self.locations["player_1"][1])
    
    pygame.display.flip()


  def game_loop(self):  #used to integrate with main.py
    #dynamic variables to be udpated
    self.update_pot(20.00)
    self.draw_text_box("Chips: £50.00", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 255, 140, 30)

    self.fold_all_in(500)
    self.show_winners(["player_1", "player_3"], "Three of kind", 6)
    self.flip_card("small", "spades.4",self.locations["public"][0])
    self.flip_card("small", "clubs.14",self.locations["player_5"][1])

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
      ui.game_loop()
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
        ui.draw_game()
  
    clock.tick(30)


