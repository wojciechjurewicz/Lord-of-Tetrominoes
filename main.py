import sys
import pygame
from game import Game
from display import Display
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
window_width = int(config['WindowSettings']['Width'])
window_height = int(config['WindowSettings']['Height'])
board_width = int(config['BoardSettings']['Width'])
board_height = int(config['BoardSettings']['Height']) + int(config['BoardSettings']['SafeZoneHeight'])
automove_interval = int(config['GameSettings']['AutoMoveInterval'])

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Lord of Tetrominoes')

game = Game(board_width, board_height)
display = Display(screen, board_width, board_height)

def handle_input(last_move_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                game.move(0, 1)
                last_move_time = pygame.time.get_ticks()
            elif event.key == pygame.K_RIGHT:
                game.move(1, 0)
            elif event.key == pygame.K_LEFT:
                game.move(-1, 0)
            elif event.key == pygame.K_UP:
                game.rotate()
            elif event.key == pygame.K_SPACE:
                game.hard_drop()
                last_move_time = pygame.time.get_ticks()
    return last_move_time

def main():
    clock = pygame.time.Clock()
    last_move_time = pygame.time.get_ticks()
    while True:
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time >= automove_interval:
            game.move(0, 1)
            last_move_time = pygame.time.get_ticks()
        last_move_time = handle_input(last_move_time)
        display.update(game)
        clock.tick(30)

if __name__ == '__main__':
    main()