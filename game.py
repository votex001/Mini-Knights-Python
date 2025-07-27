# game.py
import pygame
import level_loader
from player import Player
from phisics import Physics

def init_game(screen):
    camera_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    level = level_loader.SelectLevel("SelectLevel/maps/lvl1.tmx", camera_surface)
    physics = Physics(level)
    player = Player("character/Soldier.png", level.get_spawn(), physics, camera_surface)
    return level, physics, player, camera_surface

def run_game(level, physics, player, camera_surface, screen):
    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Возвращаемся в меню

        # Игровая логика
        level.draw()
        player.handle_input(events)
        
        # collision detection for debugging
        # physics.draw_walkable_tiles(camera_surface)

        screen.fill((0, 0, 0))  # Очистка экрана
        screen.blit(camera_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)
    
    return True

