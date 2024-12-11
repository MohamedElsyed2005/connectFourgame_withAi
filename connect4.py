import numpy as np
import pygame # int 
import sys

"""
 [[0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],               np.zeros((6,7))
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0]]
 
 
"""

player_1 = 1
player_2 = 2

players = [player_1,player_2]
def create_board():
    board =  np.zeros((6,7))
    return board

def drop_piece(board,selec,row, no_of_player ):
    board[row][selec] = no_of_player

def is_loc_valid(board,selec):

    if board[5][selec] == 0 :
        return True
    else: 
        print("col is full") 
        return False
    

def get_open_valid_pos(board,selec):
    for row in range(6):
        if board[row][selec] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

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

board = create_board()

game_over = False

turn = 0

# start game 
pygame.init()

size  = 100

width = 100 * 7
height = 100 * (6 + 1)

screen = pygame.display.set_mode((width , height))

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    if turn == 0 :
        selec = int(input("player 1 : enter your drop piece 0 - 6 : "))

        if is_loc_valid(board,selec):
             row = get_open_valid_pos(board,selec)
             drop_piece(board,selec,row, player_1 )
             
             if check_win(row, selec):
                 print("player 1 winsssssss")
                 game_over = True
        print_board(board)
    else:
        selec = int(input("player 2 : enter your drop piece 0 - 6 : "))

        if is_loc_valid(board,selec):
             row = get_open_valid_pos(board,selec)
             drop_piece(board,selec,row, player_2 )
             
             if check_win(row, selec):
                 print("player 2 winsssssss")
                 game_over = True
        print_board(board)
    
    turn += 1
    turn = turn % 2


