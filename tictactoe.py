import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        self.game_active = False
        
        self.choice_frame = tk.Frame(self.window)
        self.choice_frame.pack(pady=10)
        
        tk.Label(self.choice_frame, text="Choose your symbol:").pack()
        
        self.x_button = tk.Button(self.choice_frame, text="X", width=10, 
                                command=lambda: self.start_game('X'))
        self.x_button.pack(side=tk.LEFT, padx=5)
        
        self.o_button = tk.Button(self.choice_frame, text="O", width=10,
                                command=lambda: self.start_game('O'))
        self.o_button.pack(side=tk.LEFT, padx=5)
        
        self.game_frame = tk.Frame(self.window)
        self.game_frame.pack()
        
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="", width=10, height=3,
                                 command=lambda row=i, col=j: self.player_move(row, col))
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons.append(button)
                button['state'] = 'disabled'
        
        self.reset_button = tk.Button(self.window, text="Reset Game", 
                                    command=self.reset)
        self.reset_button.pack(pady=10)
        
    def start_game(self, player_symbol):
        self.player = player_symbol
        self.computer = 'O' if player_symbol == 'X' else 'X'
        self.game_active = True
        
        for button in self.buttons:
            button['state'] = 'normal'
            
        self.x_button['state'] = 'disabled'
        self.o_button['state'] = 'disabled'
        
        if self.player == 'O':
            self.computer_move()
    
    def player_move(self, row, col):
        if not self.game_active:
            return
            
        pos = row * 3 + col
        if self.board[pos] == ' ':
            self.board[pos] = self.player
            self.buttons[pos].config(text=self.player)
            
            if self.check_win(self.player):
                messagebox.showinfo("Game Over", "You win!")
                self.game_active = False
            elif self.is_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.game_active = False
            else:
                self.computer_move()
    
    def computer_move(self):
        move = self.find_best_move()
        self.board[move] = self.computer
        self.buttons[move].config(text=self.computer)
        
        if self.check_win(self.computer):
            messagebox.showinfo("Game Over", "Computer wins!")
            self.game_active = False
        elif self.is_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.game_active = False
    
    def minimax(self, depth, alpha, beta, is_max):
        if self.check_win(self.computer):
            return 1
        if self.check_win(self.player):
            return -1
        if self.is_full():
            return 0
            
        if is_max:
            best = float('-inf')
            for move in self.empty_squares():
                self.board[move] = self.computer
                score = self.minimax(depth + 1, alpha, beta, False)
                self.board[move] = ' '
                best = max(best, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best
        else:
            best = float('inf')
            for move in self.empty_squares():
                self.board[move] = self.player
                score = self.minimax(depth + 1, alpha, beta, True)
                self.board[move] = ' '
                best = min(best, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best
    
    def find_best_move(self):
        best_score = float('-inf')
        best_move = 0
        
        for move in self.empty_squares():
            self.board[move] = self.computer
            score = self.minimax(0, float('-inf'), float('inf'), False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def empty_squares(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def is_full(self):
        return ' ' not in self.board
    
    def check_win(self, mark):
        for i in range(0, 9, 3):
            if all(self.board[i+j] == mark for j in range(3)):
                return True
        for i in range(3):
            if all(self.board[i+j*3] == mark for j in range(3)):
                return True
        if all(self.board[i] == mark for i in [0, 4, 8]):
            return True
        if all(self.board[i] == mark for i in [2, 4, 6]):
            return True
        return False
    
    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.game_active = False
        
        for button in self.buttons:
            button.config(text="")
            button['state'] = 'disabled'
        
        self.x_button['state'] = 'normal'
        self.o_button['state'] = 'normal'
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()