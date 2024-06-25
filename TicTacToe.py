# Import built-in Tkinter for GUI construction
# Tkinter will need to be version > 8.6 
# If Tkinter is < 8.6, update Python to > 3.9.8

import tkinter as tk
from tkinter import font

# Defining the TicTacToe board class:
class Board(tk.Tk):
    def __init__(self):
        # Initialize Board (parent class) with super()
        super().__init__()
        # Set title
        self.title("Tic-Tac-Toe!")
        # Initialize empty cells dictionary
        self.cells = {}
        # Initialize Display
        self.CreateDisplay()
        # Initialize Grid
        self.CreateGrid()
    

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
        for row in range(3):
            # Width/length
            self.rowconfigure(row,weight=1, minsize=50)
            self.columnconfigure(row,weight=1, minsize=75)
            # Sets 2nd `for` loop to configure number of columns/coords
            for col in range(3):
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
                # Adds all (9) buttons to grid (main window)
                button.grid(
                    row = row,
                    column = col,
                    padx = 5,
                    pady = 5, 
                    sticky = "nsew"
                )

# Defines `main()` function to create instance of Board()
def main():
    # Create gameboard and run loop
    board = Board()
    board.mainloop()

if __name__ == "__main__":
    main()