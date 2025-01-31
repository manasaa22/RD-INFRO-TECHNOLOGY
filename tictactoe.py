import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        
        # Initialize game variables
        self.board = [' ' for _ in range(9)]
        self.buttons = []
        self.game_active = False
        
        # Create symbol selection frame
        self.selection_frame = tk.Frame(self.window)
        self.selection_frame.pack(pady=10)
        
        tk.Label(self.selection_frame, text="Choose your symbol:").pack()
        
        # Symbol selection buttons
        self.x_button = tk.Button(self.selection_frame, text="X", width=10, 
                                command=lambda: self.start_game('X'))
        self.x_button.pack(side=tk.LEFT, padx=5)
        
        self.o_button = tk.Button(self.selection_frame, text="O", width=10,
                                command=lambda: self.start_game('O'))
        self.o_button.pack(side=tk.LEFT, padx=5)
        
        # Create game board frame
        self.game_frame = tk.Frame(self.window)
        self.game_frame.pack()
        
        # Create game board buttons
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.game_frame, text="", width=10, height=3,
                                 command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons.append(button)
                button['state'] = 'disabled'
        
        # Create reset button
        self.reset_button = tk.Button(self.window, text="Reset Game", 
                                    command=self.reset_game)
        self.reset_button.pack(pady=10)
        
    def start_game(self, human_symbol):
        """Initialize the game with the chosen symbol"""
        self.human = human_symbol
        self.ai = 'O' if human_symbol == 'X' else 'X'
        self.game_active = True
        
        # Enable game board buttons
        for button in self.buttons:
            button['state'] = 'normal'
            
        # Disable symbol selection
        self.x_button['state'] = 'disabled'
        self.o_button['state'] = 'disabled'
        
        # If AI goes first (human chose O), make AI move
        if self.human == 'O':
            self.make_ai_move()
    
    def make_move(self, row, col):
        """Handle human player's move"""
        if not self.game_active:
            return
            
        position = row * 3 + col
        if self.board[position] == ' ':
            self.board[position] = self.human
            self.buttons[position].config(text=self.human)
            
            if self.check_winner(self.human):
                messagebox.showinfo("Game Over", "You win!")
                self.game_active = False
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.game_active = False
            else:
                self.make_ai_move()
    
    def make_ai_move(self):
        """Make AI's move using minimax algorithm"""
        move = self.get_best_move()
        self.board[move] = self.ai
        self.buttons[move].config(text=self.ai)
        
        if self.check_winner(self.ai):
            messagebox.showinfo("Game Over", "AI wins!")
            self.game_active = False
        elif self.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.game_active = False
    
    def minimax(self, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        if self.check_winner(self.ai):
            return 1
        if self.check_winner(self.human):
            return -1
        if self.is_board_full():
            return 0
            
        if is_maximizing:
            max_eval = float('-inf')
            for move in self.get_available_moves():
                self.board[move] = self.ai
                eval = self.minimax(depth + 1, alpha, beta, False)
                self.board[move] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_available_moves():
                self.board[move] = self.human
                eval = self.minimax(depth + 1, alpha, beta, True)
                self.board[move] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_best_move(self):
        """Get the optimal move for the AI"""
        best_score = float('-inf')
        best_move = None
        
        for move in self.get_available_moves():
            self.board[move] = self.ai
            score = self.minimax(0, float('-inf'), float('inf'), False)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def get_available_moves(self):
        """Get list of empty positions"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def is_board_full(self):
        """Check if the board is full"""
        return ' ' not in self.board
    
    def check_winner(self, player):
        """Check if the given player has won"""
        # Check rows
        for i in range(0, 9, 3):
            if all(self.board[i+j] == player for j in range(3)):
                return True
        # Check columns
        for i in range(3):
            if all(self.board[i+j*3] == player for j in range(3)):
                return True
        # Check diagonals
        if all(self.board[i] == player for i in [0, 4, 8]):
            return True
        if all(self.board[i] == player for i in [2, 4, 6]):
            return True
        return False
    
    def reset_game(self):
        """Reset the game to initial state"""
        # Clear board
        self.board = [' ' for _ in range(9)]
        self.game_active = False
        
        # Reset buttons
        for button in self.buttons:
            button.config(text="")
            button['state'] = 'disabled'
        
        # Enable symbol selection
        self.x_button['state'] = 'normal'
        self.o_button['state'] = 'normal'
    
    def run(self):
        """Start the game window"""
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()