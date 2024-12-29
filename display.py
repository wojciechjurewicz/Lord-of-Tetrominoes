import pygame

# Colors for each tetromino and background.
# Each tetromino has in its matrix numbers from below which are then translated into colors.
COLORS = {1: 'turquoise1',
          2: 'coral',
          3: 'MediumOrchid4',
          4: 'OliveDrab1',
          5: 'cornflower blue',
          6: 'SeaGreen1',
          7: 'maroon',
          0: 'grey'}

class Display:
    def __init__(self, screen, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height
        self.font = pygame.font.SysFont('Arial', 24)
        self.screen = screen

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
        # Drawing the playing grid square by square
        for row in range(self.board_height):
            for column in range(self.board_width):
                color = COLORS[int(board[row][column])]
                rect = pygame.Rect(column*30, row*30, 29, 29)
                pygame.draw.rect(self.screen, color, rect)

        # Draw the ghost pieces on board fields with value 0
        for y, x in ghost_piece:
            if board[y][x] == 0:
                rect = pygame.Rect(x * 30, y * 30, 29, 29)
                pygame.draw.rect(self.screen, 'pink', rect)

    def draw_game_over_screen(self):
        pass