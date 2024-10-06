import functools
import time

N = 8

MX = [1, 2, 2, 1, -1, -2, -2, -1]
MY = [-2, -1, 1, 2, 2, 1, -1, -2]


def degree(x, y, board):
    count = 0
    for i in range(8):
        nx, ny = x + MX[i], MY[i] + y
        if check(nx, ny, board):
            count += 1
    return count


def check(x, y, board):
    return N > x >= 0 and N > y >= 0 and board[x][y] == -1


@functools.cache
def solve():
    board = [[-1 for _ in range(N)] for _ in range(N)]
    board[0][0] = 0

    if not kt(board, 0, 0):
        return False
    return True


def kt(board, x, y):
    for pos in range(1, N * N):
        idx = -1
        deg = N + 1
        nnx, nny = -1, -1

        for i in range(8):
            nx, ny = x + MX[i], y + MY[i]
            if check(nx, ny, board):
                count = degree(x, y, board)
                if count < deg:
                    deg = count
                    idx = i
                    nnx, nny = nx, ny

        if deg == -1:
            return False

        x, y = nnx, nny
        board[x][y] = pos

    return True


if __name__ == "__main__":
    print(solve())

