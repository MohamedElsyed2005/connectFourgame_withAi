from GUI import *

def minimax(board, depth, alpha, beta, maximizingPlayer, tree, parent_id= "Root"): 
    if depth == 0 or is_terminal_node(board):
        return None, score_position(board, 2)

    node_id = f"Node_{len(tree)}" # {"Root": []} => 2st node_id = "Node_2" # [1,2].append(3) = > [1,2,3]
    tree[parent_id].append(node_id) # {"Root": ["Node_1"]}
    tree[node_id] = [] # {"Root": ["Node_1" = ["Node_2"] ]}
    vaild_location = get_valid_locations(board) # [0,1,2,3,4,5,6]
    
    if maximizingPlayer: # max
        max_eval = -math.inf
        column = random.choice(vaild_location) # 3

        for col in vaild_location: # 0
            temp_board = board.copy()
            row = get_next_open_row(temp_board, col) # col 0, row 1
            drop_piece(temp_board, row, col, 2) # doesn't appear in GUI
            eval = minimax(temp_board, depth-1, alpha, beta, False, tree, node_id)[1] # 1, {"Root": ["Node_1" = [] ]}
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
            row = get_next_open_row(temp_board, col) # 1
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
    tree = {"Root": []} # dictionary {"Root": []}

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
            # col = np.random.choice(get_valid_locations(board))
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
