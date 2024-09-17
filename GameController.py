from UIController import UIController
import Player, os
from NeuralNetwork import NeuralNet
 
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
        
        print("Column is full")
        return False
    
    def findPieces(self, direction, player, row, col):
        pieces = 0

        if direction == 'row':
            for x in self.board_state[row]:
                if x == player.symbol:
                    pieces += 1
            return pieces
        elif direction == 'col':
            for x in range(len(self.board_state)):
                if self.board_state[x][col] == player.symbol:
                    pieces += 1
            return pieces
        elif direction == 'diag':
            # Count the origin piece if it matches the player's symbol
            if self.board_state[row][col] == player.symbol:
                pieces += 1

            # Major diagonal (top-left to bottom-right)
            i, j = row - 1, col - 1
            while i >= 0 and j >= 0:
                if self.board_state[i][j] == player.symbol:
                    pieces += 1
                i -= 1
                j -= 1

            i, j = row + 1, col + 1
            while i < len(self.board_state) and j < len(self.board_state[0]):
                if self.board_state[i][j] == player.symbol:
                    pieces += 1
                i += 1
                j += 1

            # Minor diagonal (top-right to bottom-left)
            i, j = row - 1, col + 1
            while i >= 0 and j < len(self.board_state[0]):
                if self.board_state[i][j] == player.symbol:
                    pieces += 1
                i -= 1
                j += 1

            i, j = row + 1, col - 1
            while i < len(self.board_state) and j >= 0:
                if self.board_state[i][j] == player.symbol:
                    pieces += 1
                i += 1
                j -= 1

            return pieces

        return pieces  # Default return in case of invalid direction
            

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
            p2 = Player.Computer("O")
            self.players.append(p1)
            self.players.append(p2)

        elif(int(playerCount) == 2):
            p1 = Player.Human("X")
            p2 = Player.Human("O")
            self.players.append(p1)
            self.players.append(p2)

        return self.players
    
    def getPlayers(self):
        return self.players

    def checkForWinner(self):
        def checkDirection(row, col, delta_row, delta_col):
            piece = self.board.board_state[row][col]
            if piece == " ":
                return None
            for i in range(1, 4):
                new_row = row + delta_row * i
                new_col = col + delta_col * i
                if new_row < 0 or new_row >= len(self.board.board_state) or new_col < 0 or new_col >= len(self.board.board_state[0]):
                    return None
                if self.board.board_state[new_row][new_col] != piece:
                    return None
            return piece

        for row in range(len(self.board.board_state)):
            for col in range(len(self.board.board_state[0])):
                winner = (
                    checkDirection(row, col, 1, 0) or
                    checkDirection(row, col, 0, 1) or
                    checkDirection(row, col, 1, 1) or
                    checkDirection(row, col, 1, -1)
                )
                if winner:
                    return winner
        return None

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


    def startGame(self):
        
        self.uiController.clearConsole()
        self.uiController.displayTitle()
        players = self.initPlayers(self.getSelection())
        self.board.createNewBoard()

        

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
    move = current_player.getMove(game_controller.get_current_player_index() + 1)
    if game_controller.board.dropPiece(move, current_player.symbol):
        current_player.myPieces += 1
        game_controller.uiController.clearConsole()
        print(f"There is {game_controller.board.findPieces('row', current_player, 5, 1)} pieces of Player {current_player.symbol}'s in row 6")
        print(f"There is {game_controller.board.findPieces('col', current_player, 1, 3)} pieces of Player {current_player.symbol}'s in column 4")            
        print(f"There is {game_controller.board.findPieces('diag', current_player, 5, 0)} pieces of Player {current_player.symbol}'s diagonally")

        winner = game_controller.checkForWinner()
        print(f"Player {game_controller.get_current_player_index() + 1} has {current_player.myPieces} on the board")
        game_controller.set_current_player_index((game_controller.get_current_player_index() + 1) % len(players))
    else:
        print("Invalid move. Try again.")

if winner:
    print(f"The winner is {winner}")
    game_controller.board.printBoard()

# neural_net = NeuralNet.NeuralNetworkController()
# random_node = neural_net.generate_random_node(0, 3, player_piece, opponent_piece)
# print(random_node)