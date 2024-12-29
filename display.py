import pygame
import configparser
from assets.colors import COLORS

# Colors for each tetromino and background.
# Each tetromino has in its matrix numbers from below which are then translated into colors.


class Display:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.window_width = int(config['WindowSettings']['Width'])
        self.window_height = int(config['WindowSettings']['Height'])
        self.board_width = int(config['BoardSettings']['Width'])
        self.board_height = int(config['BoardSettings']['Height'])
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
        pygame.display.set_caption('Lord of Tetrominoes')
        self.board_width = self.board_width
        self.board_height = self.board_height
        self.font = pygame.font.SysFont('Arial', 24)
        self.screen = self.screen
        colorspath = config['Assets']['ColorMap']

        grid_background_path = config['Assets']['GridBackground']

        self.grid_background = pygame.image.load(grid_background_path).convert()
        self.grid_background = pygame.transform.scale(self.grid_background, (400, 880))

        block_path = config['Assets']['Block']

        self.block_texture = pygame.image.load(block_path).convert_alpha()
        self.block_texture = pygame.transform.scale(self.block_texture, (40, 40))


    def update(self, scene_id, game=None):
        if scene_id == 0:
            self.draw_start_screen()
        elif scene_id == 1:
            # Draw the board, tetromino and ghost piece
            self.draw_game_screen(game.get_board_with_tetromino(game.board), game.ghost_piece())
        elif scene_id == 2:
            self.draw_game_over_screen()

        # Update the display
        pygame.display.flip()
        self.screen.fill('black')

    def draw_start_screen(self):
        pass

    def draw_game_screen(self, board, ghost_piece):

        grid_surface = pygame.Surface((400, 880))
        grid_surface.blit(self.grid_background, (0, 0))

        # Drawing the playing grid square by square
        for row in range(self.board_height):
            for column in range(self.board_width):
                color = COLORS[int(board[row][column])]
                rect = pygame.Rect(column*40, row*40, 39, 39)

                colored_block = self.block_texture.copy()
                colored_block.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
                grid_surface.blit(colored_block, rect.topleft)

        # Draw the ghost pieces on board fields with value 0
        for y, x in ghost_piece:
            if board[y][x] == 0:
                color = pygame.Color(255, 255, 255, 120)
                rect = pygame.Rect(x * 40, y * 40, 39, 39)
                colored_block = self.block_texture.copy()
                colored_block.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
                grid_surface.blit(colored_block, rect.topleft)

        self.screen.blit(grid_surface, (760, 100))

    def draw_game_over_screen(self):
        pass