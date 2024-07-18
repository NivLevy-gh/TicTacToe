import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.player = 'X'  # Human player
        self.bot = 'O'     # Bot player
        self.create_board()
        self.optimal_move_probability = 1  # Probability bot makes the optimal move

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text='', font=('consolas', 40), width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def on_button_click(self, i, j):
        if self.buttons[i][j]['text'] == '' and self.current_winner is None:
            self.buttons[i][j]['text'] = self.player
            self.board[i * 3 + j] = self.player
            if self.check_winner(self.player):
                self.current_winner = self.player
                messagebox.showinfo("Tic Tac Toe", "You win!")
            elif ' ' not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_game()
            else:
                self.bot_move()
                if self.check_winner('O'):
                    messagebox.showinfo("Tic Tac Toe", "Bot wins!")
                    self.reset_game()
                elif ' ' not in self.board:
                    messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                    self.reset_game()

    def bot_move(self):
        if self.current_winner is None:
            if random.random() < self.optimal_move_probability:
                move = self.minimax(self.board, self.bot, -float('inf'), float('inf'))[1]
            else:
                move = random.choice(self.available_moves())
            self.board[move] = self.bot
            self.buttons[move // 3][move % 3]['text'] = self.bot
            if self.check_winner(self.bot):
                self.current_winner = self.bot
                messagebox.showinfo("Tic Tac Toe", "Bot wins!")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def check_winner(self, player):
        # Check rows, columns and diagonals
        win_conditions = [
            [self.board[0], self.board[1], self.board[2]],
            [self.board[3], self.board[4], self.board[5]],
            [self.board[6], self.board[7], self.board[8]],
            [self.board[0], self.board[3], self.board[6]],
            [self.board[1], self.board[4], self.board[7]],
            [self.board[2], self.board[5], self.board[8]],
            [self.board[0], self.board[4], self.board[8]],
            [self.board[2], self.board[4], self.board[6]]
        ]
        if [player, player, player] in win_conditions:
            return True
        return False

    def minimax(self, state, player, alpha, beta):
        max_player = self.bot  # Bot is maximizing; human is minimizing
        other_player = 'O' if player == 'X' else 'X'

        # Base cases
        if self.check_winner(other_player):
            return (1, None) if other_player == max_player else (-1, None)
        elif ' ' not in state:
            return (0, None)

        if player == max_player:
            best = [-float('inf'), None]
            for possible_move in self.available_moves():
                state[possible_move] = player
                sim_score = self.minimax(state, other_player, alpha, beta)[0]
                state[possible_move] = ' '
                if sim_score > best[0]:
                    best = [sim_score, possible_move]
                alpha = max(alpha, sim_score)
                if beta <= alpha:
                    break
        else:
            best = [float('inf'), None]
            for possible_move in self.available_moves():
                state[possible_move] = player
                sim_score = self.minimax(state, max_player, alpha, beta)[0]
                state[possible_move] = ' '
                if sim_score < best[0]:
                    best = [sim_score, possible_move]
                beta = min(beta, sim_score)
                if beta <= alpha:
                    break
        return best
    
    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=self.board[i * 3 + j])

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.update_buttons()
        TicTacToe(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()