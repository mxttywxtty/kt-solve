from __future__ import annotations
from typing import Set, Tuple, List
import time


class Cell:
    """
    Represents a cell on the chess board.

    Attributes:
        col (int): The column of the cell.
        row (int): The row of the cell.
    """

    def __init__(self, col: int, row: int) -> None:
        self.col = col
        self.row = row

    @property
    def position(self) -> Tuple[int, int]:
        """Gets or sets the (col, row) position of the cell."""
        return self.col, self.row

    @position.setter
    def position(self, pos: Tuple[int, int]) -> None:
        self.col, self.row = pos

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
    return [[Cell(col, row) for col in range(n)] for row in range(n)]


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

    # TODO: use ncurses to display solution in terminal
    def show(self) -> None:
        """
        Displays the current state of the chess board.
        The knight is represented by 'K' and visited cells by 'o'.
        """
        print("   ", end="")
        for col in range(self.n):
            print(f" {col} ", end="")
        print()
        for row in range(self.n):
            print(f" {row} ", end="")
            for col in range(self.n):
                if (row, col) == self.knight.position:
                    print("\033[31m K \033[0m", end="")
                elif (row, col) in self.visits:
                    print("\033[33m o \033[0m", end="")
                else:
                    print(" . ", end="")
            print()

    def solve(self) -> bool:
        """
        Attempts to solve the Knight's Tour problem.
        
        Returns:
            bool: True if a solution is found, False otherwise.
        """
        if self._solve_knight_tour(0, 0, 1):
            return True
        else:
            print("No solution found")
            return False

    def _solve_knight_tour(self, row: int, col: int, move_count: int) -> bool:
        """
        Uses backtracking to solve the Knight's Tour problem.

        Args:
            row (int): The current row of the knight.
            col (int): The current column of the knight.
            move_count (int): The current move number.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        if move_count == self.n * self.n:
            return True

        for dx, dy in self.knight.offsets:
            next_row, next_col = row + dx, col + dy

            if self._is_valid(next_row, next_col):
                self.solution[next_row][next_col] = move_count
                self.knight.position = (next_row, next_col)
                self.visits.add((next_row, next_col))

                self.show()
                print(f"Move: {move_count}")
                time.sleep(0.2)
                print("\033[H\033[J", end="")  # Clear the terminal screen

                if self._solve_knight_tour(next_row, next_col, move_count + 1):
                    return True

                self.solution[next_row][next_col] = -1
                self.visits.remove((next_row, next_col))

        return False

    def _is_valid(self, row: int, col: int) -> bool:
        """
        Checks if a move is valid (within board boundaries and not yet visited).

        Args:
            row (int): The row to check.
            col (int): The column to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return 0 <= row < self.n and 0 <= col < self.n and self.solution[row][col] == -1


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
    k = Knight()
    b = Board(knight=k, n=8)

    if b.solve():
        print("Solution found")
    else:
        print("No solution found")
