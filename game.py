import sys

import numpy as np
import random

import pygame

from tetrominos import tetrominos as tetrominos_shapes
from tetrominos import jlstz_kicks, i_kicks


class Tetromino():
    # Creating specified piece at the top of the middle of the screen with rotation 0
    def __init__(self, shape, hold=False):
        self.rotation = 0
        self.shape_name = shape
        self.shape = tetrominos_shapes[self.shape_name][self.rotation]
        self.x = (board_width - len(self.shape)) // 2
        self.y = 0
        self.next_rotation_shape = tetrominos_shapes[self.shape_name][(self.rotation + 1) % 4]
        self.hold = hold
        self.volume = np.count_nonzero(self.shape)

    # Rotating the piece based on the pre-generated rotations.
    # X, Y position doesn't change thanks to implementation of so-called Super Rotation System
    # (official Tetris way for pieces to behave).
    def rotate(self, dr, dx, dy):
        self.shape = self.get_rotated_shape(dr)
        self.rotation += dr
        self.rotation = self.rotation % 4
        self.x += dx
        self.y += dy

    # Moving the piece in specified direction
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def get_rotated_shape(self, dr):
        return tetrominos_shapes[self.shape_name][(self.rotation + dr) % 4]


class Game():
    # Game initialization
    def __init__(self, width, height):
        global board_width
        board_width = width
        # Generating empty board
        self.board = np.zeros((height, width), dtype=int)

        # Initial score set to 0
        self.score = 0
        self.level = 1
        self.lines = 0
        self.game_over = False

        # Initialization of queue of pieces and generating first piece to play
        self.pieces_queue = []
        self.new_piece()

        self.piece_on_hold = None


    # Function taking next piece from the queue and maintaining constant number of 3 pieces in the queue
    def new_piece(self):
        # We are making the queue of length 4 as we are taking a piece from it right away.
        while len(self.pieces_queue) != 4:
            self.pieces_queue.append(random.choice(list(tetrominos_shapes.keys())))
        self.current_tetromino = Tetromino(self.pieces_queue.pop())

    # Function moving the piece in given direction (y increases downwards)
    def move(self, dx, dy, drop=False):
        if dy == 1:
            self.score += 1
        if not self.collision_move(dx, dy):
            self.current_tetromino.x += dx
            self.current_tetromino.y += dy
        # If there is a collision and player tried to move piece downwards, place it
        elif dy == 1:
            # If we are not dropping the piece to the bottom, we ignore the exception
            # The exception stops the dropping loop
            if not drop:
                try:
                    self.place()
                except Exception:
                    pass
            if drop:
                self.place()

    # Function rotating the current piece
    def rotate(self, dr):
        kicks = self.get_kicks(self.current_tetromino.rotation, dr, self.current_tetromino.shape_name)
        for dx, dy in kicks:
            if not self.collision_rotation(dr, dx, dy):
                self.current_tetromino.rotate(dr, dx, dy)
                break

    # Dropping the pieces all the way to the bottom
    def hard_drop(self):
        while True:
            # Stop when bottom reached
            try:
                self.move(0, 1, True)
                self.score += 1
            except Exception:
                break

    # Function checking whether there will occur a collision while moving horizontally or vertically.
    # It compares the number of non-zero elements in a state before the move and after the move.
    def collision_move(self, dx, dy):
        current = self.get_board_with_tetromino()
        tried_move = self.get_board_with_tetromino(x=self.current_tetromino.x + dx, y=self.current_tetromino.y + dy)
        if np.count_nonzero(current) == np.count_nonzero(tried_move):
            return False
        return True

    # Function checking whether there will be a collision while rotating.
    # It works similarly to the checking collision on move, it compares number of non-zero elements
    def collision_rotation(self, dr, dx, dy):
        current = self.get_board_with_tetromino()
        tried_move = self.get_board_with_tetromino(shape=self.current_tetromino.get_rotated_shape(dr), x=self.current_tetromino.x + dx, y=self.current_tetromino.y + dy)
        if np.count_nonzero(current) == np.count_nonzero(tried_move):
            return False
        return True

    # Function responsible for placing a piece.
    # It updates the board and generates a new piece
    def place(self):
        self.board = self.get_board_with_tetromino()
        self.clear_rows()
        del self.current_tetromino
        self.new_piece()
        if np.count_nonzero(self.board) + self.current_tetromino.volume != np.count_nonzero(self.get_board_with_tetromino()):
            self.game_over = True
        # Exception to stop hard drop loop
        raise Exception("Block placed")

    # Function returning the board along with current tetromino.
    # Used for checking for collisions, placing a piece and display purposes.
    def get_board_with_tetromino(self, board=None, shape=None, x=None, y=None):
        # If no arguments are given, we use the default ones.
        # This cannot be done in the function definition as the arguments are mutable objects
        if board is None:
            board = self.board
        if shape is None:
            shape = self.current_tetromino.shape
        if x is None:
            x = self.current_tetromino.x
        if y is None:
            y = self.current_tetromino.y

        # Copy is necessary in order to not modify the original board
        board = board.copy()

        for i, row in enumerate(shape):
            for j, value in enumerate(row):
                if value != 0:
                    if x + j >= 0 and x + j < board_width and y + i < len(board) and y + i >= 0:
                        board[y + i][x + j] = value
        return board

    # Functino for clearing full rows
    def clear_rows(self):
        old_board = self.board.copy()
        new_board = []
        lines_cleared = 0
        scoring = (0, 100, 300, 500, 800)

        # We copy all rows that are not full
        for row in old_board:
            if np.count_nonzero(row) != len(row):
                new_board.append(row)

        # Then we as many empty rows as many full we have removed
        while len(new_board) < len(old_board):
            new_board.insert(0, np.zeros_like(old_board[0]))
            lines_cleared += 1

        self.lines += lines_cleared
        self.level = self.lines//10
        self.score += scoring[lines_cleared]
        self.board = np.array(new_board)

    # Function for holding a piece
    def hold(self):
        # Check if player didn't already hold in this round
        if not self.current_tetromino.hold:
            # If player hasn't held before, hold a piece and generate a new one
            if self.piece_on_hold is None:
                self.piece_on_hold = self.current_tetromino.shape_name
                self.new_piece()
                self.current_tetromino.hold = True
            # If player held before, swap the current and held pieces
            else:
                self.current_tetromino, self.piece_on_hold = Tetromino(self.piece_on_hold,
                                                                       True), self.current_tetromino.shape_name

    def ghost_piece(self):

        ghost_piece_position = []

        dy = 0
        while not self.collision_move(0 , dy):
            dy += 1
        dy -= 1
        for i, row in enumerate(self.current_tetromino.shape):
            for j, value in enumerate(row):
                if value != 0:
                    ghost_piece_position.append((self.current_tetromino.y + i + dy, self.current_tetromino.x + j))
        return ghost_piece_position

    def get_kicks(self, r, dr, shape_name):
        if shape_name == "I":
            return i_kicks[(r, dr)]
        else:
            return jlstz_kicks[(r, dr)]