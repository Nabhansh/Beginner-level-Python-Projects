# ============================================================
# PROJECT 2: Tic-Tac-Toe (GUI) using Tkinter
# ============================================================

import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.build_ui()

    def build_ui(self):
        # Title
        title = tk.Label(self.root, text="Tic-Tac-Toe", font=("Arial", 24, "bold"), bg="#2C3E50", fg="white")
        title.pack(fill=tk.X, pady=(0, 5))

        # Score Frame
        score_frame = tk.Frame(self.root, bg="#34495E")
        score_frame.pack(fill=tk.X, padx=10, pady=5)
        self.score_label = tk.Label(score_frame, text="X: 0  |  O: 0  |  Draws: 0",
                                     font=("Arial", 13), bg="#34495E", fg="white")
        self.score_label.pack(pady=5)

        # Status Label
        self.status = tk.Label(self.root, text="Player X's Turn", font=("Arial", 14),
                                bg="#ECF0F1", fg="#2C3E50")
        self.status.pack(fill=tk.X, padx=10, pady=5)

        # Board Frame
        board_frame = tk.Frame(self.root, bg="#2C3E50")
        board_frame.pack(padx=20, pady=10)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_frame, text="", font=("Arial", 30, "bold"),
                            width=4, height=2, bg="#ECF0F1", fg="#2C3E50",
                            command=lambda i=i: self.click(i),
                            relief=tk.RAISED, bd=3)
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)
            self.buttons.append(btn)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#2C3E50")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="New Game", font=("Arial", 12), bg="#27AE60", fg="white",
                  command=self.reset_board, padx=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset Scores", font=("Arial", 12), bg="#E74C3C", fg="white",
                  command=self.reset_all, padx=10).pack(side=tk.LEFT, padx=5)

        self.root.configure(bg="#2C3E50")

    def click(self, idx):
        if self.board[idx] == "" and not self.game_over:
            self.board[idx] = self.current_player
            color = "#3498DB" if self.current_player == "X" else "#E74C3C"
            self.buttons[idx].config(text=self.current_player, fg=color, state=tk.DISABLED)
            winner = self.check_winner()
            if winner:
                self.game_over = True
                if winner == "Draw":
                    self.status.config(text="It's a Draw!", bg="#F39C12")
                    self.scores["Draws"] += 1
                else:
                    self.status.config(text=f"Player {winner} Wins! 🎉", bg="#27AE60", fg="white")
                    self.scores[winner] += 1
                    self.highlight_winner()
                self.update_scores()
                self.disable_all()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status.config(text=f"Player {self.current_player}'s Turn", bg="#ECF0F1", fg="#2C3E50")

    def check_winner(self):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != "":
                self.winning_combo = (a, b, c)
                return self.board[a]
        if "" not in self.board:
            return "Draw"
        return None

    def highlight_winner(self):
        for idx in self.winning_combo:
            self.buttons[idx].config(bg="#F1C40F")

    def disable_all(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def update_scores(self):
        self.score_label.config(text=f"X: {self.scores['X']}  |  O: {self.scores['O']}  |  Draws: {self.scores['Draws']}")

    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winning_combo = ()
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, bg="#ECF0F1")
        self.status.config(text="Player X's Turn", bg="#ECF0F1", fg="#2C3E50")

    def reset_all(self):
        self.scores = {"X": 0, "O": 0, "Draws": 0}
        self.update_scores()
        self.reset_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()
