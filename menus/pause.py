import pygame_menu
import pygame
import pygame_menu.themes
# theme to customize
custom_theme = pygame_menu.themes.THEME_BLUE.copy()

custom_theme.set_background_color_opacity(0) # disable bg to see game on pause

# buttons
custom_theme.widget_margin = (0,20)

def create_pause(screen, start_game, quit_game):
    menu = pygame_menu.Menu('Pause Menu', screen.get_width(), screen.get_height(), theme=custom_theme)
    def resume_game():
        start_game() # function to resume the game
        menu.disable() # Disable the menu to resume the game
    def go_to_menu():
        quit_game() # function to go back to the main menu
        menu.disable()
        #btns
    menu.add.button('Continue Game', resume_game,button_id = "btn_continue")
    menu.add.button('Go to menu', go_to_menu,button_id = "btn_quit")
    
    return menu 

def run_pause(screen, menu):
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu.get_widget('btn_continue').apply()
        
                
        # If the menu is not enabled, break the loop before drawing
        if not menu.is_enabled():
            break
        # Update the menu with events
        menu.update(events)
      
        if menu.is_enabled():
            menu.draw(screen)
            btn_continue = menu.get_widget('btn_continue')
            btn_quit = menu.get_widget('btn_quit')

            # Hover color
            if btn_continue.get_rect().collidepoint(pygame.mouse.get_pos()):
                btn_continue.set_background_color((100, 100, 255))
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                btn_continue.set_background_color((229, 229, 229)) 
            if btn_quit.get_rect().collidepoint(pygame.mouse.get_pos()):
                btn_quit.set_background_color((100, 100, 255))
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # Default color
            else:
                btn_quit.set_background_color((229, 229, 229))  










        pygame.display.update()