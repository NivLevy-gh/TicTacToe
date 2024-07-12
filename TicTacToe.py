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

    # Minimax algorithm
    def minimax(self, depth, is_maximizing):
        if self.winner():
            return 1 if self.current_player.label == 'O' else -1
        if self.tied():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.current_moves[row][col].label == "":
                        self.current_moves[row][col] = Move(row, col, 'O')
                        self.current_player = Player(label='X', color='blue')
                        score = self.minimax(depth + 1, False)
                        self.current_moves[row][col] = Move(row, col)
                        self.current_player = Player(label='O', color='red')
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.current_moves[row][col].label == "":
                        self.current_moves[row][col] = Move(row, col, 'X')
                        self.current_player = Player(label='O', color='red')
                        score = self.minimax(depth + 1, True)
                        self.current_moves[row][col] = Move(row, col)
                        self.current_player = Player(label='X', color='blue')
                        best_score = min(score, best_score)
            return best_score

    # Find the best move
    def best_move(self):
        best_score = -math.inf
        move = None
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.current_moves[row][col].label == "":
                    self.current_moves[row][col] = Move(row, col, 'O')
                    self.current_player = Player(label='X', color='blue')
                    score = self.minimax(0, False)
                    self.current_moves[row][col] = Move(row, col)
                    self.current_player = Player(label='O', color='red')
                    if score > best_score:
                        best_score = score
                        move = Move(row=row, col=col, label='O')
        return move




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
                self.BotMoveOptimal()


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
    
    instructions = f'I will give you a raw code output of the status of a standard {BOARD_SIZE} by {BOARD_SIZE} Tic-Tac-Toe Game. For example, for a standard 3 by 3 tictactoe game, the formatting will be something like this to represent the first row: "[[Move(row=0, col=0, label=\'X\'), Move(row=0, col=1, label=\'O\'), Move(row=0, col=2, label=\'\')]]". This represents the first row of the board. From the left to the right, there is an X, followed by an O, followed by an empty (unplayed) space. Your job is to act as the other player (you will go second). You will take the symbol that has not been played (X or O). You may only play a move on an empty square. Your job is to win the tic-tac-toe game by connecting three of your symbol in a row. You will do this by outputting ONLY 3 things, all separated by a whitespace: `row (number), column (number), and symbol (X or O).` It does not matter if we are several moves in and there can be no winner. you must keep playing valid moves. You should always try to win.'
    
    # Defines ChatGPT Function for playing with a robot
    def BotMove(self):
        prompt = [{"role": "system", "content": f'{Board.instructions} Here is the Raw Code output: {self.Game.current_moves}'}]

        response = openai.chat.completions.create(
            model = 'gpt-3.5-turbo',
            messages = prompt,
        )
        bot_response = response.choices[0].message.content.strip()
        row, col, label = bot_response.split()
        row, col = int(row), int(col)
        print(row, col, label)
        move = Move(row=row, col=col, label=label)

        self.Game.current_moves[row][col] = move
        print("response received!")

        # Update button in GUI for visual representation of bot's move
        button = next(
            button for button, (r, c) in self.cells.items() if r == row and c == col
        )
        self.update_button(button)

        # Process the bot's move in the game logic
        self.Game.process_move(move)

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

    def BotMoveOptimal(self):
        # Get the best move for the bot
        move = self.Game.best_move()

        # Make the move
        if move:
            row, col, label = move.row, move.col, move.label
            print(row, col, label)

            self.Game.current_moves[row][col] = move
            print("Optimal move response received!")

            # Update button in GUI for visual representation of bot's move
            self.update_button(row, col, move)

            # Process the bot's move in the game logic
            self.Game.process_move(move)

            # Check game status after bot's move
            if self.Game.tied():
                self.update_display(msg="Tied Game!", color="green")
            elif self.Game.winner():
                msg = f'Player "{self.Game.current_player.label}" won!'
                color = self.Game.current_player.color
                self.update_display(msg, color)
                self.highlight_cells()
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


