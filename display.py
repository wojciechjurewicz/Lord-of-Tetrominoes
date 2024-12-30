import pygame
import configparser
from tetrominos import tetrominos_queue_display as queue_shapes
from assets.colors import COLORS

class Display:
    def __init__(self):
        # Loading window and board settings
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.window_width = int(config['WindowSettings']['Width'])
        self.window_height = int(config['WindowSettings']['Height'])
        self.board_width = int(config['BoardSettings']['Width'])
        self.board_height = int(config['BoardSettings']['Height'])

        # Setting up the screen
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
        pygame.display.set_caption('Lord of Tetrominoes')
        self.font = pygame.font.SysFont('Go', 24)

        # Assets loading
        grid_background_path = config['Assets']['GridBackground']
        block_path = config['Assets']['Block']

        self.grid_background = pygame.image.load(grid_background_path).convert()
        self.grid_background = pygame.transform.scale(self.grid_background, (400, 880))
        self.block_texture = pygame.image.load(block_path).convert_alpha()
        self.block_texture = pygame.transform.scale(self.block_texture, (40, 40))

    def draw_text(self, x, y, string, surface, size, color, font):
        font = pygame.font.SysFont(font, size)
        text = font.render(string, True, color)
        textbox = text.get_rect()
        textbox.center = (x, y)
        surface.blit(text, textbox)

    def update(self, scene_id, game=None):
        # Draw starting screen
        if scene_id == 0:
            self.draw_start_screen()
        # Draw playing screen
        elif scene_id == 1:
            self.draw_playing_grid(game.get_board_with_tetromino(game.board), game.ghost_piece())
            self.draw_score(game.score, game.level, game.lines)
            self.draw_queue_hold(game.pieces_queue, game.piece_on_hold)
            self.pause_button()
            self.music_buttion()
        # Draw game over screen
        elif scene_id == 2:
            self.draw_game_over_screen()

        # Update the display
        pygame.display.flip()
        self.screen.fill('black')

    def draw_start_screen(self):
        title_surface = pygame.Surface((1000, 300))
        title_surface.fill('brown')
        self.screen.blit(title_surface, (460, 100))

    def draw_playing_grid(self, board, ghost_piece):
        # Initialization of surface - grid for the tetris game
        grid_surface = pygame.Surface((400, 880))
        grid_surface.blit(self.grid_background, (0, 0))

        # Drawing the playing grid square by square
        for row in range(self.board_height):
            for column in range(self.board_width):
                color = COLORS[int(board[row][column])] # Color according to the shape
                rect = pygame.Rect(column*40, row*40, 39, 39)

                # Get the texture and color it
                colored_block = self.block_texture.copy()
                colored_block.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

                grid_surface.blit(colored_block, rect.topleft) # Place it on the surface

        # Draw the ghost pieces on board fields with value 0
        for y, x in ghost_piece:
            if board[y][x] == 0:
                color = pygame.Color(255, 255, 255, 120) # White ghsot piece
                rect = pygame.Rect(x * 40, y * 40, 39, 39)

                # Get the texture and color it
                colored_block = self.block_texture.copy()
                colored_block.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

                grid_surface.blit(colored_block, rect.topleft) # Place it on the surface

        # Show the grid surface on the screen
        self.screen.blit(grid_surface, (760, 100))

    def draw_score(self, points, level, lines):
        # Surface for scores
        score_surface = pygame.Surface((280, 280))
        score_surface.fill('brown')

        self.draw_text(140, 65, f'SCORE: {points}', score_surface, 40, 'black', 'Arial')
        self.draw_text(140, 135, f'LEVEL: {level}', score_surface, 40, 'black', 'Arial')
        self.draw_text(140, 205, f'LINES: {lines}', score_surface, 40, 'black', 'Arial')

        self.screen.blit(score_surface, (240, 300))

    def draw_queue_hold(self, queue, hold):
        queue_hold_surface = pygame.Surface((280, 880))
        queue_hold_surface.fill('brown')
        self.draw_text(140, 60, 'NEXT', queue_hold_surface, 40, 'black', 'Arial')
        self.draw_shape_for_queue(queue[0], 140, 140, queue_hold_surface)
        self.draw_shape_for_queue(queue[1], 140, 340, queue_hold_surface)
        self.draw_shape_for_queue(queue[2], 140, 540, queue_hold_surface)
        self.draw_text(140, 650, 'HOLD', queue_hold_surface, 40, 'black', 'Arial')
        if hold is not None:
            self.draw_shape_for_queue(hold, 140, 740, queue_hold_surface)
        self.screen.blit(queue_hold_surface, (1480, 100))

    def draw_shape_for_queue(self, shape, x, y, surface):
        height, width = queue_shapes[shape].shape
        shape_surface = pygame.Surface((width*40, height*40), pygame.SRCALPHA)

        for row in range(height):
            for column in range(width):
                if int(queue_shapes[shape][row][column]) != 0:
                    color = COLORS[int(queue_shapes[shape][row][column])]
                    rect = pygame.Rect(column * 40, row * 40, 39, 39)

                    colored_block = self.block_texture.copy()
                    colored_block.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

                    shape_surface.blit(colored_block, rect.topleft)

        shapebox = shape_surface.get_rect()
        shapebox.center = (x, y)
        surface.blit(shape_surface, shapebox)

    def pause_button(self):
        pass

    def music_buttion(self):
        pass

    def draw_game_over_screen(self):
        pass