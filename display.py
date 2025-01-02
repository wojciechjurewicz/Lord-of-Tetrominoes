import sys

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

        display_info = pygame.display.Info()
        self.user_width = display_info.current_w
        self.user_height = display_info.current_h

        # Setting up the screen
        self.screen = pygame.display.set_mode((self.user_width, self.user_height), pygame.FULLSCREEN)
        self.dummy_screen = pygame.Surface((self.window_width, self.window_height))
        pygame.display.set_caption('Lord of Tetrominoes')
        self.font = pygame.font.SysFont('Go', 24)

        # Assets loading
        start_background_path = config['Assets']['StartBackground']
        game_background_path = config['Assets']['GameBackground']
        gameover_background_path = config['Assets']['GameOverBackground']
        block_path = config['Assets']['Block']
        empty_block_path = config['Assets']['EmptyBlock']

        self.start_background = pygame.image.load(start_background_path).convert()
        self.start_background = pygame.transform.scale(self.start_background, (1920, 1080))
        self.game_background = pygame.image.load(game_background_path).convert()
        self.game_background = pygame.transform.scale(self.game_background, (1920, 1080))
        self.gameover_background = pygame.image.load(gameover_background_path).convert()
        self.gameover_background = pygame.transform.scale(self.gameover_background, (1920, 1080))
        self.block_texture = pygame.image.load(block_path).convert_alpha()
        self.block_texture = pygame.transform.scale(self.block_texture, (40, 40))
        self.empty_block_texture = pygame.image.load(empty_block_path).convert_alpha()
        self.empty_block_texture = pygame.transform.scale(self.empty_block_texture, (40, 40))

        self.dummy_screen = pygame.transform.scale(self.dummy_screen, (self.user_width, self.user_height))

        self.play_button = None
        self.quit_button = None
        self.music_button = None

    def draw_text(self, x, y, string, surface, size, color, font):
        font = pygame.font.SysFont(font, size)
        text = font.render(string, True, color)
        textbox = text.get_rect()
        textbox.center = (x, y)
        surface.blit(text, textbox)

    def update(self, scene_id, game=None, scores=None):
        self.dummy_screen = pygame.Surface((self.window_width, self.window_height))
        # Draw starting screen
        if scene_id == 0:
            action = self.draw_start_screen()
        # Draw playing screen
        elif scene_id == 1:
            self.draw_playing_grid(game.get_board_with_tetromino(game.board), game.ghost_piece())
            self.draw_score(game.score, game.level, game.lines)
            self.draw_queue_hold(game.pieces_queue, game.piece_on_hold)
        # Draw game over screen
        elif scene_id == 2:
            self.draw_game_over_screen(game.score, scores)

        self.draw_quit_button()
        self.draw_music_button()
        # Update the display
        self.dummy_screen = pygame.transform.scale(self.dummy_screen, (self.user_width, self.user_height))
        self.screen.blit(self.dummy_screen, (0, 0))
        pygame.display.flip()
        self.dummy_screen.fill('black')

    def draw_quit_button(self):
        # Button properties
        button_color = pygame.Color('red')
        hover_color = pygame.Color('#8b0000')
        outline_color = pygame.Color('black')
        text_color = pygame.Color('white')
        button_rect = pygame.Rect(self.window_width - 50, 10, 40, 40)
        scaled_button_rect = pygame.Rect((self.window_width - 50)*(self.user_width/self.window_width), (10)*(self.user_height/self.window_height), 40, 40)
        # Check if button is hovered
        mouse_pos = pygame.mouse.get_pos()
        if scaled_button_rect.collidepoint(mouse_pos):
            current_button_color = hover_color
        else:
            current_button_color = button_color

        # Outline
        pygame.draw.rect(self.dummy_screen, outline_color, button_rect.inflate(4, 4), border_radius=5)

        # Draw the button
        pygame.draw.rect(self.dummy_screen, current_button_color, button_rect, border_radius=5)
        self.draw_text(button_rect.centerx, button_rect.centery, "X", self.dummy_screen, 24, text_color, 'Arial')

        # Clicking the button
        self.quit_button = scaled_button_rect

    def draw_music_button(self):
        # Button properties
        button_color = pygame.Color('blue')
        hover_color = pygame.Color('dark blue')
        outline_color = pygame.Color('black')
        text_color = pygame.Color('white')
        button_rect = pygame.Rect(self.window_width - 100, 10, 40, 40)
        scaled_button_rect = pygame.Rect((self.window_width - 100) * (self.user_width / self.window_width),
                                         (10) * (self.user_height / self.window_height), 40, 40)

        # Check if button is hovered
        mouse_pos = pygame.mouse.get_pos()
        if scaled_button_rect.collidepoint(mouse_pos):
            current_button_color = hover_color
        else:
            current_button_color = button_color

        # Outline
        pygame.draw.rect(self.dummy_screen, outline_color, button_rect.inflate(4, 4), border_radius=5)

        # Draw the button
        pygame.draw.rect(self.dummy_screen, current_button_color, button_rect, border_radius=5)
        self.draw_text(button_rect.centerx, button_rect.centery, "♪", self.dummy_screen, 24, text_color, 'Arial')

        # Clicking the button
        self.music_button = scaled_button_rect

    def draw_start_screen(self):
        # Draw the start background
        self.dummy_screen.blit(self.start_background, (0, 0))

        # Button properties
        button_color = pygame.Color('#241e2e')
        hover_color = pygame.Color('#1c181f')
        outline_color = pygame.Color('#fcf58e')
        text_color = pygame.Color('white')
        button_rect = pygame.Rect(820, 915, 300, 70)
        scaled_button_rect = pygame.Rect((820) * (self.user_width / self.window_width),
                                         (915) * (self.user_height / self.window_height), (300) * (self.user_width / self.window_width), (70) * (self.user_height / self.window_height))

        # Check if button is hovered
        mouse_pos = pygame.mouse.get_pos()
        if scaled_button_rect.collidepoint(mouse_pos):
            current_button_color = hover_color
        else:
            current_button_color = button_color

        # button outline
        pygame.draw.rect(self.dummy_screen, outline_color, button_rect.inflate(6, 6), border_radius=5)

        #Draw the button with text
        pygame.draw.rect(self.dummy_screen, current_button_color, button_rect, border_radius=5)
        self.draw_text(button_rect.centerx, button_rect.centery, "PLAY", self.dummy_screen, 32, text_color, 'Calibri')

        self.play_button = scaled_button_rect

    def draw_playing_grid(self, board, ghost_piece):
        self.dummy_screen.blit(self.game_background, (0, 0))
        # Initialization of surface - grid for the tetris game
        grid_surface = pygame.Surface((400, 880), pygame.SRCALPHA)
        #grid_surface.blit(self.grid_background, (0, 0))

        # Drawing the playing grid square by square
        for row in range(self.board_height):
            for column in range(self.board_width):
                color = COLORS[int(board[row][column])] # Color according to the shape
                rect = pygame.Rect(column*40, row*40, 39, 39)

                # Get the texture and color it
                if int(board[row][column]) == 0:
                    colored_block = self.empty_block_texture.copy()
                else:
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
        self.dummy_screen.blit(grid_surface, (760, 100))

    def draw_score(self, points, level, lines):
        # Surface for scores
        score_surface = pygame.Surface((380, 280), pygame.SRCALPHA)
        score_surface.fill((0, 0, 0, 170))

        self.draw_text(190, 65, f'SCORE: {points}', score_surface, 40, 'grey', 'Arial')
        self.draw_text(190, 135, f'LEVEL: {level}', score_surface, 40, 'grey', 'Arial')
        self.draw_text(190, 205, f'LINES: {lines}', score_surface, 40, 'grey', 'Arial')

        self.dummy_screen.blit(score_surface, (180, 300))

    def draw_queue_hold(self, queue, hold):
        queue_hold_surface = pygame.Surface((280, 880), pygame.SRCALPHA)
        queue_hold_surface.fill((0, 0, 0, 170))
        self.draw_text(140, 60, 'NEXT', queue_hold_surface, 40, 'grey', 'Arial')
        self.draw_shape_for_queue(queue[0], 140, 140, queue_hold_surface)
        self.draw_shape_for_queue(queue[1], 140, 340, queue_hold_surface)
        self.draw_shape_for_queue(queue[2], 140, 540, queue_hold_surface)
        self.draw_text(140, 650, 'HOLD', queue_hold_surface, 40, 'grey', 'Arial')
        if hold is not None:
            self.draw_shape_for_queue(hold, 140, 740, queue_hold_surface)
        self.dummy_screen.blit(queue_hold_surface, (1480, 100))

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

    def draw_game_over_screen(self, score, scores):
        self.dummy_screen.blit(self.gameover_background, (0, 0))
        leaderboards_surface = pygame.Surface((400, 290), pygame.SRCALPHA)
        self.draw_text(196, 14, 'LEADERBOARDS', leaderboards_surface, 30, 'white', 'Arial')
        self.draw_text(196, 64, f'{scores[0]}', leaderboards_surface, 30, 'gold', 'Arial')
        self.draw_text(196, 114, f'{scores[1]}', leaderboards_surface, 30, pygame.Color((192,192,192)), 'Arial')
        self.draw_text(196, 164, f'{scores[2]}', leaderboards_surface, 30, 'brown', 'Arial')
        self.draw_text(196, 214, 'YOUR SCORE', leaderboards_surface, 30, 'white', 'Arial')
        self.draw_text(196, 264, f'{score}', leaderboards_surface, 30, 'white', 'Arial')

        button_color = pygame.Color('#241e2e')
        hover_color = pygame.Color('#1c181f')
        outline_color = pygame.Color('#fcf58e')
        text_color = pygame.Color('white')
        button_rect = pygame.Rect(1220, 915, 300, 70)
        scaled_button_rect = pygame.Rect((1220) * (self.user_width / self.window_width),
                                         (915) * (self.user_height / self.window_height), (300) * (self.user_width / self.window_width), (70) * (self.user_height / self.window_height))

        mouse_pos = pygame.mouse.get_pos()
        if scaled_button_rect.collidepoint(mouse_pos):
            current_button_color = hover_color
        else:
            current_button_color = button_color
        pygame.draw.rect(self.dummy_screen, outline_color, button_rect.inflate(6, 6), border_radius=5)
        pygame.draw.rect(self.dummy_screen, current_button_color, button_rect, border_radius=5)
        self.draw_text(button_rect.centerx, button_rect.centery, "PLAY AGAIN", self.dummy_screen, 32, text_color, 'Calibri')
        self.play_button = scaled_button_rect

        self.dummy_screen.blit(leaderboards_surface, (778, 680))