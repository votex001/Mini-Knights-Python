# main.py
import pygame
from menus.menu import create_menu, run_menu
from game import init_game, run_game
from settings import *

pygame.init()

# setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)
icon = pygame.image.load(GAME_ICON)
pygame.display.set_icon(icon)

# game button functions
def start_game():
    global in_game
    in_game = True  # start the game

def quit_game():
    global running
    running = False  #stop main game loop

# initialize menu
menu = create_menu(screen, start_game, quit_game)

# main loop
running = True # main game loop
in_game = False # game state
# router
while running:
    if in_game:
        # game init
        level, physics, player, camera_surface = init_game(MAP_WIDTH,MAP_HEIGHT,FIRST_LVL,CHARACTER_FOLDER,IMGS_MAP)

        #  start game
        in_game = run_game(level, physics, player, camera_surface, screen,ZOOM)
    else:
        # menu loop
        run_menu(screen, menu)

pygame.quit() 
