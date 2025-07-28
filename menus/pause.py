import pygame_menu
import pygame

def create_pause(screen, start_game, quit_game):
    menu = pygame_menu.Menu('Pause Menu', screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_BLUE)
    def resume_game():
        start_game() # function to resume the game
        menu.disable() # Disable the menu to resume the game
    def go_to_menu():
        quit_game() # function to go back to the main menu
        menu.disable()
        #btns
    menu.add.button('Continue Game', resume_game)
    menu.add.button('Go to menu', go_to_menu)
    return menu 

def run_pause(screen, menu):
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # Update the menu with events
        menu.update(events)
        # If the menu is not enabled, break the loop before drawing
        if not menu.is_enabled():
            break
        #clear the screen
        screen.fill((0, 0, 0))
        menu.draw(screen)
        pygame.display.update()