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

small_font = pygame.font.SysFont("courier", 15)


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
def draw_button(text, x, y, width, height, colour, action):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()
  hover_colour = GREY
  #check if hover
  if x + width > mouse[0] > x and y + height > mouse[1] > y:
    pygame.draw.rect(screen, hover_colour, (x, y, width, height))
    if click[0] == 1:
      action()
  else:
    pygame.draw.rect(screen, colour, (x, y, width, height))

  #white border
  border_width = 1
  pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), border_width)

  #add text
  text_surface = small_font.render(text, True, WHITE)
  text_rect = text_surface.get_rect()
  #add text to centre
  text_rect.center = ((x + (width // 2)), (y + (height // 2)))
  screen.blit(text_surface, text_rect)


def draw_text_box(text, x, y, width, height):
  box_colour = WHITE
  text_colour = BLACK

  pygame.draw.rect(screen, box_colour, (x, y, width, height))
  text_surface = small_font.render(text, True, text_colour)
  text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
  screen.blit(text_surface, text_rect)



def out():
  print("out")



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
    for i in range(6):
      screen.blit(back[0], (20 , 112 + i * SMALL_CARD_HEIGHT))
      screen.blit(back[0], (90 , 112 + i * SMALL_CARD_HEIGHT))
    
    #big cards bottom left
    screen.blit(back[1], (20, HEIGHT - 162))
    screen.blit(back[1], (20 + BIG_CARD_WIDTH, HEIGHT - 162))

    
    # Draw cards on the table
    #draw_cards(cards_on_table, 50, 250)

    # Draw player's hand
    #draw_cards(player_hand, 50, 450)

    #buttons ADD FUNCTIONS ###
    draw_button("All In", 20, HEIGHT - 205, 60, 30, BLACK, out)
    draw_button("Check", 20 + 80, HEIGHT - 205, 60, 30, BLACK, out)
    draw_button("Fold", 20 + 80 + 80, HEIGHT - 205, 60, 30, BLACK, out)

    draw_button("Clear", 15 + BIG_CARD_WIDTH*2 , HEIGHT - 55, 60, 30, BLACK, out)
    draw_button("- 50p", 15 + BIG_CARD_WIDTH*2 , HEIGHT - 105, 60, 30, BLACK, out)
    draw_button("+ 50p", 15 + BIG_CARD_WIDTH*2 , HEIGHT - 155, 60, 30, BLACK, out)
    draw_button("Fold", WIDTH - 80, HEIGHT - 55, 60, 30, BLACK, out)
    draw_button("Check", WIDTH - 80, HEIGHT - 105, 60, 30, BLACK, out)
    draw_button("All In", WIDTH - 80, HEIGHT - 155, 60, 30, BLACK, out)
    

    #show bet amount, minimum value £0.50 to prevent raising nothing
    draw_text_box("£20.50", 15 + BIG_CARD_WIDTH*2, HEIGHT - 205, 60, 30)
  
    #instead of sliders add more buttons to raise pot by (chip values just like a real table)

    #draw_button("Fold", 10 + BIG_CARD_WIDTH*2 , HEIGHT - 80, 60, 30, BLACK, out)
    #draw_button("Call", 10 + BIG_CARD_WIDTH*2 , HEIGHT - 140, 60, 30, BLACK, out)
    #draw_button("Raise", WIDTH - 80, HEIGHT - 200, 60, 30, BLACK, out)

    #draw_button("Fold", 10 + BIG_CARD_WIDTH*2 , HEIGHT - 80, 60, 30, BLACK, out)
    #draw_button("All In", 10 + BIG_CARD_WIDTH*2 , HEIGHT - 140, 60, 30, BLACK, out)


    #update display
    pygame.display.flip()

draw_game()


'''
# Function to draw cards
def draw_cards(cards, x, y):
  for i, card in enumerate(cards):
      screen.blit(card_images[card - 1], (x + i * CARD_WIDTH, y))
'''