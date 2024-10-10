from abc import ABC, abstractmethod
import random
from NeuralNetwork.NeuralNet import NeuralNetworkController

class Player(ABC):
    symbol = "X"; # Either X or O
    myPieces = 0

    @abstractmethod
    def getMove(self):
        pass
class Human(Player):
    def __init__(self, symbol):
        self.player_type = "Human"
        self.symbol = symbol
        self.myPieces = 0

    def getMove(self, player_number):
        while True:
            try:
                move = int(input(f"Player {player_number}, enter column (1-7): "))
                if 1 <= move <= 7:
                    return move - 1
                else:
                    print("Invalid input. Please enter a number between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        
class Computer(Player):

    def __init__(self,symbol, neural_net):
        self.player_type = "Computer"
        self.symbol = symbol
        self.myPieces = 0
        self.neural_net = neural_net

    def getMove(self, board):
        # neural_net.load_tree("debugTree")
        self.neural_net.graph_tree()
        self.neural_net.tree.aggregate_child_scores(board)