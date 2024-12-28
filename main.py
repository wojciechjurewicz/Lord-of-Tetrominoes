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

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Lord of Tetrominoes')

game = Game(board_width, board_height)
display = Display(screen, board_width, board_height)

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                game.move(0, 1)
            elif event.key == pygame.K_RIGHT:
                game.move(1, 0)
            elif event.key == pygame.K_LEFT:
                game.move(-1, 0)
            elif event.key == pygame.K_UP:
                game.rotate()

def main():
    clock = pygame.time.Clock()
    while True:
        handle_input()
        display.update(game)
        clock.tick(30)

if __name__ == '__main__':
    main()