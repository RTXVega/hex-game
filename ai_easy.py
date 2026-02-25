"""Easy AI player: shallow minimax with simple evaluation."""

from player import Player
from minimax import minimax
from evaluation import eval_simple
from utils import PLAYER_NAMES


class EasyAI(Player):
    """Easy difficulty AI using depth-1 minimax with stone-count heuristic."""

    DEPTH = 1

    def __init__(self, color):
        super().__init__(color, f"Easy AI ({PLAYER_NAMES[color]})")

    def get_move(self, board):
        _, move = minimax(board, self.DEPTH, True, self.color, eval_simple)
        return move
