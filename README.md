# connectFourgame_withAi
# Project Overview:  
Connect 4 is a two-player game in which the players first choose a color and then take \n
turns dropping their colored discs from the top into a grid. The pieces fall straight  
down, occupying the next available space within the column. The objective of the 
game is to connect-four of one’s own discs of the same color next to each other 
vertically, horizontally, or diagonally. The two players keep playing until the board is 
full. The winner is the player having greater number of connected-fours. 

## the following 2 algorithms as options for the AI agent: 
• Minimax without alpha-beta pruning.
• Minimax with alpha-beta pruning.

# Heuristic Function: 
• The heuristic function implemented in this project is defined as the 
score_position and evaluate_window function. It evaluates the game board's 
state to estimate the likelihood of winning for the AI agent or the player. This 
evaluation is crucial for pruning the game tree and focusing on the most 
promising moves. The function considers various factors to assign a score to the 
board, helping the AI make optimal decisions. 
• Details of the Heuristic Function 
• The board is divided into 4-cell "windows" (horizontal, vertical, positive diagonal 
and negative diagonal), and each window is evaluated using the 
evaluate_window function. 
# The evaluation assigns scores based on: 
• 4 AI pieces in a window: Adds a high score (+100 points). 
• 3 AI pieces + 1 empty cell: Adds a moderate score (+5 points). 
• 2 AI pieces + 2 empty cells: Adds a small score (+2 points). 
• 3 opponent pieces + 1 empty cell: Subtracts points to discourage letting the 
opponent win (-15 points). 
# Diagonal and Horizontal Advantage: 
• The function evaluates positive and negative diagonal windows, as well as 
horizontal windows, to account for strategic placements. 
The score_position heuristic is designed to:  
• Return a higher score when the AI is closer to winning. 
• Return a lower score (or a negative one) when the opponent is closer to 
winning. 
• Enable efficient pruning of the game tree by limiting depth exploration based on 
evaluated scores.
