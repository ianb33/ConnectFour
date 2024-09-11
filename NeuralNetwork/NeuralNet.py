import GameController

class Node:
    def __init__(self, node_type, value = None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def addChild(self, child_node):
        self.children.append(child_node)

    def evaluate(self, board_state):
        pass
    
    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, children={self.children})"
    
