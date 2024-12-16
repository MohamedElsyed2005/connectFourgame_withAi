import numpy as np
import pygame
import sys
from graphviz import Digraph
import random
import math

# Constants for the game
PLAYER = 0
AI = 1

# Initialize pygame
pygame.init()

SQUARESIZE = 100
width = 7 * SQUARESIZE
height = (6 + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("monospace", 75)

def create_board():
    return np.zeros((6, 7))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[6 - 1][col] == 0

def get_next_open_row(board, col): # [0,1,2,3,4,5,6] = [1,0,0,0,0,0,0]
    for r in range(6):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal
    for r in range(6):
        for c in range(7 - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    
    # Check vertical
    for c in range(7):
        for r in range(6 - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    
    # Check positively sloped diagonals
    for r in range(6 - 3):
        for c in range(7 - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for r in range(3, 6):
        for c in range(7 - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def draw_board(board):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, (160,160,160), (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (253,245,230), (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(7):
        for r in range(6):
            if board[r][c] == 1:
                pygame.draw.circle(screen, (204,0,0), (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (0,204,0), (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def get_valid_locations(board): #[0,1,2,3,4,5,6]
    return [c for c in range(7) if is_valid_location(board, c)]

def evaluate_window(window, piece):
	score = 0
	opp_piece = 1
	if piece == 1:
		opp_piece = 2

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(0) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(0) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(0) == 1:
		score -= 15

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, 7//2])]
	center_count = center_array.count(piece)
	score += center_count * 4

	## Score Horizontal
	for r in range(6):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(7-3):
			window = row_array[c:c + 4]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(7):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(6-3):
			window = col_array[r:r+4]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal 1101
	for r in range(6-3):
		for c in range(7-3):
			window = [board[r+i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	for r in range(6-3):
		for c in range(7-3):
			window = [board[r+3-i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	return score

def save_minimax_tree(tree, output_path="minimax_tree"):
    """
            [Root]
          /       \
      [Child 1]  [Child 2]
       /    \         \
  [Leaf 1] [Leaf 2]   [Leaf 3]
===============================================================================================
  tree_data = [
    {
        'id': 1, 'label': "Root", 'children': [
            {
                'id': 2, 'label': "Child 1", 'children': [
                    {'id': 4, 'label': "Leaf 1"},
                    {'id': 5, 'label': "Leaf 2"}
                ]
            },
            {
                'id': 3, 'label': "Child 2", 'children': [
                    {'id': 6, 'label': "Leaf 3"}
                ]
            }
        ]
    }
]
    """
    dot = Digraph(comment="Minimax Tree")
    dot.node("Root", "Root") # tree {root : root, node1 : node }
    for parent, children in tree.items():
        for child in children:
            dot.node(child, child)
            dot.edge(parent, child)
    dot.render(output_path, format="png", cleanup=True)
    print(f"Minimax tree saved to {output_path}.png")


def check_win(row, col):
        row_moves = [0, 1, 1, 1]
        col_moves = [1, 0, 1, -1]

        for direction in range(len(row_moves)):
            count = 1
            for d in (1, -1):
                r, c = row, col
                while True:
                    r += row_moves[direction] * d
                    c += col_moves[direction] * d
                    if 0 <= r < 6 and 0 <= c < 7 and board[r][c] == players[turn]:
                        count += 1
                    else:
                        break

            if count >= 4:
                return True
        return False