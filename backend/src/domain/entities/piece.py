from abc import ABC, abstractmethod
from ..value_objects.piece_type import PieceType, Color
from ..value_objects.position import Position


class Piece(ABC):
    """Represents a chess piece."""

    def __init__(self, piece_type: PieceType, color: Color):
        self._type = piece_type
        self._color = color

    @property
    def type(self) -> PieceType:
        return self._type

    @property
    def color(self) -> Color:
        return self._color

    @abstractmethod
    def get_possible_moves(self, position: Position, board: 'Board') -> list[Position]:
        """Returns a list of possible moves for the piece."""
        pass

    def __repr__(self) -> str:
        return f"{self.color.name.capitalize()} {self.type.name.capitalize()}"
