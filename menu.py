# menu.py
import pygame_menu
import pygame

def create_menu(screen, start_game, quit_game):
    menu = pygame_menu.Menu('Welcome', screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('Play', start_game)
    menu.add.button('Quit', quit_game)
    return menu

def run_menu(screen, menu):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    menu.update(events)
    menu.draw(screen)
    pygame.display.update()
