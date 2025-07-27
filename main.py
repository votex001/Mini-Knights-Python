import pygame
import level_loader
from player import Player
from phisics import Physics
pygame.init()

# fps
clock = pygame.time.Clock()

#  Settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 480
GAME_NAME = "Mini Knights"
GAME_ICON = "imgs/icon.png"


# camera
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
camera_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
level = level_loader.SelectLevel("SelectLevel/maps/lvl1.tmx",camera_surface)

# game name and icon
pygame.display.set_caption(GAME_NAME)
icon = pygame.image.load(GAME_ICON)
pygame.display.set_icon(icon)

# move physics
physics = Physics(level)
# player
player = Player("character/Soldier.png",level.get_spawn(),physics,camera_surface)



play = True

while play:
# exit settings
    events =pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            play = False




    level.draw()
    player.handle_input(events)
    screen.blit(camera_surface, (0, 0))
    pygame.display.update()
    clock.tick(60)

    # Draw walkable tiles for debugging purposes
    # physics.draw_walkable_tiles(camera_surface)
pygame.quit()