"""Evaluation heuristics for Hex AI players."""

import heapq
import random
from utils import RED, BLUE, opponent


def eval_simple(board, player):
    """Simple evaluation: stone count difference + small random noise.

    Used by Easy AI. Positive = good for player.
    """
    opp = opponent(player)
    my_stones = 0
    opp_stones = 0
    for r in range(board.size):
        for c in range(board.size):
            if board.grid[r][c] == player:
                my_stones += 1
            elif board.grid[r][c] == opp:
                opp_stones += 1
    return (my_stones - opp_stones) + random.uniform(-0.5, 0.5)


def _shortest_path_cost(board, player):
    """Dijkstra shortest path cost for player to connect their two sides.

    Cost: own stone = 0, empty cell = 1, opponent stone = impassable.
    Returns the minimum number of empty cells needed to complete a path.
    Returns float('inf') if no path exists (fully blocked).
    """
    n = board.size
    opp = opponent(player)
    INF = float('inf')

    dist = [[INF] * n for _ in range(n)]
    heap = []

    # Seed from starting side
    if player == RED:
        # RED connects top (row 0) to bottom (row n-1)
        for c in range(n):
            if board.grid[0][c] == opp:
                continue
            cost = 0 if board.grid[0][c] == player else 1
            if cost < dist[0][c]:
                dist[0][c] = cost
                heapq.heappush(heap, (cost, 0, c))
    else:
        # BLUE connects left (col 0) to right (col n-1)
        for r in range(n):
            if board.grid[r][0] == opp:
                continue
            cost = 0 if board.grid[r][0] == player else 1
            if cost < dist[r][0]:
                dist[r][0] = cost
                heapq.heappush(heap, (cost, r, 0))

    while heap:
        d, r, c = heapq.heappop(heap)
        if d > dist[r][c]:
            continue
        # Check if we reached the target side
        if player == RED and r == n - 1:
            return d
        if player == BLUE and c == n - 1:
            return d
        for nr, nc in board.get_neighbors(r, c):
            if board.grid[nr][nc] == opp:
                continue
            nd = d + (0 if board.grid[nr][nc] == player else 1)
            if nd < dist[nr][nc]:
                dist[nr][nc] = nd
                heapq.heappush(heap, (nd, nr, nc))

    return INF


def eval_shortest_path(board, player):
    """Shortest-path evaluation: opponent's path cost minus player's.

    Positive = good for player. Used by Medium AI.
    """
    opp = opponent(player)
    my_cost = _shortest_path_cost(board, player)
    opp_cost = _shortest_path_cost(board, opp)
    return opp_cost - my_cost


def _count_connected_to_start(board, player):
    """Count player stones connected to their starting side via own stones."""
    from collections import deque
    n = board.size
    visited = set()
    queue = deque()

    if player == RED:
        for c in range(n):
            if board.grid[0][c] == player and (0, c) not in visited:
                visited.add((0, c))
                queue.append((0, c))
    else:
        for r in range(n):
            if board.grid[r][0] == player and (r, 0) not in visited:
                visited.add((r, 0))
                queue.append((r, 0))

    while queue:
        r, c = queue.popleft()
        for nr, nc in board.get_neighbors(r, c):
            if (nr, nc) not in visited and board.grid[nr][nc] == player:
                visited.add((nr, nc))
                queue.append((nr, nc))

    return len(visited)


def eval_advanced(board, player):
    """Advanced evaluation: Dijkstra path + connectivity bonus.

    Combines shortest-path difference with a bonus for stones connected
    to the starting side. Used by Hard AI.
    """
    opp = opponent(player)
    my_cost = _shortest_path_cost(board, player)
    opp_cost = _shortest_path_cost(board, opp)

    my_connected = _count_connected_to_start(board, player)
    opp_connected = _count_connected_to_start(board, opp)

    path_score = opp_cost - my_cost
    connectivity_bonus = (my_connected - opp_connected) * 0.3

    return path_score + connectivity_bonus
