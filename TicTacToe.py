# Import built-in Tkinter for GUI construction
# Tkinter will need to be version > 8.6 
# If Tkinter is < 8.6, update Python to > 3.9.8
# Import NamedTuple module for data storage
# Import cycle from itertools
import os
import tkinter as tk
from tkinter import font
from typing import NamedTuple
from itertools import cycle
import math

# Import OpenAI as Chatbot for move response
import openai

# Import python-dotenv variable to hide API Key
from dotenv import load_dotenv
load_dotenv()

# Need to create a .env file and put it in .gitignore
openai.api_key = os.getenv("OPENAI_KEY")

# Define Player class
class Player(NamedTuple):
    # `Label` attribute stores player signs (X/O)
    label: str
    # Player identifier
    color: str

# Defines Move class
class Move(NamedTuple):
    # Stores coordinates for moves
    row: int
    col: int
    # Player identifier
    label: str = ""

# Defines constant variables and assigns player symbols
BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="red")
)

# Define TicTacToe game class
class Game:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self.Players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.Players)
        self.winner_combo = []
        self.current_moves = []
        self.has_winner = False
        self.winning_combos = []
        self.setup_board()
    
    def setup_board(self):
        # Creates initial list of move values
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        # Calls `get_winning_combos` and assigns value to `winning_combos`
        self.winning_combos = self.get_winning_combos()

    # Defines winning combinations on a TicTacToe board
    def get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self.current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        # Returns list of all possible winning combinations
        return rows + columns + [first_diagonal, second_diagonal]
    
    # Defines what a valid move is
    def valid_move(self, move):
        # Performs check for two conditions: game not won & move not played
        row, col = move.row, move.col
        move_not_played = self.current_moves[row][col].label == ""
        no_winner = not self.has_winner
        # Returns True or False
        return move_not_played and no_winner
    
    # Defines move-processing process
    def process_move(self, move):
        # Collect row/column coordinates from input move
        row, col = move.row, move.col
        self.current_moves[row][col] = move
        # Check current moves against winning combinations
        for combo in self.winning_combos:
            results = set(
                self.current_moves[n][m].label
                for n, m in combo
            )
            # Tests for both conditions to be true
            is_win = (len(results) == 1) and ("" not in results)
            # If true, then `has_winner` becomes True, the function ends
            if is_win:
                self.has_winner = True
                self.winner_combo = combo
                break
    
    def undo_move(self, move):
        # Undo moves
        row, col = move.row, move.col
        self.current_moves[row][col] = Move(row, col)

    # Defines and returns `has_winner` Boolean
    def winner(self):
        return self.has_winner

    # Defines conditions for a tied game
    def tied(self):
        no_winner = not self.has_winner
        # Define a list of all the played moves
        played_moves = (
            move.label for row in self.current_moves for move in row
        )
        # Returns two Booleans to see if game is tied
        return no_winner and all(played_moves)
    
    # Defines player turn-toggler
    def toggle_player(self):
        # Switches to next player
        self.current_player = next(self.Players)

    # Define reset game function
    def reset_game(self):
        # Resets all played moves to empty objects
        for row, row_content in enumerate(self.current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        # Reset `has winner` Boolean to False
        self.has_winner = False
        # Reset played X/O's, winner of previous match goes first
        self.winner_combo = []

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        if board.winner():
            return -1 if maximizing_player else 1
        elif board.tied():
            return 0
        
        if maximizing_player:
            max_eval = -math.inf
            for move in self.available_moves(board):
                board.process_move(move)
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                board.process_move(Move(row=move.row, col=move.col))
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in self.available_moves(board):
                board.process_move(move)
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                board.process_move(Move(row=move.row, col=move.col))
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # Function to get available moves on the board
    def available_moves(self, board):
        moves = []
        for row in range(board.board_size):
            for col in range(board.board_size):
                if board.valid_move(Move(row, col)):
                    moves.append(Move(row, col, board.current_player.label))
        return moves

    # Function to determine the best move for the bot using minimax
    def get_best_move(self, board):
        best_move = None
        best_eval = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in self.available_moves(board):
            board.process_move(move)
            eval = self.minimax(board, 0, False, alpha, beta)
            board.process_move(Move(row=move.row, col=move.col))
            
            if eval > best_eval:
                best_eval = eval
                best_move = move

        return best_move


# Defining the TicTacToe board class
class Board(tk.Tk):
    def __init__(self, game):
        # Initialize Board (parent class) with super()
        super().__init__()
        # Set title
        self.title("Tic-Tac-Toe!")
        # Initialize empty cells dictionary
        self.cells = {}
        # Initialize game code
        self.Game = game
        # Initialize GUI menu
        self.Menu()
        # Initialize Display
        self.CreateDisplay()
        # Initialize Grid
        self.CreateGrid()
    
    # Defines menu
    def Menu(self):
        # Create menu bar
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label = "Play Again",
            # Initialize board reset when "Play Again" is clicked
            command = self.reset
        )
        file_menu.add_separator()
        # Add options to exit and file dropdown
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="file", menu=file_menu)

    # Defines `play` infinite loop
    def play(self, event):
        # Retrieves clicked button widget
        click = event.widget
        # Collects row/column coordinates of button clicked
        row, col = self.cells[click]
        move = Move(row, col, self.Game.current_player.label)
        # Checks to see if move was valid
        if self.Game.valid_move(move):
            self.update_button(click)
            self.Game.process_move(move)
            # Print "Tied Game!" message if tied game
            if self.Game.tied():
                # Tied message
                self.update_display(msg="Tied Game!", color="green")
            # Print "Player 1/2 Won!" message if Player 1/2 won
            elif self.Game.winner():
                # Highlight winning cells
                self.highlight_cells()
                # Winning message/color
                msg = f'Player "{self.Game.current_player.label}" won!'
                color = self.Game.current_player.color
                self.update_display(msg, color)
            # Or else keep playing
            else:
                self.Game.toggle_player()
                msg = f"{self.Game.current_player.label}'s turn"
                self.update_display(msg)
                print(self.Game.current_moves)
                self.BotMove()


    # Generate display
    def CreateDisplay(self):
        # Create `Frame` object to hold display
        display_frame = tk.Frame(master=self)
        # Packs display & ensure dimensions on window resize
        display_frame.pack(fill=tk.X)
        # Create `Label` object with text
        self.display = tk.Label(
            master = display_frame,
            text = "Ready?",
            font = font.Font(size=28, weight="bold"),
        )
        # Packs `Label` inside `Display`
        self.display.pack()

    # Generate grid
    def CreateGrid(self):
        # Create `Frame` object to hold grid
        grid_frame = tk.Frame(master=self)
        # Packs grid
        grid_frame.pack()
        # Sets `for` loop to configure number of rows/coords
        for row in range(self.Game.board_size):
            # Width/length
            self.rowconfigure(row,weight=1, minsize=50)
            self.columnconfigure(row,weight=1, minsize=75)
            # Sets 2nd `for` loop to configure number of columns/coords
            for col in range(self.Game.board_size):
                # Configs `Button``
                button = tk.Button(
                    master = grid_frame,
                    text = "",
                    font = font.Font(size=36, weight="bold"),
                    fg = "black",
                    width = 3, 
                    height = 2, 
                    highlightbackground = "lightblue",
                )
                # Adds all (9) buttons to the self.cells dictionary
                self.cells[button] = (row,col)
                # Binds button to `click` widget for def(play) above
                button.bind("<ButtonPress-1>", self.play)
                # Adds all (9) buttons to grid (main window)
                button.grid(
                    row = row,
                    column = col,
                    padx = 5,
                    pady = 5, 
                    sticky = "nsew"
                )
    
    # Defines grid button update function
    def update_button(self, click):
        # Sets clicked grid's label and color to that of current player
        click.config(text=self.Game.current_player.label)
        click.config(fg=self.Game.current_player.color)

    # Define display update function
    def update_display(self, msg, color="black"):
        # Utilize dictionary-style notation to tweak display
        self.display["text"] = msg
        self.display["fg"] = color

    # Define winning cells highlighting function
    def highlight_cells(self):
        # Iterate items in `cells` dictionary
        # Maps buttons to row/column coordinates on grid
        for button, coordinates in self.cells.items():
            # Highlights winning combination in purple
            if coordinates in self.Game.winner_combo:
                button.config(highlightbackground="Purple")

    # Define reset board function
    def reset(self):
        # Calls `reset_game` function to reset memory
        self.Game.reset_game()
        # Resets GUI and board 
        self.update_display(msg="Ready?")
        for button in self.cells.keys():
            button.config(highlightbackground='lightblue')
            button.config(text='')
            button.config(fg='white')

    def BotMove(self):
        # Get the best move using minimax algorithm
        move = self.Game.get_best_move(self.Game)

        # Process the bot's move in the game logic
        self.Game.process_move(move)

        # Update button in GUI for visual representation of bot's move
        button = next(
            button for button, (r, c) in self.cells.items() if r == move.row and c == move.col
        )
        self.update_button(button)

        # Check game status after bot's move
        if self.Game.tied():
            self.update_display(msg="Tied Game!", color="green")
        elif self.Game.winner():
            msg = f'Player "{self.Game.current_player.label}" won!'
            color = self.Game.current_player.color

            
            self.update_display(msg, color)
        else:
            self.Game.toggle_player()
            msg = f"{self.Game.current_player.label}'s turn"
            self.update_display(msg)


# Defines `main()` function to create instance of Board()
def main():
    # Create `Game` instance from `game`
    game = Game()
    board = Board(game)
    # Create GUI loop
    board.mainloop()

# Ensure local app running only
if __name__ == "__main__":
    main()


