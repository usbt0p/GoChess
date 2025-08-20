from typing import Optional
from .piece import Piece
from ..value_objects.position import Position
from ..exceptions.game_error import *


class Board:
    """Represents the chess board."""

    def __init__(self, size: int = 8):

        self._size = size
        # just a list of lists
        self._grid: list[list[Optional[Piece]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]

    def place_piece(self, piece: Piece, position: Position):
        
        if not piece:
            raise ValueError("Invalid piece")
        
        if self.is_valid_position(position):
            self._grid[position.row][position.col] = piece
        else:
            raise ValueError("Invalid board position")

    def get_piece(self, position: Position) -> Optional[Piece]:
        
        if self.is_valid_position(position):
            return self._grid[position.row][position.col]
        return None

    def move_piece(self, from_pos: Position, to_pos: Position):
        
        piece = self.get_piece(from_pos)
        if piece:
            self._grid[from_pos.row][from_pos.col] = None
            self.place_piece(piece, to_pos)
        else:
            raise InvalidMoveError("No piece at the source position")

    def is_valid_position(self, position: Position) -> bool:
        
        return 0 <= position.row < self._size and 0 <= position.col < self._size

    def __repr__(self) -> str:
        # Find the max width of any piece's string representation
        max_width = 1  # Minimum width for empty squares
        for row in self._grid:
            for piece in row:
                if piece:
                    max_width = max(max_width, len(str(piece)))

        # this pads the cells to align them using python's string formatting
        cell_fmt = f"{{:>{max_width}}}"

        lines = []
        for i, row in enumerate(self._grid):
            line = []
            for j, piece in enumerate(row):
                cell = str(piece) if piece else "□" if (i + j) % 2 == 0 else "▨"
                line.append(cell_fmt.format(cell))
            lines.append(" ".join(line))
        return "\n".join(lines)
