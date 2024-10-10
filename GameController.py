from UIController import UIController
import Player, os
from NeuralNetwork.NeuralNet import NeuralNetworkController
 
class Board:
    board_state = []

    def __init__(self):
        self.board_state = []

    def createNewBoard(self):
        self.board_state = [[" "]*7 for _ in range(6)]
        
    def saveBoard(self, newBoard):
        self.board_state 

    def isColFull(self, column):
        return bool(self.board_state[0][column - 1] != " ")
    
    def getBoard(self):
        return self
    
    def getBoardState(self):
        return self.board_state

    def printBoard(self):
        print("  1   2   3   4   5   6   7")
        print("+---+---+---+---+---+---+---+")
        for row in self.board_state:
            print("| " + " | ".join(row) + " |")
            print("+---+---+---+---+---+---+---+")

    def dropPiece(self, col, playerSymbol):
        if col < 0 or col >= len(self.board_state[0]):
            print("Invalid column")
            return False
        
        for row in range(len(self.board_state)-1, -1, -1):
            if self.board_state[row][col] == " ":
                self.board_state[row][col] = str(playerSymbol)
                return True
            
    def SimulateMove(self, col, playerSymbol, board_state):
        if col < 0 or col >= len(board_state[0]):
            print("Invalid column")
            return None
        
        # Create a copy of the board for simulation
        temp_board = [row[:] for row in board_state]  # Create a copy of the board
        for row in reversed(temp_board):
            if row[col] == ' ':
                row[col] = playerSymbol
                return temp_board
        
        print("Column is full")
        return temp_board
    
    def count_connected(self, board, piece, col=None):
        max_pieces = 0

        columns_to_check = range(len(board.getBoardState())) if col is None else [col]

        for col in columns_to_check:
            pieces = 0

            # Find the lowest non-empty row in the current column
            row = -1
            for r in range(len(board.getBoardState()) - 1, -1, -1):
                if board.getBoardState()[r][col] == piece:
                    row = r
                    break

            if row == -1:
                continue  # No pieces found in the column

            # Check horizontally (row)
            for x in range(len(board.getBoardState())):
                if board.getBoardState()[row][x] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0

            # Check vertically (column)
            pieces = 0
            for x in range(len(board.getBoardState())):
                if board.getBoardState()[x][col] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0

            # Major diagonal (top-left to bottom-right)
            pieces = 0
            i, j = row, col
            while i >= 0 and j >= 0:
                if board.getBoardState()[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i -= 1
                j -= 1

            i, j = row + 1, col + 1
            while i < len(board.getBoardState()) and j < len(board.getBoardState()):
                if board.getBoardState()[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i += 1
                j += 1

            # Minor diagonal (top-right to bottom-left)
            pieces = 0
            i, j = row, col
            while i >= 0 and j < len(board.getBoardState()[0]):
                if board.getBoardState()[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i -= 1
                j += 1

            i, j = row + 1, col - 1
            while i < len(board.getBoardState()) and j >= 0:
                if board.getBoardState()[i][j] == piece:
                    pieces += 1
                    max_pieces = max(max_pieces, pieces)
                else:
                    pieces = 0
                i += 1
                j -= 1

        return max_pieces  # Return the maximum number of connected pieces found
    
    
    def checkForWinner(self, board_state):
        def checkDirection(row, col, delta_row, delta_col):
            piece = board_state[row][col]
            if piece == " ":
                return None
            for i in range(1, 4):
                new_row = row + delta_row * i
                new_col = col + delta_col * i
                if new_row < 0 or new_row >= len(board_state) or new_col < 0 or new_col >= len(board_state[0]):
                    return None
                if board_state[new_row][new_col] != piece:
                    return None
            return piece

        for row in range(len(board_state)):
            for col in range(len(board_state)):
                winner = (
                    checkDirection(row, col, 1, 0) or
                    checkDirection(row, col, 0, 1) or
                    checkDirection(row, col, 1, 1) or
                    checkDirection(row, col, 1, -1)
                )
                if winner:
                    return winner
        return None
            

class GameController():
    board = Board()

    def __init__(self):
        self.board = Board()
        self.uiController = UIController()
        self.players = []

    def initPlayers(self, playerCount):
        self.players = []
        if(int(playerCount) == 1):
            p1 = Player.Human("X")
            p2 = Player.Computer("O", neural_net=NeuralNetworkController("O", "X", self.board))
            self.players.append(p1)
            self.players.append(p2)

        elif(int(playerCount) == 2):
            p1 = Player.Human("X")
            p2 = Player.Human("O")
            self.players.append(p1)
            self.players.append(p2)

        elif(int(playerCount) == 9):
            p1 = Player.Computer("X", neural_net=NeuralNetworkController("X", "O", self.board))
            p2 = Player.Computer("O", neural_net=NeuralNetworkController("O", "X", self.board))
            self.players.append(p1)
            self.players.append(p2)

        return self.players
    
    def getPlayers(self):
        return self.players

    def getSelection(self):
        selection = input("> ")
        self.uiController.clearConsole()
        return selection

    # Define the global variable
    current_player_index = 0

    # Example function to access and modify the global variable
    def get_current_player_index(self):
        return self.current_player_index

    def set_current_player_index(self, index):
        self.current_player_index = index

    def getBoard(self):
        return self.board

    def startGame(self):
        
        self.uiController.clearConsole()
        self.uiController.displayTitle()
        self.initPlayers(self.getSelection())
        self.board.createNewBoard()

        
if __name__ == "__main__":
    # Example usage
    game_controller = GameController()
    game_controller.startGame()

    players = game_controller.getPlayers()

    winner = None

    while winner is None:
        player_piece = players[game_controller.get_current_player_index()].symbol
        opponent_piece = ""

        if player_piece == "X":
            opponent_piece = "O"
        else: 
            opponent_piece = "X"

        print("Current Player: " + player_piece)
        print("Opponent Piece: " + opponent_piece)
        game_controller.board.printBoard()
        current_player = players[game_controller.get_current_player_index()]
        move = None
        if current_player.player_type == "Computer":
            move = current_player.getMove(game_controller.board)
        elif current_player.player_type == "Human":
            move = current_player.getMove(game_controller.get_current_player_index() + 1)

        if game_controller.board.dropPiece(move, current_player.symbol):
            current_player.myPieces += 1
            game_controller.uiController.clearConsole()

            winner = game_controller.board.checkForWinner(game_controller.board.getBoardState())
            print(f"Player {game_controller.get_current_player_index() + 1} has {current_player.myPieces} on the board")
            game_controller.set_current_player_index((game_controller.get_current_player_index() + 1) % len(players))
        else:
            print("Invalid move. Try again.")

    if winner:
        print(f"The winner is {winner}")
        game_controller.board.printBoard()
    