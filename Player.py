from abc import ABC, abstractmethod
import random

class Player(ABC):
    symbol = "X"; # Either X or O
    myPieces = 0

    @abstractmethod
    def getMove(self):
        pass
class Human(Player):
    def __init__(self, symbol):
        self.symbol = symbol
        self.myPieces = 0

    def getMove(self, player_number):
        return int(input(f"Player {player_number}, enter column (1-7): ")) - 1
        
class Computer(Player):

    def __init__(self, symbol):
        self.symbol = symbol
        self.myPieces = 0

    def getMove(self, playerNum):
        move = random.randint(1, 7)
        print("Player " + str(playerNum) + " placed their piece in column " + str(move))
        return move
        # Better algorithim to be added!!