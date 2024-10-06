import functools
import time

N = 8

MX = [1, 2, 2, 1, -1, -2, -2, -1]
MY = [-2, -1, 1, 2, 2, 1, -1, -2]


def degree(x, y, board):
    """
    Counts how many valid moves can be made from the current knight's position (x, y).

    A valid move is one where the knight moves to an unvisited square within
    the board's boundaries. The count represents how many onward moves are
    available from this position, helping the knight make smarter decisions
    based on Warnsdorff's rule (which favors positions with fewer onward moves).

    Args:
        x (int): Current x-coordinate of the knight.
        y (int): Current y-coordinate of the knight.
        board (list): The current board configuration showing visited cells.

    Returns:
        int: Number of valid moves from (x, y).
    """
    count = 0
    for i in range(8):
        nx, ny = x + MX[i], y + MY[i]
        if check(nx, ny, board):
            count += 1
    return count


def check(x, y, board):
    """
    Checks whether the knight's move to (x, y) is valid.

    A move is valid if the target square (x, y) is within the board's limits
    and has not been visited yet.

    Args:
        x (int): Target x-coordinate for the knight.
        y (int): Target y-coordinate for the knight.
        board (list): The current board configuration.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1


@functools.cache
def solve():
    """
    Solves the Knight's Tour problem using Warnsdorff's heuristic.

    The goal is to move a knight on a chessboard such that it visits every
    square exactly once. Warnsdorff's heuristic helps guide the knight's moves
    by always selecting the next square that has the fewest onward moves.

    The function starts at position (0, 0) and attempts to find a tour. If
    successful, it prints the solution; otherwise, it indicates that no solution
    was found.

    Returns:
        bool: True if a solution was found, False otherwise.
    """
    board = [[-1 for _ in range(N)] for _ in range(N)]  # Initialize the board
    board[0][0] = 0  # Start knight at position (0, 0)

    if not kt(board, 0, 0, 1):
        return False
    else:
        display(board)
        return True


def kt(board, x, y, pos):
    """
    Recursively attempts to solve the Knight's Tour problem using Warnsdorff's rule.

    This function tries to move the knight to all possible positions, choosing
    the one with the least onward moves first. If it reaches a dead-end, it
    backtracks and tries a different path.

    Args:
        board (list): The current state of the board.
        x (int): Current x-coordinate of the knight.
        y (int): Current y-coordinate of the knight.
        pos (int): The number of the current move (starting from 1).

    Returns:
        bool: True if the knight successfully completes the tour, False otherwise.
    """
    if pos == N * N:
        return True

    idx = -1
    temp = N + 1
    nnx, nny = -1, -1

    for i in range(8):
        nx, ny = x + MX[i], y + MY[i]
        if check(nx, ny, board):
            deg = degree(nx, ny, board)
            if deg < temp:
                temp = deg
                idx = i
                nnx, nny = nx, ny

    if idx == -1:  # No valid move found (dead-end)
        return False

    board[nnx][nny] = pos

    if kt(board, nnx, nny, pos + 1):
        return True

    board[nnx][nny] = -1
    return False


def display(board):
    """
    Prints the current state of the board, showing the knight's tour.

    The board is displayed with the move numbers in a nicely formatted grid.

    Args:
        board (list): The current board configuration showing move numbers.
    """
    for row in board:
        print(' '.join(f'{cell:2}' for cell in row))


if __name__ == "__main__":
    solve()
