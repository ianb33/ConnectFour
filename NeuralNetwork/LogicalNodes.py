import NeuralNet

class LogicalNode(NeuralNet.Node):
    def __init__(self, logic_type):
        self.logic_type = logic_type  # The type of logical operation (IF, AND, OR, etc.)
        self.children = []  # List of child nodes

    def add_child(self, child_node):
        """Add a child node (operands or conditions)."""
        self.children.append(child_node)

    def evaluate(self, board_state):
        """To be implemented in subclasses, this method will evaluate the logic on the board state."""
        raise NotImplementedError("Subclasses should implement the 'evaluate' method.")

    def __repr__(self):
        return f"{self.logic_type}({', '.join([str(child) for child in self.children])})"
    
class IfThenElseNode(LogicalNode):
    def __init__(self):
        super().__init__(logic_type="IF-THEN-ELSE")

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
        
class AndNode(LogicalNode):
    def __init__(self):
        super().__init__(logic_type="AND")

    def evaluate(self, board_state):
        # Returns True if all children evaluate to True
        return all(child.evaluate(board_state) for child in self.children)
    
class OrNode(LogicalNode):
    def __init__(self):
        super().__init__(logic_type="OR")

    def evaluate(self, board_state):
        # Returns True if any child evaluates to True
        return any(child.evaluate(board_state) for child in self.children)
    
class NotNode(LogicalNode):
    def __init__(self):
        super().__init__(logic_type="NOT")

    def evaluate(self, board_state):
        # NOT logic only has one child, so negate the result of that child
        return not self.children[0].evaluate(board_state)
    
