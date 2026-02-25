"""Hard AI player: alpha-beta pruning with advanced evaluation and move ordering."""

from player import Player
from minimax import alphabeta, order_moves_by_heuristic
from evaluation import eval_advanced
from utils import PLAYER_NAMES


class HardAI(Player):
    """Hard difficulty AI using depth-3 alpha-beta with advanced heuristic."""

    DEPTH = 3

    def __init__(self, color):
        super().__init__(color, f"Hard AI ({PLAYER_NAMES[color]})")

    def get_move(self, board):
        _, move = alphabeta(
            board, self.DEPTH,
            float('-inf'), float('inf'),
            True, self.color,
            eval_advanced, order_moves_by_heuristic
        )
        return move
