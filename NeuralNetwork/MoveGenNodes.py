import random
from NeuralNetwork.NeuralNet import Node

class GenerateMoveNode(Node):
    def __init__(self):
        super().__init__(node_type="GenerateMove")
        self.column = 0
        greatest = 0
        for x in range(len(self.column_scores)):  
            if self.column_scores[x] > greatest:
                greatest = self.column_scores[x]
                self.column = x
        if greatest == 0:
            self.column = random.randint(0, 6)
            

    def evaluate(self, board):
        """Evaluates the move generation by returning the column for the move."""
        print(f"Placing a piece in column {self.column + 1}")
        return self.column  # Returns the column as the move choice

    def __repr__(self):
        return f"GenerateMoveNode(column={self.column})"

class ScoreBoard():
    def __init__(self, player_piece, opponent_piece, weights=None):
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
    
    def score_move(self, board_state, column, playerSymbol):
        return self.evaluate(board_state.SimulateMove(column, playerSymbol, board_state))

    def evaluate(self, board_state):
        # Combine the scores from different heuristics
        score = 0
        score += self.weights['maximize_connected_pieces'] * self.maximize_connected_pieces(board_state)
        score += self.weights['minimize_opponent_threat'] * self.minimize_opponent_threat(board_state)
        score += self.weights['center_column_preference'] * self.center_column_preference(board_state)
        score += self.weights['avoid_full_columns'] * self.avoid_full_columns(board_state)
        return score

    def maximize_connected_pieces(self, board):
        """Calculate a score based on how many AI pieces are connected."""
        # Call the MaximizeConnectedPiecesNode or use custom logic here
        max_connected = board.count_connected(board.getBoardState(), self.player_piece)
        return max_connected * 10  # Example score: 10 points per connected piece

    def minimize_opponent_threat(self, board):
        """Calculate a score based on blocking opponent's winning moves."""
        opponent_connected = board.count_connected(board.getBoardState(), self.opponent_piece)
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

    