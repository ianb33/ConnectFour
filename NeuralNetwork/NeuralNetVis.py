import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import random
import graphviz

# Initialize the Dash app
app = dash.Dash(__name__)

# Constants for Connect Four game
ROWS = 6
COLS = 7

# Create an empty board
board = [[" "]*7 for _ in range(6)]

# Column scores (initially all 0)
column_scores = {i: 0 for i in range(COLS)}

game_controller = None

def ai_move(game_controller):
    if game_controller != None:
        player = (game_controller.getPlayers())[game_controller.get_current_player_index()]
        move = player.getMove(game_controller.getBoard())
        column_scores = player.neural_net.get_column_scores()
        return move, column_scores
    else:
        raise Exception("Game Controller not initialized")


# Dash layout with a graph for the Connect Four board and a bar chart for column scores
app.layout = html.Div([
    html.H1("Connect Four AI Decision Tracker"),
    
    dcc.Graph(id="connect-four-board"),
    
    dcc.Graph(id="column-scores"),
    
    html.Button("AI Move", id="ai-move-button", n_clicks=0),  # Button to trigger AI move
    
    dcc.Interval(id="interval-component", interval=1000, n_intervals=0)  # Update interval for real-time changes
])

@app.callback(
    Output("connect-four-board", "figure"),
    [Input("ai-move-button", "n_clicks")]
)
def update_board(self, n_clicks, board):
    board_fig = go.Figure()
    self.board = board
    # Plotting circles for each piece (1 for AI, 0 for empty slots)
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == "X":
                board_fig.add_shape(
                    go.layout.Shape(
                        type="circle",
                        x0=col, y0=ROWS - row - 1, x1=col + 1, y1=ROWS - row,
                        line_color="red", fillcolor="red"
                    )
                )
            elif board[row][col] == "O":
                board_fig.add_shape(
                    go.layout.Shape(
                        type="circle",
                        x0=col, y0=ROWS - row - 1, x1=col + 1, y1=ROWS - row,
                        line_color="yellow", fillcolor="yellow"
                    )
                )
            else:  # Empty spot
                board_fig.add_shape(
                    go.layout.Shape(
                        type="circle",
                        x0=col, y0=ROWS - row - 1, x1=col + 1, y1=ROWS - row,
                        line_color="lightgray"
                    )
                )

    # Set grid for the board
    board_fig.update_layout(
        xaxis=dict(range=[0, COLS], zeroline=False, showgrid=False),
        yaxis=dict(range=[0, ROWS], zeroline=False, showgrid=False),
        height=600, width=600,
        shapes=[],  # Reset the shapes in every update
    )
    # Trigger AI move after button press
    if n_clicks > 0:
        ai_move(game_controller)  # Update the board and scores

    return board_fig

# Update the column scores bar chart
@app.callback(
    Output("column-scores", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_column_scores(n_intervals):
    # Bar chart for column scores
    fig = go.Figure([go.Bar(x=list(column_scores.keys()), y=list(column_scores.values()))])

    fig.update_layout(
        title="Column Scores",
        xaxis_title="Columns",
        yaxis_title="Score",
        yaxis=dict(range=[0, max(column_scores.values()) + 1])
    )

    return fig

def set_game_controller(self, game_controller):
    self.game_controller = game_controller

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)

def graph_tree(tree):
        dot = graphviz.Digraph()

        # Recursive function to add nodes and edges to the graph
        def add_nodes_edges(node, parent=None):
            node_label = f"{node.node_type}"
            dot.node(node_label)  # Add the current node

            if node_label == "IF":
                dot.node(f"{node.children[0].node_type}")
                add_nodes_edges(node.children[1], node.children[0].node_type)

            if parent:
                dot.edge(parent, node_label)  # Add edge from parent to this node

            for child in node.children:
                add_nodes_edges(child, node_label)  # Recursively add children

        add_nodes_edges(tree)

        dot.render('decision_tree', format='png')
