from NeuralNetwork.NeuralNet import Node

class IfThenElseNode(Node):
    def __init__(self):
        super().__init__(node_type="IF-THEN-ELSE")
        
    def evaluate(self, board_state):
        # The first child is the condition, second is the THEN action, third is the ELSE action.
        condition = self.children[0]
        then_branch = self.children[1]
        else_branch = self.children[2]

        # Evaluate the condition (assumed to return a boolean)
        if condition.evaluate(board_state):
            return then_branch.evaluate(board_state)
        else:
            return else_branch.evaluate(board_state)
        
class AndNode(Node):
    def __init__(self):
        super().__init__(node_type="AND")

    def evaluate(self, board_state):
        # Returns True if all children evaluate to True
        return all(child.evaluate(board_state) for child in self.children)
    
class OrNode(Node):
    def __init__(self):
        super().__init__(node_type="OR")

    def evaluate(self, board_state):
        # Returns True if any child evaluates to True
        return any(child.evaluate(board_state) for child in self.children)
    
class NotNode(Node):
    def __init__(self):
        super().__init__(node_type="NOT")

    def evaluate(self, board_state):
        # NOT logic only has one child, so negate the result of that child
        return not self.children[0].evaluate(board_state)
    
class OpponentCanWinInColumnNode(Node):
    def __init__(self, opponent_piece, player_piece):
        self.opponent_piece = opponent_piece
        self.player_piece = player_piece
        super().__init__(node_type="Condition")

    def evaluate(self, board):
        for col in range(len(board.getBoardState())): 
            simBoard = board.SimulateMove(col, self.opponent_piece, board.getBoardState())
            if board.checkForWinner(self, simBoard) == self.opponent_piece:
                self.column_scores[col] += 10
                return True
            else:
                return False

class ICanWinInColumnNode(Node):
    def __init__(self, opponent_piece, player_piece):
        self.opponent_piece = opponent_piece
        self.player_piece = player_piece
        super().__init__(node_type="Condition")

    def evaluate(self, board):
        for col in range(len(board.getBoardState())):
            simBoard = board.SimulateMove(col, self.player_piece, board.getBoardState())
            if board.checkForWinner(simBoard) == self.player_piece:
                self.column_scores[col] += 15
                return True
            else:
                return False

class MaximizeConnectedPiecesNode(Node):
    def __init__(self, opponent_piece, player_piece):
        self.opponent_piece = opponent_piece
        self.player_piece = player_piece
        super().__init__(node_type="MaximizeConnectedPieces")
        

    def evaluate(self, board):
        for col in range(len(board.getBoardState()[0])):
            simBoard = board.SimulateMove(col, self.player_piece, board.getBoardState())
            connected_pieces = board.count_connected(simBoard, self.player_piece, col)
            self.column_scores[col] += connected_pieces
        self.aggregate_child_scores(board)

class CreateForkNode(Node):
    def __init__(self, opponent_piece, player_piece):
        self.opponent_piece = opponent_piece
        self.player_piece = player_piece
        super().__init__("CreateFork")

    def creates_fork(self, board, col):
        simBoard = board.SimulateMove(col, self.player_piece, board.getBoardState())
        if col > 0 and col < 6:
            testBoard1 = board.SimulateMove(col-1, self.player_piece, board.getBoardState())
            testBoard2 = board.SimulateMove(col, self.player_piece, board.getBoardState())
            testBoard3 = board.SimulateMove(col+1, self.player_piece, board.getBoardState())

            winner1 = board.checkForWinner(testBoard1)
            winner2 = board.checkForWinner(testBoard2)
            winner3 = board.checkForWinner(testBoard3)

            if winner1 == self.player_piece and (winner2 == self.player_piece or winner3 == self.player_piece):
                return True
            if winner2 == self.player_piece and winner3 == self.player_piece:
                return True
            return False
        elif col == 0:
            testBoard1 = board.SimulateMove(col, self.player_piece, board.getBoardState())
            testBoard2 = board.SimulateMove(col+1, self.player_piece, board.getBoardState())
            winner1 = board.checkForWinner(testBoard1)
            winner2 = board.checkForWinner(testBoard2)
            return winner1 == self.player_piece and winner1 == winner2
        elif col == 6:
            testBoard1 = board.SimulateMove(col, self.player_piece, board.getBoardState())
            testBoard2 = board.SimulateMove(col-1, self.player_piece, board.getBoardState())
            winner1 = board.checkForWinner(testBoard1)
            winner2 = board.checkForWinner(testBoard2)
            return winner1 == self.player_piece and winner1 == winner2
        return False
        
    def evaluate(self, board):
        for col in range(len(board.getBoardState()[0])):
            if self.creates_fork(board, col): 
                self.column_scores[col] += 15  # Higher score for creating a fork
        self.aggregate_child_scores(board)

class PreventOpponentForkNode(Node):
    def __init__(self, opponent_piece, player_piece):
        self.opponent_piece = opponent_piece
        self.player_piece = player_piece
        super().__init__("PreventOpponentFork")

    def opponent_creates_fork(self, board, col):
        simBoard = board.SimulateMove(col, self.opponent_piece, board.getBoardState())
        if col > 0 and col < 6:
            testBoard1 = board.SimulateMove(col-1, self.opponent_piece, board.getBoardState())
            testBoard2 = board.SimulateMove(col, self.opponent_piece, board.getBoardState())
            testBoard3 = board.SimulateMove(col+1, self.opponent_piece, board.getBoardState())

            winner1 = board.checkForWinner(testBoard1)
            winner2 = board.checkForWinner(testBoard2)
            winner3 = board.checkForWinner(testBoard3)

            if winner1 == self.opponent_piece and (winner2 == self.opponent_piece or winner3 == self.opponent_piece):
                return True
            if winner2 == self.opponent_piece and winner3 == self.opponent_piece:
                return True
            return False
        elif col == 0:
            testBoard1 = board.SimulateMove(col, self.opponent_piece, board.getBoardState())
            testBoard2 = board.SimulateMove(col+1, self.opponent_piece, board.getBoardState())
            winner1 = board.checkForWinner(testBoard1)
            winner2 = board.checkForWinner(testBoard2)
            return winner1 == self.opponent_piece and winner1 == winner2
        elif col == 6:
            testBoard1 = board.SimulateMove(col, self.opponent_piece, board.getBoardState())
            testBoard2 = board.SimulateMove(col-1, self.opponent_piece, board.getBoardState())
            winner1 = board.checkForWinner(testBoard1)
            winner2 = board.checkForWinner(testBoard2)
            return winner1 == self.opponent_piece and winner1 == winner2
        return False

    def evaluate(self, board):
        for col in range(len(board.getBoardState()[0])):
            if self.opponent_creates_fork(board, col):
                self.column_scores[col] += 12  # Score for blocking opponent fork
        self.aggregate_child_scores(board)

class CenterControlNode(Node):
    def __init__(self, opponent_piece, player_piece):
        self.opponent_piece = opponent_piece
        self.player_piece = player_piece
        super().__init__("CenterControl")

    def evaluate(self, board):
        center_col = len(board.getBoardState()[0]) // 2
        self.column_scores[center_col] += 5  # Assign a higher score to the center column
        self.aggregate_child_scores(board)