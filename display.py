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
        self.screen = screen

    def update(self, game):
        self.draw(game.get_board_with_tetromino(game.board), game.ghost_piece())

        # Updating the display
        pygame.display.flip()

    # Drawing the playing grid square by square
    def draw(self, board, ghost_piece):
        for row in range(self.board_height):
            for column in range(self.board_width):
                color = COLORS[int(board[row][column])]
                rect = pygame.Rect(column*30, row*30, 29, 29)
                pygame.draw.rect(self.screen, color, rect)

        for y, x in ghost_piece:
            if board[y][x] == 0:
                rect = pygame.Rect(x * 30, y * 30, 29, 29)
                pygame.draw.rect(self.screen, 'pink', rect)