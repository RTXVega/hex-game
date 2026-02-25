"""Medium AI player: deeper minimax with shortest-path evaluation."""

from player import Player
from minimax import minimax
from evaluation import eval_shortest_path
from utils import PLAYER_NAMES


class MediumAI(Player):
    """Medium difficulty AI using depth-2 minimax with Dijkstra path heuristic."""

    DEPTH = 2

    def __init__(self, color):
        super().__init__(color, f"Medium AI ({PLAYER_NAMES[color]})")

    def get_move(self, board):
        _, move = minimax(board, self.DEPTH, True, self.color, eval_shortest_path)
        return move
