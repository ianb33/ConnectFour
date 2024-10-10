import random
import io
import pickle
import plotly.express as px

class Node:
    def __init__(self, node_type, value = None):
        self.node_type = node_type
        self.value = value
        self.column_scores = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.children = []

    def addChild(self, child_node):
        self.children.append(child_node)

    def evaluate(self, board):
        raise NotImplementedError("This method should be implemented in the child classes")
    
    def get_column_scores(self):
        return self.column_scores
    
    def aggregate_child_scores(self, board):
        # Evaluate all child nodes and aggregate their scores
        for child in self.children:
            child.evaluate(board)
            for col in self.column_scores:
                self.column_scores[col] += child.column_scores[col]
        #Add some kind of return

    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value}, children={self.children})"
    
    

class NetworkGenerator:
    def create_debug_tree(self, player_piece, opponent_piece):
        from NeuralNetwork import MoveGenNodes, LogicalNodes

        root = LogicalNodes.IfThenElseNode()
        prevent_fork_node = LogicalNodes.PreventOpponentForkNode(opponent_piece, player_piece)
        generate_move_node = MoveGenNodes.GenerateMoveNode()
        create_fork_node = LogicalNodes.CreateForkNode(opponent_piece, player_piece)
        and_node = LogicalNodes.AndNode()
        or_node = LogicalNodes.OrNode()
        not_node = LogicalNodes.NotNode()
        maximize_connected_pieces_node = LogicalNodes.MaximizeConnectedPiecesNode(player_piece, opponent_piece)
        center_control_node = LogicalNodes.CenterControlNode(opponent_piece, player_piece)
        can_win_in_col = LogicalNodes.ICanWinInColumnNode(opponent_piece, player_piece)
        opp_can_win_in_col = LogicalNodes.OpponentCanWinInColumnNode(opponent_piece, player_piece)

        # Manually construct the tree to ensure all nodes are reachable
        root.addChild(can_win_in_col)
        root.addChild(and_node)
        root.addChild(or_node)

        and_node.addChild(prevent_fork_node)
        and_node.addChild(create_fork_node)

        or_node.addChild(not_node)
        or_node.addChild(maximize_connected_pieces_node)

        not_node.addChild(center_control_node)
        not_node.addChild(opp_can_win_in_col)

        prevent_fork_node.addChild(generate_move_node)
        create_fork_node.addChild(generate_move_node)
        maximize_connected_pieces_node.addChild(generate_move_node)
        center_control_node.addChild(generate_move_node)
        opp_can_win_in_col.addChild(generate_move_node)

        return root
    
    def generate_random_node(self, depth, max_depth, player_piece, opponent_piece):
        """
        Generates a random node for the decision tree.
        :param depth: Current depth of the tree
        :param max_depth: Maximum depth allowed for the tree
        :return: A randomly generated Node
        """
        from NeuralNetwork import MoveGenNodes, LogicalNodes
        if depth >= max_depth:
            return MoveGenNodes.GenerateMoveNode()
        
        # Randomly decide node type
        node_type = random.choice(["IF", "AND", "OR", "NOT", "MaximizeConnectedPieces", "CreateFork", "PreventOpponentFork", "CenterControl"])
        
        if node_type == "IF":
            node = LogicalNodes.IfThenElseNode()
            condition = random.choice(["OpponentCanWinInColumn", "ICanWinInColumn", "CanCreateFork", "CanPreventOpponentFork"])
            node.addChild(self.generate_condition_node(condition, player_piece, opponent_piece))
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "AND":
            node = LogicalNodes.AndNode()
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "OR":
            node = LogicalNodes.OrNode()
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "NOT":
            node = LogicalNodes.NotNode()
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "MaximizeConnectedPieces":
            node = LogicalNodes.MaximizeConnectedPiecesNode(player_piece, opponent_piece)
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "CreateFork":
            node = LogicalNodes.CreateForkNode(player_piece, opponent_piece)
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))

        elif node_type == "PreventOpponentFork":
            node = LogicalNodes.PreventOpponentForkNode(player_piece, opponent_piece)
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))
        
        elif node_type == "CenterControl":
            node = LogicalNodes.CenterControlNode(player_piece, opponent_piece)
            node.addChild(self.generate_random_node(depth + 1, max_depth, player_piece, opponent_piece))

        return node

    def generate_condition_node(self, condition, player_piece, opponent_piece):
        from NeuralNetwork import LogicalNodes, MoveGenNodes

        if condition == "OpponentCanWinInColumn":
            return LogicalNodes.OpponentCanWinInColumnNode(player_piece, opponent_piece)
        elif condition == "ICanWinInColumn":
            return LogicalNodes.ICanWinInColumnNode(player_piece, opponent_piece)
        elif condition == "MaximizeConnectedPieces":
            return LogicalNodes.MaximizeConnectedPiecesNode(player_piece, opponent_piece)
        elif condition == "CanCreateFork":
            return LogicalNodes.CreateForkNode(player_piece, opponent_piece)
        elif condition == "CanPreventOpponentFork":
            return LogicalNodes.PreventOpponentForkNode(player_piece, opponent_piece)
        return MoveGenNodes.GenerateMoveNode()
    
class NeuralNetworkController(NetworkGenerator):

    def __init__(self, player_piece, opponent_piece, board):
        # self.tree = self.generate_random_node(0, 10, player_piece, opponent_piece)
        self.tree = self.create_debug_tree(player_piece, opponent_piece) 
        self.column_scores = {}

    def save_tree(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.tree, f)  # Save the tree to a file
        print(f"Tree saved to {filename}")

    def load_tree(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.tree = pickle.load(f)  # Load the tree from the file
            print(f"Tree loaded from {filename}")
        except FileNotFoundError:
            print(f"Error: The file {filename} does not exist.")   

    def get_column_scores(self):
        self.column_scores = self.tree.column_scores
        return self.column_scores


    
