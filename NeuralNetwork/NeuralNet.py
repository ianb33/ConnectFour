import random

class Node:
    def __init__(self, node_type, value = None):
        self.node_type = node_type
        self.value = value
        self.children = []

    def addChild(self, child_node):
        self.children.append(child_node)

    def evaluate(self,  board_state):
        pass
    
    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, children={self.children})"
    
class NeuralNetworkController:
    
    def __init__(self):
        self.tree = []

    def generate_random_node(self, depth, max_depth, player_piece, opponent_piece):
        """
        Generates a random node for the decision tree.
        :param depth: Current depth of the tree
        :param max_depth: Maximum depth allowed for the tree
        :return: A randomly generated Node
        """
        from NeuralNetwork import MoveGenNodes, LogicalNodes

        if depth >= max_depth:
            # Base case: return an action or heuristic node
            action_type = random.choice(["GenerateMove", "ScoreMove"])
            column = random.randint(0, 6)  # Assuming a 7-column Connect Four board
            if action_type == "GenerateMove":
                return MoveGenNodes.GenerateMoveNode(column=column)
            else:
                weights = {
                    'maximize_connected_pieces': random.random(),
                    'minimize_opponent_threat': random.random(),
                    'center_column_preference': random.random(),
                    'avoid_full_columns': random.random()
                }
                return MoveGenNodes.ScoreMoveNode(player_piece, opponent_piece, weights)
        
        # Randomly decide node type
        node_type = random.choice(["IF", "AND", "OR", "NOT"])
        
        if node_type == "IF":
            node = LogicalNodes.IfThenElseNode()
            condition = random.choice(["Opponent can win in column", "I can win in column", "MaximizeConnectedPieces() > 3"])
            node.add_child(self.generate_condition_node(condition))
            node.add_child(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
            node.add_child(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "AND":
            node = LogicalNodes.AndNode()
            node.add_child(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
            node.add_child(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "OR":
            node = LogicalNodes.OrNode()
            node.add_child(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
            node.add_child(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "NOT":
            node = LogicalNodes.NotNode()
            node.add_child(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        return node

    def generate_condition_node(self, condition):
        """
        Generates a condition node based on the given condition string.
        :param condition: Condition string
        :return: A condition node
        """
        from NeuralNetwork import MoveGenNodes
        # Placeholder implementation for condition nodes
        # You can replace this with actual condition node implementations
        return MoveGenNodes.GenerateMoveNode(column=random.randint(0, 6))  # Placeholder
    

    
