from UIController import UIController
import Player, os
class Board:
    __board = []

    def __init__(self):
        self.__board = []

    def createNewBoard(self):
        self.__board = [[" "]*7 for _ in range(6)]
        
    def saveBoard(self, newBoard):
        self.__board 

    def isColFull(self, column):
        return bool(self.__board[0][column - 1] != " ")
    
    def printBoard(self):
        print("  1   2   3   4   5   6   7")
        print("+---+---+---+---+---+---+---+")
        for row in self.__board:
            print("| " + " | ".join(row) + " |")
            print("+---+---+---+---+---+---+---+")

    def dropPiece(self, col, playerSymbol):
        if col < 0 or col >= len(self.__board[0]):
            print("Invalid column")
            return False
        
        for row in range(len(self.__board)-1, -1, -1):
            if self.__board[row][col] == " ":
                self.__board[row][col] = str(playerSymbol)
                return True
        
        print("Column is full")
        return False
    
    def SimulatePieceDrop(self, col, playerSymbol):
        if col < 0 or col >= len(self.__board[0]):
            print("Invalid column")
            return None
        
        # Create a copy of the board for simulation
        simulated_board = [row[:] for row in self.__board]
        
        for row in range(len(simulated_board)-1, -1, -1):
            if simulated_board[row][col] == " ":
                simulated_board[row][col] = str(playerSymbol)
                return simulated_board
        
        print("Column is full")
        return None
    
    def findPieces(self, direction, player, row, col):
        pieces = 0

        if direction == 'row':
            for x in self.__board[row]:
                if x == player.symbol:
                    pieces += 1
            return pieces
        elif direction == 'col':
            for x in range(len(self.__board)):
                if self.__board[x][col] == player.symbol:
                    pieces += 1
            return pieces
        elif direction == 'diag':
            # Count the origin piece if it matches the player's symbol
            if self.__board[row][col] == player.symbol:
                pieces += 1

            # Major diagonal (top-left to bottom-right)
            i, j = row - 1, col - 1
            while i >= 0 and j >= 0:
                if self.__board[i][j] == player.symbol:
                    pieces += 1
                i -= 1
                j -= 1

            i, j = row + 1, col + 1
            while i < len(self.__board) and j < len(self.__board[0]):
                if self.__board[i][j] == player.symbol:
                    pieces += 1
                i += 1
                j += 1

            # Minor diagonal (top-right to bottom-left)
            i, j = row - 1, col + 1
            while i >= 0 and j < len(self.__board[0]):
                if self.__board[i][j] == player.symbol:
                    pieces += 1
                i -= 1
                j += 1

            i, j = row + 1, col - 1
            while i < len(self.__board) and j >= 0:
                if self.__board[i][j] == player.symbol:
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

    def initPlayers(self, playerCount):
        players = []
        if(int(playerCount) == 1):
            p1 = Player.Human("X")
            p2 = Player.Computer("O")
            players.append(p1)
            players.append(p2)

        elif(int(playerCount) == 2):
            p1 = Player.Human("X")
            p2 = Player.Human("O")
            players.append(p1)
            players.append(p2)

        return players
    
    def checkForWinner(self):
        def checkDirection(row, col, delta_row, delta_col):
            piece = self.board._Board__board[row][col]
            if piece == " ":
                return None
            for i in range(1, 4):
                new_row = row + delta_row * i
                new_col = col + delta_col * i
                if new_row < 0 or new_row >= len(self.board._Board__board) or new_col < 0 or new_col >= len(self.board._Board__board[0]):
                    return None
                if self.board._Board__board[new_row][new_col] != piece:
                    return None
            return piece

        for row in range(len(self.board._Board__board)):
            for col in range(len(self.board._Board__board[0])):
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

        winner = None

        while winner is None:
            self.board.printBoard()
            current_player = players[self.get_current_player_index()]
            move = current_player.getMove(self.get_current_player_index() + 1)
            if self.board.dropPiece(move, current_player.symbol):
                current_player.myPieces += 1
                self.uiController.clearConsole()
                print(f"There is {self.board.findPieces('row', current_player, 5, 1)} pieces of Player {current_player.symbol}'s in row 6")
                print(f"There is {self.board.findPieces('col', current_player, 1, 3)} pieces of Player {current_player.symbol}'s in column 4")
                print(f"There is {self.board.findPieces('diag', current_player, 5, 0)} pieces of Player {current_player.symbol}'s diagonally")

                winner = self.checkForWinner()
                print(f"Player {self.get_current_player_index() + 1} has {current_player.myPieces} on the board")
                self.set_current_player_index((self.get_current_player_index() + 1) % len(players))
                

            else:
                print("Invalid move. Try again.")

        if winner:
            print(f"The winner is {winner}")
            self.board.printBoard()

# Example usage
game_controller = GameController()
game_controller.startGame()
print("Game has finished.")