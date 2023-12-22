import pygame
import sys
import random
import time
import webbrowser



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

    for suit in ("hearts", "diamonds", "spades", "clubs"):
      for value in range(2, 15):
        self.small_card_images.append(pygame.image.load(f"small_cards/{suit}.{value}.png"))  
        self.big_card_images.append(pygame.image.load(f"big_cards/{suit}.{value}.png"))

    #map index 2-14 to 0-12, add offset of 13 for each suit

    self.back.append(pygame.image.load(f"small_cards/back.png"))
    self.back.append(pygame.image.load(f"big_cards/back.png"))


    #two big cards at bottom left
    #maybe big public cards at top 
    #list of 9 other players with cards on right side
    # reveal cards in succession by moving down 5px and flipping and up 5px again





  #draw buttons and execute function when pressed
  def draw_button(self, text, box_colour, x, y, width, height, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hover_colour = self.GREY
    font = pygame.font.SysFont("courier", 15)
    #check if hover
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


  #for greyed out button
  def blank(self):  
    pass


  def GetMenu(self):
    return self.menu
  

  def GoBack(self):
    self.menu = "main menu"
  

  def main_menu(self):
    self.screen.fill(self.BLACK)
    self.draw_text_box("Poker VS Bots", self.WHITE, self.BLACK, 30, 0, 40, 414, 100)
    self.draw_button("Play", self.BLACK, 0, 200, 414, 50, self.draw_game)
    self.draw_button("Settings", self.BLACK, 0, 250, 414, 50, self.settings)
    self.draw_button("Help", self.BLACK, 0, 300, 414, 50, self.help)
    self.draw_button("Quit", self.BLACK, 0, 350, 414, 50, self.quit)


    pygame.display.flip()
    #draw_button("New Game", LIGHTGREY, 375, 460, 100,
    #play game, settings, help, quit button




  def open_wikipedia(self):
    webbrowser.open("https://en.wikipedia.org/wiki/Texas_hold_%27em")
    time.sleep(1)


  def help(self):
    self.menu = "help"
    self.screen.fill(self.BLACK)
    self.draw_text_box("Welcome to Poker VS Bots!", self.WHITE, self.BLACK, 20, 0, 40, 414, 100)
    self.draw_button("Wikipedia page", self.BLACK, 0, 200, 414, 100, self.open_wikipedia)
    self.draw_button("Back", self.BLACK, 0, self.HEIGHT - 100, 414, 100, self.GoBack)
    
    #if button pressed
    pygame.display.flip()
    return "help"
    

  def settings(self):
    self.menu = "settings"
    self.screen.fill(self.BLACK)
    self.draw_button("Back", self.BLACK, 0, self.HEIGHT - 100, 414, 100, self.GoBack)
    pygame.display.flip()


  def quit(self):
    pygame.quit()
    sys.exit()

  # Main game loop
  def draw_game(self):
    self.menu = "game"
    self.cards_on_table = [random.randint(1, 52) for i in range(5)]
    self.player_hand = [random.randint(1, 52) for i in range(2)]

    
    self.screen.fill(self.BLACK)  #background
    #5 small cards at top
    for i in range(5):
      self.screen.blit(self.back[0], (40 + i * self.SMALL_CARD_WIDTH, 20))
    
    #list of players on left for right handed players on mobile
    for i in range(6):  #range of other opponents #player in players
      self.screen.blit(self.back[0], (20, 122 + i * self.SMALL_CARD_HEIGHT))
      self.screen.blit(self.back[0], (80, 122 + i * self.SMALL_CARD_HEIGHT))
      self.draw_text_box("player 1", self.BLACK, self.WHITE, 13, 140, 122 + i * self.SMALL_CARD_HEIGHT, 100, 24) #change string with player name  ###self.
      self.draw_text_box("", self.BLACK, self.WHITE, 13, 140, 146 + i * self.SMALL_CARD_HEIGHT, 100, 24)  #two to be replaced with actual variables ###
      self.draw_text_box("Chips:£50.00", self.BLACK, self.WHITE, 13, 140, 170 + i * self.SMALL_CARD_HEIGHT, 100, 24)

    #pot
    self.draw_text_box("Pot: £20.00", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 122, 140, 30)

    #big cards bottom left
    self.screen.blit(self.back[1], (20, self.HEIGHT - 162))
    self.screen.blit(self.back[1], (20 + self.BIG_CARD_WIDTH, self.HEIGHT - 162))

    #buttons ADD FUNCTIONS ###      
    self.draw_text_box("Chips: £20.50", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 255, 140, 30)
    self.draw_button("All In", self.BLACK, 20, self.HEIGHT - 205, 60, 30, self.blank)
    self.draw_button("Fold", self.BLACK, 20 + 80 + 80, self.HEIGHT - 205, 60, 30, self.blank)

    self.draw_button("Clear Bet", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 55, 140, 30, self.blank)
    self.draw_button("- 50p", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("+ 50p", self.BLACK, self.WIDTH - 80, self.HEIGHT - 105, 60, 30, self.blank)
    self.draw_button("Confirm Raise", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 155, 140, 30, self.blank)


    self.fold_all_in()
    self.show_winners()
    #update display
    pygame.display.flip()

  def fold_check_bet(self):
    self.draw_text_box("Bet: £0.50", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("Check", self.BLACK, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    #show bet amount, minimum value £0.50 to prevent raising nothing

  def fold_call_bet(self):
    self.draw_text_box("Bet: £10.00", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
    self.draw_button("Call", self.BLACK, 20 + 80, self.HEIGHT - 205, 60, 30, self.blank)
    
  def fold_all_in(self):
    self.draw_text_box("Bet: £50", self.BLACK, self.WHITE, 15, 15 + self.BIG_CARD_WIDTH*2, self.HEIGHT - 205, 140, 30)
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

  def show_winners(self):
    self.draw_text_box("Winning combination", self.BLACK, self.WHITE, 11, self.WIDTH - 160, 422, 140, 24)
    self.draw_text_box("Three of a kind", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 446, 140, 24)#
    self.draw_text_box("6 high", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 470, 140, 24)# 

    self.draw_text_box("Winner(s)", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 214, 140, 24)
    for i in range(7):
      self.draw_text_box("player_1", self.BLACK, self.WHITE, 15, self.WIDTH - 160, 238 + i * 24, 140, 24)
    
    #continue to next round or save
    self.draw_text_box("Save and exit?", self.BLACK, self.WHITE, 11, self.WIDTH - 160, self.HEIGHT - 375, 140, 24)
    self.draw_button("Yes", self.BLACK, 15 + self.BIG_CARD_WIDTH*2 , self.HEIGHT - 345, 60, 30, self.blank)
    self.draw_button("No", self.BLACK, self.WIDTH - 80, self.HEIGHT - 345, 60, 30, self.blank)

    

  def flip_card(self):
    pass


ui = ui()

pygame.init()
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      ui.quit()
  
  menu = ui.GetMenu()
  if menu == "main menu":
    ui.main_menu()
  elif menu == "settings":
    ui.settings()
  elif menu == "help":
    ui.help()
  elif menu == "game":
    ui.draw_game()
  
  #draw_game()
  

