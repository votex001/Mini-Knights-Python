import pygame
import level_loader
from player import Player
from phisics import Physics
from menus.pause import create_pause, run_pause
from camera import Camera

def init_game(map_width,map_height,first_level,player_folder,imgs_map):
    
    camera_surface = pygame.Surface((map_width, map_height))
    level = level_loader.SelectLevel(first_level, camera_surface)
    physics = Physics(level)
    player = Player(player_folder,imgs_map, level.get_spawn(), physics, camera_surface)
    return level, physics, player, camera_surface

def run_game(level, physics, player, camera_surface, screen,zoom):
    clock = pygame.time.Clock()
    running = True # main game loop
    paused = False # pause state
    go_to_menu = True # flag to return to menu
    pause_menu = None #enable pause menu
    camera = Camera(camera_surface,player,screen,zoom)
    def start_game():
        nonlocal paused
        paused = False # resume game
    def quit_game():
        nonlocal go_to_menu, running
        go_to_menu = False #return false to exit the game
        running = False #exit running loop
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #create pause menu every time escape is pressed
                    pause_menu = create_pause(screen, start_game, quit_game)
                    paused = not paused # toggle pause state

        screen.fill((0, 0, 0))  # clear the screen
        scaled_surface,pos=camera.prepare_scaled_surface()
        
        screen.blit(scaled_surface,pos)
        # pause logic
        if not paused:
            pause_menu = None #clear pause state
            # draw the level
            level.draw()
            # update the players movement
            player.handle_input(events)
        else:
            player.reset_moves()  # Reset movement flags
            run_pause(screen, pause_menu) # run the pause menu
            
        # collision detection for debugging
        # physics.draw_walkable_tiles(camera_surface)

        pygame.display.update()
        clock.tick(60)
    return go_to_menu

