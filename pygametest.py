import pygame
import sys
import random
import time

pygame.init()

# Constants
#origin at top left
WIDTH, HEIGHT = 414, 896 #logical point resolution of iphone 11
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (105, 105, 105)
DARK_GREY = (75, 75, 75)
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




# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poker")

# Load card images
small_card_images = []  # https://code.google.com/archive/p/vector-playing-cards/
big_card_images = []
back = [] #small, big

for suit in ("hearts", "diamonds", "spades", "clubs"):
  for value in range(2, 15):
    small_card_images.append(pygame.image.load(f"small_cards/{suit}.{value}.png"))  
    big_card_images.append(pygame.image.load(f"big_cards/{suit}.{value}.png"))

#map index 2-14 to 0-12, add offset of 13 for each suit

back.append(pygame.image.load(f"small_cards/back.png"))
back.append(pygame.image.load(f"big_cards/back.png"))


#two big cards at bottom left
#maybe big public cards at top 
#list of 9 other players with cards on right side
# reveal cards in succession by moving down 5px and flipping and up 5px again





#draw buttons and execute function when pressed
def draw_button(text, box_colour, x, y, width, height, action):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  hover_colour = GREY
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
  pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), border_width)

  #add text
  text_surface = font.render(text, True, WHITE)
  text_rect = text_surface.get_rect()
  #add text to centre
  text_rect.center = ((x + (width // 2)), (y + (height // 2)))
  screen.blit(text_surface, text_rect)


def draw_text_box(text, box_colour, font_size, x, y, width, height):
  text_colour = BLACK
  font = pygame.font.SysFont("courier", font_size)
  
  pygame.draw.rect(screen, box_colour, (x, y, width, height))
  text_surface = font.render(text, True, text_colour)
  text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
  screen.blit(text_surface, text_rect)


#for greyed out button
def blank():  
  pass



# Main game loop
def draw_game():
  cards_on_table = [random.randint(1, 52) for i in range(5)]
  player_hand = [random.randint(1, 52) for i in range(2)]

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    screen.fill(BLACK)  #background
    #5 small cards at top
    for i in range(5):
      screen.blit(back[0], (40 + i * SMALL_CARD_WIDTH, 20))
    
    #list of players on left for right handed players on mobile
    for i in range(6):  #range of other opponents #player in players
      screen.blit(back[0], (20, 122 + i * SMALL_CARD_HEIGHT))
      screen.blit(back[0], (80, 122 + i * SMALL_CARD_HEIGHT))
      draw_text_box("player 1", WHITE, 13, 140, 122 + i * SMALL_CARD_HEIGHT, 100, 24) #change string with player name  ###
      draw_text_box("", WHITE, 13, 140, 146 + i * SMALL_CARD_HEIGHT, 100, 24)  #two to be replaced with actual variables ###
      draw_text_box("Chips:£50.00", WHITE, 13, 140, 170 + i * SMALL_CARD_HEIGHT, 100, 24)

    #pot
    draw_text_box("Pot: £20.00", WHITE, 15, WIDTH - 160, 122, 140, 30)

    #big cards bottom left
    screen.blit(back[1], (20, HEIGHT - 162))
    screen.blit(back[1], (20 + BIG_CARD_WIDTH, HEIGHT - 162))

    #buttons ADD FUNCTIONS ###      
    draw_text_box("Chips: £20.50", WHITE, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 255, 140, 30)
    draw_button("All In", BLACK, 20, HEIGHT - 205, 60, 30, blank)
    draw_button("Fold", BLACK, 20 + 80 + 80, HEIGHT - 205, 60, 30, blank)

    draw_button("Clear Bet", BLACK, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, blank)
    draw_button("- 50p", BLACK, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, blank)
    draw_button("+ 50p", BLACK, WIDTH - 80, HEIGHT - 105, 60, 30, blank)
    draw_button("Confirm Raise", BLACK, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, blank)

    def fold_check_bet():
      draw_text_box("Bet: £0.50", WHITE, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
      draw_button("Check", BLACK, 20 + 80, HEIGHT - 205, 60, 30, blank)
      #show bet amount, minimum value £0.50 to prevent raising nothing
  
    def fold_call_bet():
      draw_text_box("Bet: £10.00", WHITE, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
      draw_button("Call", BLACK, 20 + 80, HEIGHT - 205, 60, 30, blank)
      
    def fold_all_in():
      draw_text_box("Bet: £50", WHITE, 15, 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 140, 30)
      #draw over in black to eliminate white
      draw_text_box("", BLACK, 15, 20 + 80, HEIGHT - 205, 60, 30)
      draw_text_box("", BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30)
      draw_text_box("", BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30)
      draw_text_box("", BLACK, 15, WIDTH - 80, HEIGHT - 105, 60, 30)
      draw_text_box("", BLACK, 15, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30)
      #grey out with buttons that do nothing
      draw_button("Call", DARK_GREY, 20 + 80, HEIGHT - 205, 60, 30, blank)
      draw_button("Clear Bet", DARK_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 140, 30, blank)
      draw_button("- 50p", DARK_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, blank)
      draw_button("+ 50p", DARK_GREY, WIDTH - 80, HEIGHT - 105, 60, 30, blank)
      draw_button("Confirm Raise", DARK_GREY, 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 140, 30, blank)

    def show_winners():
      draw_text_box("Winning combination", WHITE, 11, WIDTH - 160, 490, 140, 24)
      draw_text_box("Three of a kind", WHITE, 15, WIDTH - 160, 514, 140, 24)#
      draw_text_box("6 high", WHITE, 15, WIDTH - 160, 538, 140, 24)# 

      draw_text_box("Winner(s)", WHITE, 11, WIDTH - 160, 214, 140, 24)
      for i in range(7):
        draw_text_box("player_1", WHITE, 11, WIDTH - 160, 238 + i * 24, 140, 24)


    fold_all_in()
    show_winners()
    #update display
    pygame.display.flip()

draw_game()


'''
# Function to draw cards
def draw_cards(cards, x, y):
  for i, card in enumerate(cards):
      screen.blit(card_images[card - 1], (x + i * CARD_WIDTH, y))
'''