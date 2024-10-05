from __future__ import annotations

import functools
import time
from typing import Set, Tuple, List


class Cell:
    """
    Represents a cell on the chess board.

    Attributes:
        y (int): The y of the cell.
        x (int): The x of the cell.
    """

    def __init__(self, y: int, x: int) -> None:
        self.y = y
        self.x = x

    @property
    def position(self) -> Tuple[int, int]:
        """Gets or sets the (y, x) position of the cell."""
        return self.y, self.x

    @position.setter
    def position(self, pos: Tuple[int, int]) -> None:
        self.y, self.x = pos

    def __eq__(self, other: Cell) -> bool:
        """Checks equality based on position."""
        return isinstance(other, Cell) and self.position == other.position

    def __hash__(self) -> int:
        """Provides a hash based on the cell's position."""
        return hash(self.position)


def _populate_board(n: int) -> List[List[Cell]]:
    """
    Populates the board with Cell objects.

    Args:
        n (int): The size of the board (n x n).

    Returns:
        List[List[Cell]]: The populated board.
    """
    return [[Cell(y, x) for y in range(n)] for x in range(n)]


class Board:
    """
    Represents the chess board and handles the Knight's Tour problem.

    Attributes:
        n (int): The size of the board (n x n).
        knight (Knight): The knight piece.
        board (List[List[Cell]]): The 2D list of Cell objects.
        solution (List[List[int]]): The 2D list tracking the solution path.
        move_path (List[Tuple[int, int]]): The list of moves taken by the knight.
        visits (Set[Tuple[int, int]]): The set of visited positions.
    """

    def __init__(self, knight: Knight = None, n: int = 8) -> None:
        self.n = n
        self.board = _populate_board(n)
        self.knight = knight
        self.solution = [[-1 for _ in range(n)] for _ in range(n)]
        self.solution[0][0] = 0
        self.move_path = [(0, 0)]
        self.visits = {(0, 0)}
        self.knight.position = (0, 0)

    @functools.cache
    def solve(self) -> bool:
        """
        Attempts to solve the Knight's Tour problem.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        if self._solve_knight_tour(0, 0, 1):
            return True
        else:
            return False

    def _solve_knight_tour(self, x: int, y: int, move_count: int) -> bool:
        """
        Uses backtracking to solve the Knight's Tour problem.

        Args:
            x (int): The current x of the knight.
            y (int): The current y of the knight.
            move_count (int): The current move number.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        if move_count == self.n * self.n:
            return True

        for dx, dy in self.knight.offsets:
            nx, ny = x + dx, y + dy

            if self._is_valid(nx, ny):
                self.solution[nx][ny] = move_count
                self.knight.position = (nx, ny)
                self.visits.add((nx, ny))

                if self._solve_knight_tour(nx, ny, move_count + 1):
                    return True

                self.solution[nx][ny] = -1
                self.visits.remove((nx, ny))

        return False

    def _is_valid(self, x: int, y: int) -> bool:
        """
        Checks if a move is valid (within board boundaries and not yet visited).

        Args:
            x (int): The x to check.
            y (int): The yumn to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= x < self.n and 0 <= y < self.n and self.solution[x][y] == -1


class Knight:
    """
    Represents the Knight piece in chess.

    Attributes:
        cell (Cell): The current cell of the knight.
        offsets (List[Tuple[int, int]]): The possible move offsets for the knight.
    """

    def __init__(self) -> None:
        self._position = (0, 0)
        self.offsets = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

    @property
    def position(self) -> Tuple[int, int]:
        """Gets or sets the position of the knight."""
        return self._position

    @position.setter
    def position(self, pos: Tuple[int, int]) -> None:
        self._position = pos


if __name__ == "__main__":
    st = time.time()
    k = Knight()
    b = Board(knight=k, n=8)

    ans = b.solve()

    print(f"runtime: {(time.time() - st):.2f} s - {ans}")
