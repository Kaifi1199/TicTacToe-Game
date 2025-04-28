import tkinter as tk
from tkinter import messagebox


BOARD_SIZE = 3
EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")

        self.current_player = PLAYER_X
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        self.create_board_buttons()

    def create_board_buttons(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j] = tk.Button(self.root, text=EMPTY, font=('Arial', 20),
                                               width=4, height=2, command=lambda i=i, j=j: self.handle_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def handle_click(self, row, col):
        if self.board[row][col] == EMPTY:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Winner!", f"{self.current_player} wins!")
                self.reset_board()
            elif self.check_tie():
                messagebox.showinfo("Tie!", "It's a draw!")
                self.reset_board()
            else:
                self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
                if self.current_player == PLAYER_O:
                    self.ai_move()

    def check_winner(self, player):
        # Check rows, columns, and diagonals for winner
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == player for j in range(BOARD_SIZE)) or \
                    all(self.board[j][i] == player for j in range(BOARD_SIZE)):
                return True
        if all(self.board[i][i] == player for i in range(BOARD_SIZE)) or \
                all(self.board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
            return True
        return False

    def check_tie(self):
        for row in self.board:
            if EMPTY in row:
                return False
        return True

    def reset_board(self):
        self.current_player = PLAYER_X
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(text=EMPTY)

    def ai_move(self):
        best_score = float('-inf')
        best_move = None

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = PLAYER_O
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        row, col = best_move
        self.board[row][col] = PLAYER_O
        self.buttons[row][col].config(text=PLAYER_O)

        if self.check_winner(PLAYER_O):
            messagebox.showinfo("Winner!", f"{PLAYER_O} wins!")
            self.reset_board()
        elif self.check_tie():
            messagebox.showinfo("Tie!", "It's a tie!")
            self.reset_board()
        else:
            self.current_player = PLAYER_X

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(PLAYER_X):
            return -1
        elif self.check_winner(PLAYER_O):
            return 1
        elif self.check_tie():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER_O
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER_X
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = EMPTY
                        best_score = min(score, best_score)
            return best_score

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()