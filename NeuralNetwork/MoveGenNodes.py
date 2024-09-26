import random
from NeuralNetwork.NeuralNet import Node

class GenerateMoveNode(Node):
    def __init__(self, column):
        super().__init__(node_type="GenerateMove")
        self.column = column  # Column where the move will be generated

    def evaluate(self, board_state):
        """Evaluates the move generation by returning the column for the move."""
        print(f"Placing a piece in column {self.column}")
        return self.column  # Returns the column as the move choice

    def __repr__(self):
        return f"GenerateMoveNode(column={self.column})"

class ScoreMoveNode(Node):
    def __init__(self, player_piece, opponent_piece, weights=None):
        super().__init__(node_type="ScoreMove")
        self.player_piece = player_piece
        self.opponent_piece = opponent_piece
        self.weights = weights if weights else {
            'maximize_connected_pieces': 1.0,
            'minimize_opponent_threat': 0.8,
            'center_column_preference': 0.5,
            'avoid_full_columns': 0.3
        }

    def set_weight(self, key, value):
        if key in self.weights:
            self.weights[key] = value
        else:
            raise KeyError(f"Weight '{key}' not found in weights dictionary.")

    def randomize_weights(self):
        for key in self.weights:
            self.weights[key] = random.uniform(0, 1)

    def print_weights(self):
        for key, value in self.weights.items():
            print(f"{key}: {value}")

    def SimulateMove(self, col, playerSymbol, board_state):
        if col < 0 or col >= len(board_state[0]):
            print("Invalid column")
            return None
        
        # Create a copy of the board for simulation
        temp_board = [row[:] for row in board_state]  # Create a copy of the board
        for row in reversed(temp_board):
            if row[col] == ' ':
                row[col] = playerSymbol
                break
            else:
                print("Column is full")
                return None
    
    def score_move(self, board_state, column, playerSymbol):
        return self.evaluate(self.SimulateMove(column, playerSymbol, board_state))

    def evaluate(self, board_state):
        # Combine the scores from different heuristics
        score = 0
        score += self.weights['maximize_connected_pieces'] * self.maximize_connected_pieces(board_state)
        score += self.weights['minimize_opponent_threat'] * self.minimize_opponent_threat(board_state)
        score += self.weights['center_column_preference'] * self.center_column_preference(board_state)
        score += self.weights['avoid_full_columns'] * self.avoid_full_columns(board_state)
        return score

    def maximize_connected_pieces(self, board_state):
        """Calculate a score based on how many AI pieces are connected."""
        # Call the MaximizeConnectedPiecesNode or use custom logic here
        max_connected = self.count_connected(board_state, self.player_piece)
        return max_connected * 10  # Example score: 10 points per connected piece

    def minimize_opponent_threat(self, board_state):
        """Calculate a score based on blocking opponent's winning moves."""
        opponent_connected = self.count_connected(board_state, self.opponent_piece)
        return (4 - opponent_connected) * 5  # Penalize for allowing opponent connections

    def center_column_preference(self, board_state, column=0):
        """Give preference to center columns, which allow more connections."""
        center_column = len(board_state[0]) // 2
        return max(0, 10 - abs(column - center_column))  # Higher score closer to the center

    def avoid_full_columns(self, board_state):
        """Penalize moves in columns that are full or nearly full."""
        score = 0
        for x in range(len(board_state[0])):
            if board_state[0][x] is not None:  # If top row is full, penalize
                score -= 100  # Large penalty for full columns
        return score  # No penalty if the column is not full

    def count_connected(self, board_state, piece):
        max_pieces = 0
    
        for col in range(len(board_state[0])):
            pieces = 0
    
            # Find the lowest non-empty row in the current column
            row = -1
            for r in range(len(board_state) - 1, -1, -1):
                if board_state[r][col] == piece:
                    row = r
                    break
    
            if row == -1:
                continue  # No pieces found in the column
    
            # Check horizontally (row)
            for x in range(len(board_state[row])):
                if board_state[row][x] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
    
            # Check vertically (column)
            pieces = 0
            for x in range(len(board_state)):
                if board_state[x][col] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
    
            # Major diagonal (top-left to bottom-right)
            pieces = 0
            i, j = row, col
            while i >= 0 and j >= 0:
                if board_state[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i -= 1
                j -= 1
    
            i, j = row + 1, col + 1
            while i < len(board_state) and j < len(board_state[0]):
                if board_state[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i += 1
                j += 1
    
            # Minor diagonal (top-right to bottom-left)
            pieces = 0
            i, j = row, col
            while i >= 0 and j < len(board_state[0]):
                if board_state[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i -= 1
                j += 1
    
            i, j = row + 1, col - 1
            while i < len(board_state) and j >= 0:
                if board_state[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i += 1
                j -= 1
    
        return max_pieces  # Return the maximum number of connected pieces found across all columns