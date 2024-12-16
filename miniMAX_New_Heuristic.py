import numpy as np
import pygame
import sys
from graphviz import Digraph
import random
import math


PLAYER = 0
AI = 1


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

def get_next_open_row(board, col):
    for r in range(6):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    row_moves = [0, 1, 1, 1]
    col_moves = [1, 0, 1, -1]

    for r in range(6):
        for c in range(7):
            if board[r][c] == piece:  
                for direction in range(4):
                    count = 0
                    for step in range(4):
                        new_row = r + step * row_moves[direction]
                        new_col = c + step * col_moves[direction]

                        if 0 <= new_row < 6 and 0 <= new_col < 7 and board[new_row][new_col] == piece:
                            count += 1
                        else:
                            break
                    
                    if count == 4: 
                        return True
    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = 1 if piece == 2 else 2

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 100

    return score

def score_position(board, piece):
    score = 0
    row_moves = [0, 1, 1, 1]
    col_moves = [1, 0, 1, -1]
    opp_piece = 1 if piece == 2 else 2

    # Score based on potential lines
    for r in range(6):
        for c in range(7):
            for direction in range(4):
                window = []
                for step in range(4):
                    new_row = r + step * row_moves[direction]
                    new_col = c + step * col_moves[direction]
                    
                    if 0 <= new_row < 6 and 0 <= new_col < 7:
                        window.append(board[new_row][new_col])
                    else:
                        break
                
                if len(window) == 4:
                    score += evaluate_window(window, piece)
    return score

def draw_board(board):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, (0,0,0), (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, (253,245,230), (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(7):
        for r in range(6):
            if board[r][c] == 1:
                pygame.draw.circle(screen, (50,205,50), (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, (0,0,128), (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    return [c for c in range(7) if is_valid_location(board, c)]

def save_minimax_tree(tree, output_path="minimax_tree"):
    dot = Digraph(comment="Minimax Tree")
    dot.node("Root", "Root")
    for parent, children in tree.items():
        for child in children:
            dot.node(child, child)
            dot.edge(parent, child)
    dot.render(output_path, format="png", cleanup=True)
    print(f"Minimax tree saved to {output_path}.png")

def minimax(board, depth, alpha, beta, maximizingPlayer, tree, parent_id= "Root"): 
    if depth == 0 or is_terminal_node(board):
        return None, score_position(board, 2)

    node_id = f"Node_{len(tree)}"
    tree[parent_id].append(node_id)
    tree[node_id] = []
    vaild_location = get_valid_locations(board)
    
    if maximizingPlayer:
        max_eval = -math.inf
        column = random.choice(vaild_location)

        for col in vaild_location:
            temp_board = board.copy()
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, 2)
            eval = minimax(temp_board, depth-1, alpha, beta, False, tree, node_id)[1]
            if eval > max_eval:
                 max_eval = eval
                 column = col 
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return column, max_eval
    else: 
        min_eval = math.inf 
        column = random.choice(vaild_location)

        for col in get_valid_locations(board):
            temp_board = board.copy()
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, 1)
            eval = minimax(temp_board, depth-1, alpha, beta, True, tree, node_id)[1]
            if eval < min_eval:
                 min_eval = eval
                 column = col
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return column, min_eval

def main():
    board = create_board()
    game_over = False
    turn = PLAYER
    tree = {"Root": []}

    draw_board(board)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(posx // SQUARESIZE)
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        if winning_move(board, 1):
                            label = font.render("Player 1 wins!", 1, (50,205,50))
                            screen.blit(label, (40, 10))
                            game_over = True
                        turn = AI
                        draw_board(board)

        if turn == AI and not game_over:
            col, minimax_score = minimax(board, 3, -math.inf, math.inf, True, tree)
            save_minimax_tree(tree, "output\\minimax_tree")
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if winning_move(board, 2):
                    label = font.render("AI wins!", 1, (0,0,128))
                    screen.blit(label, (40, 10))
                    game_over = True
                turn = PLAYER
                draw_board(board)

        if game_over:
            pygame.time.wait(3000)

if __name__ == "__main__":
    main()
