"""Player base class and HumanPlayer implementation."""

from abc import ABC, abstractmethod
from utils import PLAYER_NAMES, parse_move, format_move


class Player(ABC):
    """Abstract base class for Hex players."""

    def __init__(self, color, name=None):
        self.color = color
        self.name = name or PLAYER_NAMES[color]

    @abstractmethod
    def get_move(self, board):
        """Return a (row, col) move for the given board state.

        Returns None if the player wants to quit.
        """
        pass

    def __str__(self):
        return self.name


class HumanPlayer(Player):
    """Human player with terminal input."""

    def __init__(self, color):
        super().__init__(color, f"Human ({PLAYER_NAMES[color]})")

    def get_move(self, board):
        """Prompt the human for a move via terminal input."""
        while True:
            try:
                text = input(f"\n{self.name} — enter move (e.g. A1) or 'quit': ").strip()
            except (EOFError, KeyboardInterrupt):
                return None

            if text.lower() == 'quit':
                return None

            move = parse_move(text, board.size)
            if move is None:
                print(f"  Invalid input. Use format like A1 (column letter + row number, 1-{board.size}).")
                continue

            r, c = move
            if board.grid[r][c] != 0:
                print(f"  Cell {format_move(r, c)} is already occupied. Try again.")
                continue

            return move
