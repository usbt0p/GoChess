from abc import ABC, abstractmethod
from ..entities.board import Board
from ..entities.game_state import GameState
from ..value_objects.position import Position
from ..value_objects.piece_type import PieceType, Color


class Validator(ABC):
    """Abstract class for a rule validator."""

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool: ...


# --- Validation Helper Functions ---


def find_king(game_state: GameState, color: Color) -> Position | None:
    """Finds the position of the king of a given color on the board."""
    board = game_state.board
    for r in range(board.size):
        for c in range(board.size):
            pos = Position(r, c)
            piece = board.get_piece(pos)
            if piece and piece.type == PieceType.KING and piece.color == color:
                return pos
    return None


def is_square_attacked_by(
    game_state: GameState, position: Position, attacker_color: Color
) -> bool:
    """Checks if a square is under attack by any piece of the attacker's color."""
    # scan all pieces of the attacker color
    # and check if any can move to the position
    board = game_state.board
    for r in range(board.size):
        for c in range(board.size):
            attacker_pos = Position(r, c)
            piece = board.get_piece(attacker_pos)

            if piece is None or piece.color != attacker_color:
                continue

            # don't consider castling as an attack move to remove recursion error
            if piece.type == PieceType.KING:
                possible_moves = piece.get_possible_moves(
                    attacker_pos, game_state, include_castling=False
                )
            else:
                possible_moves = piece.get_possible_moves(attacker_pos, game_state)

            if position in possible_moves:
                if piece.type == PieceType.PAWN:
                    # A pawn only attacks diagonally.
                    if attacker_pos.col != position.col:
                        return True
                else:
                    return True
    return False


def is_capture(
    game_state: GameState, position: Position, attacker_color: Color
) -> bool:
    """Checks if a square is occupied by an opponent's piece (i.e., a capture)."""
    piece = game_state.board.get_piece(position)
    return piece is not None and piece.color != attacker_color


def is_en_passant_capture(
    game_state: GameState, from_pos: Position, to_pos: Position, attacker_color: Color
) -> bool:
    """Checks if a move is an en passant capture."""
    piece = game_state.board.get_piece(from_pos)
    if not piece or piece.type != PieceType.PAWN or piece.color != attacker_color:
        return False

    # if the pawn has moved diagonally to an empty square
    if (
        abs(from_pos.col - to_pos.col) == 1
        and from_pos.row + (1 if attacker_color == Color.BLACK else -1) == to_pos.row
    ):
        # and  the target square is the en passant target
        if game_state.en_passant_target and to_pos == game_state.en_passant_target:
            return True
    return False


# --- Validator Classes ---


class CheckNowValidator(Validator):
    """Validates if a player is currently in check."""

    def validate(self, game_state: GameState, player_color: Color) -> bool:
        """Checks if the king of the specified color is under attack."""
        king_pos = find_king(game_state, player_color)
        if not king_pos:
            return False  # No king, no check

        opponent_color = Color.WHITE if player_color == Color.BLACK else Color.BLACK
        return is_square_attacked_by(game_state, king_pos, opponent_color)


class CheckNextValidator(Validator):

    def validate(
        self,
        game_state: GameState,
        from_pos: Position,
        to_pos: Position,
        player_color: Color,
    ) -> bool:
        """Checks if moving a piece from from_pos to to_pos would leave the king in check."""
        # Make the move on a copy of the board
        temp_board = game_state.board.copy()
        piece = temp_board.get_piece(from_pos)
        if not piece or piece.color != player_color:
            return False  # Invalid move
        temp_board.move_piece(from_pos, to_pos)

        # Create a temporary game state for validation
        temp_game_state = GameState(
            board=temp_board,
            current_player_color=game_state.current_player_color,
            en_passant_target=game_state.en_passant_target,
            castling_rights=game_state.castling_rights,
        )

        check = CheckNowValidator()
        return check.validate(temp_game_state, player_color)


# TODO: Implement other specific rule validators
"""
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
"""
