"""Constants and utility functions for Hex game."""

EMPTY = 0
RED = 1    # Connects top <-> bottom
BLUE = 2   # Connects left <-> right

PLAYER_NAMES = {RED: "Red", BLUE: "Blue"}
PLAYER_SYMBOLS = {EMPTY: ".", RED: "R", BLUE: "B"}


def opponent(player):
    """Return the opposing player."""
    return BLUE if player == RED else RED


def col_label(col):
    """Return letter label for a column index (0 -> 'A', 1 -> 'B', ...)."""
    return chr(ord('A') + col)


def parse_move(text, size):
    """Parse a move string like 'A1' or 'c5' into (row, col).

    Returns (row, col) tuple or None if invalid.
    """
    text = text.strip().upper()
    if len(text) < 2:
        return None
    col_char = text[0]
    row_str = text[1:]
    if not col_char.isalpha() or not row_str.isdigit():
        return None
    col = ord(col_char) - ord('A')
    row = int(row_str) - 1
    if 0 <= row < size and 0 <= col < size:
        return (row, col)
    return None


def format_move(row, col):
    """Format a (row, col) tuple into a move string like 'A1'."""
    return f"{col_label(col)}{row + 1}"
