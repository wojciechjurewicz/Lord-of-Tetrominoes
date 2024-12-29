import numpy as np
import random
from tetrominos import tetrominos as tetrominos_shapes


class Tetromino():
    # Creating specified piece at the top of the middle of the screen with rotation 0
    def __init__(self, shape):
        self.rotation = 0
        self.shape_name = shape
        self.shape = tetrominos_shapes[self.shape_name][self.rotation]
        self.x = (board_width - len(self.shape)) // 2
        self.y = 0
        self.next_rotation_shape = tetrominos_shapes[self.shape_name][(self.rotation + 1) % 4]

    # Rotating the piece based on the pre-generated rotations.
    # X, Y position doesn't change thanks to implementation of so-called Super Rotation System
    # (official Tetris way for pieces to behave).
    def rotate(self):
        self.rotation += 1
        self.rotation = self.rotation % 4
        self.shape = tetrominos_shapes[self.shape_name][self.rotation]
        self.next_rotation_shape = tetrominos_shapes[self.shape_name][(self.rotation + 1) % 4]

    # Moving the piece in specified direction
    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Game():
    # Game initialization
    def __init__(self, width, height):
        global board_width
        board_width = width
        # Generating empty board
        self.board = np.zeros((height, width), dtype=int)

        # Initial score set to 0
        self.score = 0
        self.game_over = False

        # Initialization of queue of pieces and generating first piece to play
        self.pieces_queue = []
        self.new_piece()

    # Function taking next piece from the queue and maintaining constant number of 3 pieces in the queue
    def new_piece(self):
        # We are making the queue of length 4 as we are taking a piece from it right away.
        while len(self.pieces_queue) != 4:
            self.pieces_queue.append(random.choice(list(tetrominos_shapes.keys())))
        self.current_tetromino = Tetromino(self.pieces_queue.pop())

    # Function moving the piece in given direction (y increases downwards)
    def move(self, dx, dy):
        if not self.collision_move(dx, dy):
            self.current_tetromino.x += dx
            self.current_tetromino.y += dy

    # Function rotating the current piece clockwise
    def rotate(self):
        if not self.collision_rotation():
            self.current_tetromino.rotate()

    # Function checking whether there will occur a collision while moving horizontally or vertically.
    # It compares the number of non-zero elements in a state before the move and after the move.
    def collision_move(self, dx, dy):
        try:
            if np.count_nonzero(self.board[
                                self.current_tetromino.y:self.current_tetromino.y + self.current_tetromino.shape.shape[
                                    0],
                                self.current_tetromino.x:self.current_tetromino.x + self.current_tetromino.shape.shape[
                                    1]] + self.current_tetromino.shape) == np.count_nonzero(self.board[
                                                                                            self.current_tetromino.y + dy:self.current_tetromino.y +
                                                                                                                          self.current_tetromino.shape.shape[
                                                                                                                              0] + dy,
                                                                                            self.current_tetromino.x + dx:self.current_tetromino.x +
                                                                                                                          self.current_tetromino.shape.shape[
                                                                                                                              1] + dx] + self.current_tetromino.shape):
                return False
        except ValueError:
            pass
        return True

    def collision_move(self, dx, dy):
        new_x = self.current_tetromino.x + dx
        new_y = self.current_tetromino.y + dy

        for i, row in enumerate(self.current_tetromino.shape):
            for j, value in enumerate(row):
                if value != 0:
                    chunk_x = new_x + j
                    chunk_y = new_y + i
                    if chunk_x < 0 or chunk_x >= board_width or chunk_y >= len(self.board) or chunk_y < 0:
                        return True
                    if self.board[chunk_y][chunk_x] != 0:
                        return True
        return False


    # Function checking whether there will be a collision while rotating.
    # It works similarly to the checking collision on move, it compares number of non-zero elements
    def collision_rotation(self):
        try:
            if np.count_nonzero(self.board[
                                self.current_tetromino.y:self.current_tetromino.y + self.current_tetromino.shape.shape[
                                    0],
                                self.current_tetromino.x:self.current_tetromino.x + self.current_tetromino.shape.shape[
                                    1]] + self.current_tetromino.shape) == np.count_nonzero(self.board[
                                                                                            self.current_tetromino.y:self.current_tetromino.y +
                                                                                                                     self.current_tetromino.next_rotation_shape.shape[
                                                                                                                         0],
                                                                                            self.current_tetromino.x:self.current_tetromino.x +
                                                                                                                     self.current_tetromino.next_rotation_shape.shape[
                                                                                                                         1]] + self.current_tetromino.next_rotation_shape):
                return False
        except ValueError:
            pass
        return True

    # Function responsible for placing a piece. It adds the current tetromino to the board matrix and generates a new one
    def place(self):
        self.board[self.current_tetromino.y:self.current_tetromino.y + self.current_tetromino.shape.shape[0],
        self.current_tetromino.x:self.current_tetromino.x + self.current_tetromino.shape.shape[
            1]] += self.current_tetromino.shape
        self.new_piece()

    # Function returning the board along with current tetromino. Used for display purpouses.
    def get_game_board(self):
        board_snapshot = self.board.copy()
        board_snapshot[self.current_tetromino.y:self.current_tetromino.y + self.current_tetromino.shape.shape[0],
        self.current_tetromino.x:self.current_tetromino.x + self.current_tetromino.shape.shape[
            1]] += self.current_tetromino.shape
        return board_snapshot
