from ..entities.game_state import GameState
from ..value_objects.position import Position
from ..entities.piece import Piece
from .validators import Validator


class GoChessEngine:
    """The main engine for the Go-Chess game."""

    def __init__(self, game_state: GameState, validators: list[Validator]):
        self._game_state = game_state
        self._validators = validators

    def place_piece(self, piece: Piece, position: Position) -> bool:
        """Places a piece on the board during the placement phase."""
        # Validation logic will be added here
        self._game_state.board.place_piece(piece, position)
        return True

    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        """Moves a piece on the board during the movement phase."""
        # Validation logic will be added here
        self._game_state.board.move_piece(from_pos, to_pos)
        return True
