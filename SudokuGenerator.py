import random
import numpy as np
import matplotlib.pyplot as plt

class SudokuGenerator:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.solution = np.zeros((9, 9), dtype=int)

    def is_valid(self, board, row, col, num):
        """Check if placing num at (row, col) is valid."""
        if num in board[row]:
            return False
        if num in board[:, col]:
            return False
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        if num in board[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True

    def find_empty_location(self, board):
        """Find an empty location in the board."""
        for row in range(9):
            for col in range(9):
                if board[row, col] == 0:
                    return row, col
        return None

    def solve_sudoku(self, board):
        """Solve the Sudoku using backtracking."""
        empty_loc = self.find_empty_location(board)
        if not empty_loc:
            return True  # Puzzle is solved
        
        row, col = empty_loc
        nums = list(range(1, 10))
        random.shuffle(nums)  # Randomize order for diversity

        for num in nums:
            if self.is_valid(board, row, col, num):
                board[row, col] = num
                if self.solve_sudoku(board):
                    return True
                board[row, col] = 0
        
        return False

    def generate_full_sudoku(self):
        """Generate a complete Sudoku solution."""
        self.solve_sudoku(self.board)
        self.solution = self.board.copy()

    def place_initial_numbers(self, num_initial):
        """Place a number of initial clues on the board."""
        board = np.zeros((9, 9), dtype=int)
        count = 0
        while count < num_initial:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row, col] == 0:
                num = random.randint(1, 9)
                if self.is_valid(board, row, col, num):
                    board[row, col] = num
                    count += 1
        return board

    def generate_sudoku(self, difficulty):
        """Generate a Sudoku puzzle with a given difficulty level."""
        num_initial = {
            'easy': 60,
            'medium': 50,
            'hard': 40,
            'extreme': 30,
        }.get(difficulty, 25)
        
        if num_initial < 17:
            num_initial = 17  # Ensure a valid number of clues for a unique solution

        self.board = self.place_initial_numbers(num_initial)
        self.generate_full_sudoku()  # Ensure the solution is generated
        return self.board

    def plot_board(self, board):
        """Plot the Sudoku board using Matplotlib."""
        fig, ax = plt.subplots(figsize=(6, 6))  # Size of the image
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 9)
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Draw grid lines
        for i in range(10):
            lw = 2 if i % 3 == 0 else 0.5
            ax.axhline(i, color='black', linewidth=lw)
            ax.axvline(i, color='black', linewidth=lw)
        
        # Fill numbers
        for row in range(9):
            for col in range(9):
                value = board[row, col]
                if value != 0:
                    ax.text(col + 0.5, 8.5 - row, str(value), ha='center', va='center', fontsize=20)
        
        plt.gca().invert_yaxis()
        plt.show()

def main():
    """Main function to interact with the user and generate Sudoku."""
    while True:
        difficulty = input("Choose difficulty (easy, medium, hard, extreme): ").strip().lower()
        if difficulty in ['easy', 'medium', 'hard', 'extreme']:
            break
        print("Invalid difficulty. Please choose between 'easy', 'medium', 'hard', or 'extreme'.")

    generator = SudokuGenerator()
    sudoku_board = generator.generate_sudoku(difficulty)

    print("\nGenerated Sudoku:")
    generator.plot_board(sudoku_board)

if __name__ == "__main__":
    main()