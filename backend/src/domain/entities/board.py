from typing import Optional

from ..value_objects.position import Position
from ..exceptions.game_error import *


class Board:
    """Represents the chess board."""

    def __init__(self, size: int = 8):
        from ..entities.piece import Piece
        self.size = size
        # just a list of lists
        self._grid: list[list[Optional[Piece]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]

    def place_piece(self, piece, position: Position):
        
        if not piece:
            raise ValueError("Invalid piece")
        
        if self.is_valid_position(position):
            self._grid[position.row][position.col] = piece
        else:
            raise InvalidPlacementError("Invalid board position")
        
    def remove_piece(self, position: Position):
        
        if self.is_valid_position(position):
            self._grid[position.row][position.col] = None
        else:
            raise InvalidPlacementError("Invalid board position")

    def get_piece(self, position: Position):
        
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
        
        return 0 <= position.row < self.size and 0 <= position.col < self.size

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
    
    def copy(self):
        new_board = Board(self.size)
        for r in range(self.size):
            for c in range(self.size):
                piece = self.get_piece(Position(r, c))
                if piece:
                    new_board.place_piece(piece, Position(r, c))
        return new_board
