# main.py
import pygame
from menu import create_menu, run_menu
from game import init_game, run_game

# Инициализация pygame
pygame.init()

# Настройки
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 480
GAME_NAME = "Mini Knights"
GAME_ICON = "imgs/icon.png"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)
icon = pygame.image.load(GAME_ICON)
pygame.display.set_icon(icon)

# Логика меню
def start_game():
    global in_game
    in_game = True  # Игровой процесс

def quit_game():
    global running
    running = False  # Завершаем главный цикл

# Создание меню
menu = create_menu(screen, start_game, quit_game)

# Главный цикл
running = True
in_game = False
while running:
    if in_game:
        # Инициализация игры
        level, physics, player, camera_surface = init_game(screen)

        # Запуск игрового цикла
        in_game = run_game(level, physics, player, camera_surface, screen)
    else:
        # Запуск меню
        run_menu(screen, menu)

pygame.quit()  # Корректное завершение игры
