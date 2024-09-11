import NeuralNet

class GenerateMoveNode(NeuralNet.Node):
    def __init__(self, column):
        super().__init__(node_type="GenerateMove")
        self.column = column  # Column where the move will be generated

    def evaluate(self, board_state):
        """Evaluates the move generation by returning the column for the move."""
        print(f"Placing a piece in column {self.column}")
        return self.column  # Returns the column as the move choice

    def __repr__(self):
        return f"GenerateMoveNode(column={self.column})"

class ScoreMoveNode(NeuralNet.Node):
    def __init__(self, column, type):
        super().__init__(node_type=type)
        self.column = column  # Column to evaluate

    def evaluate(self, board_state):
        """Evaluates the desirability of placing a piece in the specified column."""
        # Example: Return a score based on a heuristic evaluation of the column
        # In practice, this would analyze the board state, look for connections, etc.
        score = self.heuristic_score(board_state)
        print(f"Scoring move in column {self.column}: {score}")
        return score

    def heuristic_score(self, board_state):
        """A simple heuristic function that returns a score for this column.
        For example, we return a higher score if the move leads to a win or blocks the opponent."""
        # This is a dummy heuristic, replace with actual game logic
        # Example: Higher score if the move is near the center of the board
        center_column = len(board_state[0]) // 2
        return max(1, 10 - abs(self.column - center_column))  # Center columns are better

    def __repr__(self):
        return f"ScoreMoveNode(column={self.column})"
    
    def MaximizeConnectedPieces(self, board_state, player_symbol): # node_type = "MaximizeConnectedPieces"
        # Insert future implementation :)
        pass
    def MinimizeThreat(self, board_state, player_symbol): # node_type = "MinimizeThreat"
        # Insert future implementation :)
        pass
    def CanWinInColumn(self, column, board_state, player_symbol): # node_type = "CanWinInColumn"
        # Insert future implementation :)
        pass
    def ControlCenter(self, column, board_state, player_symbol): # node_type = "ControlCenter"
        # Insert future implementation :)
        pass