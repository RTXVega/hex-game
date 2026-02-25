"""Minimax and Alpha-Beta search algorithms for Hex."""

from utils import RED, BLUE, opponent
from evaluation import _shortest_path_cost


def minimax(board, depth, maximizing, player, eval_fn):
    """Plain Minimax search.

    Args:
        board: HexBoard instance
        depth: remaining search depth
        maximizing: True if current turn is the maximizing player
        player: the AI's color (the maximizing player)
        eval_fn: evaluation function(board, player) -> score

    Returns:
        (score, move) where move is (row, col) or None
    """
    opp = opponent(player)
    current = player if maximizing else opp

    # Terminal checks
    if board.check_win(player):
        return (1000 + depth, None)
    if board.check_win(opp):
        return (-1000 - depth, None)
    if depth == 0:
        return (eval_fn(board, player), None)

    empty = board.get_empty_cells()
    if not empty:
        return (eval_fn(board, player), None)

    best_move = None

    if maximizing:
        best_score = float('-inf')
        for (r, c) in empty:
            child = board.clone()
            child.place(r, c, current)
            score, _ = minimax(child, depth - 1, False, player, eval_fn)
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return (best_score, best_move)
    else:
        best_score = float('inf')
        for (r, c) in empty:
            child = board.clone()
            child.place(r, c, current)
            score, _ = minimax(child, depth - 1, True, player, eval_fn)
            if score < best_score:
                best_score = score
                best_move = (r, c)
        return (best_score, best_move)


def alphabeta(board, depth, alpha, beta, maximizing, player, eval_fn, move_order_fn=None):
    """Alpha-Beta pruning search.

    Args:
        board: HexBoard instance
        depth: remaining search depth
        alpha: alpha bound
        beta: beta bound
        maximizing: True if current turn is the maximizing player
        player: the AI's color (the maximizing player)
        eval_fn: evaluation function(board, player) -> score
        move_order_fn: optional function(board, moves, player) -> sorted moves

    Returns:
        (score, move) where move is (row, col) or None
    """
    opp = opponent(player)
    current = player if maximizing else opp

    # Terminal checks
    if board.check_win(player):
        return (1000 + depth, None)
    if board.check_win(opp):
        return (-1000 - depth, None)
    if depth == 0:
        return (eval_fn(board, player), None)

    empty = board.get_empty_cells()
    if not empty:
        return (eval_fn(board, player), None)

    # Apply move ordering if provided
    if move_order_fn is not None:
        empty = move_order_fn(board, empty, player)

    best_move = None

    if maximizing:
        best_score = float('-inf')
        for (r, c) in empty:
            child = board.clone()
            child.place(r, c, current)
            score, _ = alphabeta(child, depth - 1, alpha, beta, False, player, eval_fn, move_order_fn)
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return (best_score, best_move)
    else:
        best_score = float('inf')
        for (r, c) in empty:
            child = board.clone()
            child.place(r, c, current)
            score, _ = alphabeta(child, depth - 1, alpha, beta, True, player, eval_fn, move_order_fn)
            if score < best_score:
                best_score = score
                best_move = (r, c)
            beta = min(beta, best_score)
            if alpha >= beta:
                break
        return (best_score, best_move)


def order_moves_by_heuristic(board, moves, player):
    """Order moves by center proximity and path cost reduction.

    Moves closer to center and that reduce the player's shortest path
    cost are ranked first.
    """
    center = board.size / 2.0

    def score(move):
        r, c = move
        # Center distance (lower is better)
        center_dist = abs(r - center) + abs(c - center)
        # Quick path cost check: simulate placing the stone
        child = board.clone()
        child.place(r, c, player)
        path_cost = _shortest_path_cost(child, player)
        # Lower path cost and center distance = better move
        return path_cost + center_dist * 0.1

    return sorted(moves, key=score)
