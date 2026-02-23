"""Hex board representation, move logic, win detection, and display."""

from collections import deque
from utils import EMPTY, RED, BLUE, PLAYER_SYMBOLS, col_label

# Six hex-grid neighbor offsets
NEIGHBOR_OFFSETS = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]


class HexBoard:
    """N x N Hex board."""

    def __init__(self, size=11):
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]

    def clone(self):
        """Return a deep copy of this board."""
        new = HexBoard(self.size)
        new.grid = [row[:] for row in self.grid]
        return new

    def in_bounds(self, row, col):
        """Check if (row, col) is within the board."""
        return 0 <= row < self.size and 0 <= col < self.size

    def get_neighbors(self, row, col):
        """Return list of valid neighbor coordinates for a hex cell."""
        neighbors = []
        for dr, dc in NEIGHBOR_OFFSETS:
            r, c = row + dr, col + dc
            if self.in_bounds(r, c):
                neighbors.append((r, c))
        return neighbors

    def place(self, row, col, player):
        """Place a stone. Returns True if successful, False if cell is occupied."""
        if not self.in_bounds(row, col):
            return False
        if self.grid[row][col] != EMPTY:
            return False
        self.grid[row][col] = player
        return True

    def get_empty_cells(self):
        """Return list of all empty (row, col) positions."""
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == EMPTY:
                    cells.append((r, c))
        return cells

    def check_win(self, player):
        """Check if player has a connected path between their two sides using BFS.

        RED connects top (row 0) to bottom (row size-1).
        BLUE connects left (col 0) to right (col size-1).
        """
        visited = set()
        queue = deque()

        # Seed BFS from the starting side
        if player == RED:
            for c in range(self.size):
                if self.grid[0][c] == player:
                    queue.append((0, c))
                    visited.add((0, c))
        else:  # BLUE
            for r in range(self.size):
                if self.grid[r][0] == player:
                    queue.append((r, 0))
                    visited.add((r, 0))

        while queue:
            row, col = queue.popleft()
            # Check if we reached the target side
            if player == RED and row == self.size - 1:
                return True
            if player == BLUE and col == self.size - 1:
                return True
            for nr, nc in self.get_neighbors(row, col):
                if (nr, nc) not in visited and self.grid[nr][nc] == player:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return False

    def display(self):
        """Print an ASCII representation of the hex board.

        Layout with offset indentation to show hex connectivity:
           A  B  C  ...
        1   R  .  B  ...
         2   .  R  .  ...
          3   .  .  .  ...
        """
        n = self.size
        # Column header
        header = "   " + "  ".join(col_label(c) for c in range(n))
        print(header)

        for r in range(n):
            indent = " " * r
            row_label = f"{r + 1:>2}"
            cells = "  ".join(PLAYER_SYMBOLS[self.grid[r][c]] for c in range(n))
            print(f"{indent}{row_label}  {cells}")

        # Legend
        print(f"\n  Red (R): top <-> bottom  |  Blue (B): left <-> right")
