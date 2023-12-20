import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 414, 896 #logical point resolution of iphone 11
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CARD_WIDTH, CARD_HEIGHT = 75, 100

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Poker Interface")

# Load card images
card_images = []  # https://code.google.com/archive/p/vector-playing-cards/
for suit in ["hearts", "diamonds", "spades", "clubs"]:
  for value in range(2, 15):
      card_images.append(pygame.image.load(f"cards/{suit}.{value}.png"))

# Function to draw cards
def draw_cards(cards, x, y):
  for i, card in enumerate(cards):
      screen.blit(card_images[card - 1], (x + i * CARD_WIDTH, y))

# Function to draw buttons
def draw_button(text, x, y, width, height, color, hover_color, action):
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()

  if x + width > mouse[0] > x and y + height > mouse[1] > y:
    pygame.draw.rect(screen, hover_color, (x, y, width, height))
    if click[0] == 1:
      action()
    else:
      pygame.draw.rect(screen, color, (x, y, width, height))

    small_text = pygame.font.SysFont("comicsansms", 20)
    text_surface, text_rect = text_objects(text, small_text)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surface, text_rect)

# Function to create text objects
def text_objects(text, font):
  text_surface = font.render(text, True, WHITE)
  return text_surface, text_surface.get_rect()

# Main game loop
def game_loop():
  cards_on_table = [random.randint(1, 52) for _ in range(5)]
  player_hand = [random.randint(1, 52) for _ in range(2)]

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    screen.fill(BLACK)

    # Draw cards on the table
    draw_cards(cards_on_table, 50, 250)

    # Draw player's hand
    draw_cards(player_hand, 50, 450)

    # Draw buttons
    draw_button("Fold", 200, 500, 100, 50, RED, (255, 0, 0), game_loop)
    draw_button("Call", 350, 500, 100, 50, RED, (255, 0, 0), game_loop)
    draw_button("Raise", 500, 500, 100, 50, RED, (255, 0, 0), game_loop)

    pygame.display.flip()

game_loop()