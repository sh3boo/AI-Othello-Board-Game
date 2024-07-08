Introduction
This project is an Othello (also known as Reversi) game implemented using Python and Pygame. The game allows you to play against a computer opponent with adjustable difficulty levels.

Installation
To run the Othello game, you need to have Python and Pygame installed on your system.

Install Python:
Download and install the latest version of Python from python.org.

Install Pygame:
Open your terminal or command prompt and run:

sh
Copy code 
pip install pygame
Clone the Repository:

sh
Copy code
git clone https://github.com/your-repo/othello-ai-game.git
cd othello-ai-game
Run the Game:

sh
Copy code
python othello.py
How to Play
Starting the Game:

Run the game using the instructions above.
The game window will open with a grid representing the Othello board.
Gameplay:

You are the first player (white tokens) and the computer is the second player (black tokens).
Click on a valid cell to place your token.
The game will highlight available moves for the current player.
The objective is to have the majority of your tokens on the board at the end of the game.
Game Over:

The game ends when neither player can make a valid move.
The player with the most tokens on the board wins.
Code Overview
The game consists of several classes and utility functions that handle different aspects of the game, including the game state, player actions, and AI decisions.

Game Classes
Grid
The Grid class represents the game board and handles the game state, including initializing the board, rendering the game, and calculating scores.

Token
The Token class represents individual tokens on the board and handles their rendering and transitions.

Utility Functions
Utility functions include:

directions(x, y): Determines valid move directions from the current cell.
loadScaledImage(path, size): Loads and scales images.
loadSpriteSheet(sheet, row, col, new_size, size): Loads a specific sprite from a sprite sheet.
Game Controller
The mainGameClass serves as the game controller. It handles user input, updates the game state, renders the game, and controls the game flow.

mainGameClass
Initialization:
Sets up the game window, players, and initial game state.
Methods:
runGame(): Main game loop.
handleUserInput(): Handles user input events.
updateGameState(): Updates the game state based on player actions.
renderGameOnScreen(): Renders the current game state.
AI Implementation
The AI opponent uses an Alpha-Beta Pruning algorithm to determine the best move based on the current game state. The difficulty of the AI can be adjusted by changing the depth of the search.

ComputerPlayer
Initialization:
Takes the game grid as input.
Methods:
findBestMoveWithAlphaBeta(grid, depth, alpha, beta, player): Implements the Alpha-Beta Pruning algorithm to find the best move for the AI.
License
This project is licensed under the MIT License. Feel free to use, modify, and distribute this code.

Enjoy playing Othello! If you have any questions or suggestions, please feel free to reach out.

Happy gaming!
