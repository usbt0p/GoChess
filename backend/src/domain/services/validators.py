from abc import ABC, abstractmethod
from ..entities.board import Board
from ..entities.piece import Pawn
from ..value_objects.position import Position
from ..value_objects.piece_type import PieceType, Color


class Validator(ABC):
    """Abstract class for a rule validator."""

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        ...

# --- Validation Helper Functions ---

def find_king(board: Board, color: Color) -> Position | None:
    """Finds the position of the king of a given color on the board."""
    for r in range(board.size):
        for c in range(board.size):
            pos = Position(r, c)
            piece = board.get_piece(pos)
            if piece and piece.type == PieceType.KING and piece.color == color:
                return pos
    return None


def is_square_attacked_by(board: Board, position: Position, attacker_color: Color) -> bool:
    """Checks if a square is under attack by any piece of the attacker's color."""
    # scan all pieces of the attacker color
    # and check if any can move to the position
    for r in range(board.size):
        for c in range(board.size):
            attacker_pos = Position(r, c)
            piece = board.get_piece(attacker_pos)

            if piece is None or piece.color != attacker_color:
                continue

            possible_moves = piece.get_possible_moves(attacker_pos, board)
            if position in possible_moves:
                if isinstance(piece, Pawn):
                    # A pawn only attacks diagonally.
                    if attacker_pos.col != position.col:
                        return True
                else:
                    return True
    return False

def is_capture(board: Board, position: Position, attacker_color: Color) -> bool:
    """Checks if a square is occupied by an opponent's piece (i.e., a capture)."""
    piece = board.get_piece(position)
    return piece is not None and piece.color != attacker_color


# --- Validator Classes ---

class CheckValidator(Validator):
    """Validates if a player is currently in check."""

    def validate(self, board: Board, player_color: Color) -> bool:
        """Checks if the king of the specified color is under attack."""
        king_pos = find_king(board, player_color)
        if not king_pos:
            return False  # No king, no check

        opponent_color = Color.WHITE if player_color == Color.BLACK else Color.BLACK
        return is_square_attacked_by(board, king_pos, opponent_color)


# TODO: Implement other specific rule validators
'''
- phase switch validator
- piece placement validator
- piece movement rules validator (pawns move forward, etc)

- algebraic notation validator
    - grammar
    - syntax
    - correspondence with piece movement and board state

- valid movement (inside board, not occupied by own piece, 
    piece of players color, etc.)
- legal movement validator (e.g., no moving into check)
- check validator
- capture validator (when a move is capture, report the captured piece)
- checkmate validator

- stalemate validator
- castling validator
- en passant validator
- promotion validator
- draw by repetition validator
- draw by insufficient material validator
- time control validator
- timeout
- etc.
'''