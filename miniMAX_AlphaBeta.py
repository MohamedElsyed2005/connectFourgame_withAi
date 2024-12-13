import numpy as np
import pygame # int 
import sys
import math
from threading import Timer
"""
 [[0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],               np.zeros((6,7))
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0]]
 
 
"""

bord_color = (0,0,0)
empty_circle = (253,245,230)
player_1_color = (50,205,50)
player_2_color = (0,0,128)

player_1 = 1
player_2 = 2

players = [player_1,player_2]

# creating a board from numpy
def create_board():
    board =  np.zeros((6,7))
    return board

def drop_piece(board,selec,row, no_of_player):
    board[row][selec] = no_of_player

def is_loc_valid(board,selec):

    if board[0][selec] == 0 :
        return True
    else: 
        label = my_font.render("column is full!", 1, (139,0,0))
        screen.blit(label, (40, 10))
        return False
    

def get_open_valid_pos(board,selec):
    for r in range(6-1, -1, -1):
        if board[r][selec] == 0:
            return r

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
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, 7//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

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

	## Score posiive sloped diagonal
	for r in range(6-3):
		for c in range(7-3):
			window = [board[r+i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	for r in range(6-3):
		for c in range(7-3):
			window = [board[r+3-i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	return score

def minimaxAlphaBeta():
      pass

def draw_board(board):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, bord_color, (c * size, r * size + size, size, size ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, empty_circle, (int(c * size + size/2), int(r* size + size + size/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, player_1_color, (int(c * size + size/2), int(r* size + size + size/2)), circle_radius)
            else :
                pygame.draw.circle(screen, player_2_color, (int(c * size + size/2), int(r* size + size + size/2)), circle_radius)

    pygame.display.update()

def is_terminal_node(board):
	return check_win(board, 1) or check_win(board, 2) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(7):
		if is_loc_valid(board, col):
			valid_locations.append(col)
	return valid_locations

board = create_board()
game_over = False

not_over = True

def end_game():
    global game_over
    game_over = True
    print(game_over)

turn = 0

# start game 
pygame.init()

size  = 100

width = 100 * 7
height = 100 * (6 + 1)

circle_radius = int(size/2 - 5) # 100/2 - 5 = 45

screen = pygame.display.set_mode((width , height))
draw_board(board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, bord_color, (0, 0, width, size))
            xpos = pygame.mouse.get_pos()[0]
            # turn 0 => player 1
            if turn == 0:
                pygame.draw.circle(screen, player_1_color, (xpos, int(size/2)), circle_radius )

        if event.type == pygame.MOUSEBUTTONDOWN and not_over:

            pygame.draw.rect(screen, bord_color, (0, 0, width, size))
            if turn == 0 :
                # we assume players will use correct input
                xpos = event.pos[0] 
                selec = int(math.floor(xpos/size)) #int(input("Player 1 make your selection by typing (0-6):"))

                if is_loc_valid(board,selec):
                    row = get_open_valid_pos(board,selec)
                    drop_piece(board,selec,row, player_1 )
                    if check_win(row, selec):
                        print("PLAYER 1 WINS!")
                        label = my_font.render("PLAYER 1 WINS!", 1, (139,0,0))
                        screen.blit(label, (40, 10))
                        not_over = False
                        t = Timer(3.0, end_game)
                        t.start()

                draw_board(board) 

                # increment turn by 1
                turn += 1

                # this will alternate between 0 and 1 withe very turn
                turn = turn % 2 

        pygame.display.update()
        
    if turn == 1 and not_over and not game_over:

        col, minimax_score = minimaxAlphaBeta()

        if is_loc_valid(board,selec):
            pygame.time.wait(500)
            row = get_open_valid_pos(board,selec)
            drop_piece(board,selec,row, player_2 )
             
            if check_win(row, selec):
                print("PLAYER 2 WINS!")
                label = my_font.render("PLAYER 2 WINS!", 1, (139,0,0))
                screen.blit(label, (40, 10))
                not_over = False
                t = Timer(3.0, end_game)
                t.start()

        draw_board(board)

        # increment turn by 1
        turn += 1
         # this will alternate between 0 and 1 withe very turn
        turn = turn % 2

draw_board(board)
