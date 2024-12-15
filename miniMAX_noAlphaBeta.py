from GUI import * 

def minimax_no_pruning(board, depth, maximizingPlayer, tree, parent_id="Root"):
    if depth == 0 or is_terminal_node(board):
        return None, score_position(board, 2)

    node_id = f"Node_{len(tree)}"  # Node tracking for visualization
    tree[parent_id].append(node_id)
    tree[node_id] = []

    valid_locations = get_valid_locations(board)
    
    if maximizingPlayer:  # Maximize AI
        max_eval = -math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            temp_board = board.copy()
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, 2)
            _, eval = minimax_no_pruning(temp_board, depth - 1, False, tree, node_id)
            if eval > max_eval:
                max_eval = eval
                column = col
        return column, max_eval

    else:  # Minimize Player
        min_eval = math.inf
        column = random.choice(valid_locations)

        for col in valid_locations:
            temp_board = board.copy()
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, 1)
            _, eval = minimax_no_pruning(temp_board, depth - 1, True, tree, node_id)
            if eval < min_eval:
                min_eval = eval
                column = col
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
            # col, minimax_score = minimax(board, 2, -math.inf, math.inf, True, tree)
            col, minimax_score = minimax_no_pruning(board, 2, True, tree)

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
