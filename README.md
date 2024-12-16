# Connect 4 AI Game Project  

## Overview  
**Connect 4** is a two-player strategy game where players alternate turns to drop their colored discs into a vertical grid. The discs fall straight down to occupy the next available space in the chosen column.  

### Objective  
The goal is to connect four of your discs of the same color in a row, either:  
- **Vertically**  
- **Horizontally**  
- **Diagonally**  

The game ends when the board is full. The winner is determined by the player who achieves the most "connect-fours."  

---

## AI Implementation  

The AI agent for this game uses **Minimax algorithms** with two variations:  
1. **Minimax without Alpha-Beta Pruning**  
2. **Minimax with Alpha-Beta Pruning**  

These algorithms allow the AI to simulate and evaluate potential moves to choose the most optimal strategy.  

---

## Heuristic Function  

The AI's decision-making is powered by a heuristic function that evaluates the state of the board to estimate the likelihood of winning for either player.  

### Key Features of the Heuristic Function  
The heuristic consists of two main components:  
1. **`score_position`**: Evaluates the entire game board.  
2. **`evaluate_window`**: Analyzes specific "windows" of four cells.  

### Scoring Criteria  
The board is divided into 4-cell "windows" (horizontal, vertical, and diagonal), each evaluated based on the following:  
- **4 AI pieces in a window**: **+100 points** (High priority for winning moves).  
- **3 AI pieces + 1 empty cell**: **+5 points** (Good strategic placement).  
- **2 AI pieces + 2 empty cells**: **+2 points** (Moderate benefit).  
- **3 opponent pieces + 1 empty cell**: **-15 points** (Discourage letting the opponent win).  

### Strategic Considerations  
- **Diagonal and Horizontal Advantage**: Positive and negative diagonal windows are evaluated to account for strategic placements that lead to a win.  
- The heuristic aims to:  
  - **Maximize** the score when the AI is close to winning.  
  - **Minimize** the score when the opponent is close to winning.  
  - Enable efficient **pruning** by narrowing the focus to the most promising moves.  

---

## Algorithms  
### Minimax without Alpha-Beta Pruning  
- Explores the entire game tree up to a fixed depth.  
- Slower due to exhaustive search but guarantees the optimal move.  

### Minimax with Alpha-Beta Pruning  
- Optimized version of Minimax.  
- Prunes branches of the game tree that don't affect the outcome.  
- Faster performance while maintaining the same optimal decisions.  

---

## Future Enhancements  
- Add additional difficulty levels.  
- Improve heuristic function for more dynamic strategies.  
- Implement a graphical user interface (GUI) for better user interaction.  

---

### Instructions  
1. Clone the repository.  
2. Run the main Python script.  
3. Select game mode (human vs. AI or AI vs. AI).  
4. Enjoy the game!  

---

# Libraries:
- numpy => pip install numpy 
- pygame => pip install pygame 
- graphviz.Digraph => pip install graphviz + Download graphviz-12.2.1 (64-bit) EXE installe \n
Link: https://graphviz.org/download/ 
after download don't forget to add graphviz path into environment
