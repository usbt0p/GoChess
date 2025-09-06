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


class CheckInNextMovementValidator(Validator):

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
    
class CheckInNextPlacementValidator(Validator):
    """Validates if placing a piece would leave the player's king in check."""

    def validate(
        self,
        game_state: GameState,
        piece,  # Piece to be placed
        position: Position,
        player_color: Color,
    ) -> bool:
        """Checks if placing a piece at position would leave the king in check."""
        # Make the placement on a copy of the board
        temp_board = game_state.board.copy()
        if temp_board.get_piece(position) is not None:
            return False  # Can't place on an occupied square
        temp_board.place_piece(piece, position)

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
# the problem with the plimorphism idea:
# each validator needs different parameters, and not every one of them is done
# sequentially, some are required in different phases, plus some are
# more important than others...
# however, some stuff is susceptible to this, like stalemate, castling, en passant, promotion, etc. 
"""
- phase switch validator
- piece movement rules validator (pawns move forward, etc)
 
# for placement phase
- no placing self in check  (maybe we want a mode where the king is placed last?)
- no placing that would put opponent in check  (if applicable)
- no placing on occupied square 

- piece count  (e.g., only 1 king, 2 rooks, etc. per color)
- no pawns beyond a certain rank validator
- some sort of castling rights validator that allows certain placements to enable castling



- algebraic notation validator
    - grammar
    - syntax
    - correspondence with piece movement and board state

# these shopuld be done before, but a possibility would be (for the legal move one) to 
# just put the board in an invalid state and then check if the move is valid

- valid movement (inside board, not occupied by own piece / uneatable opponent piece, etc.)
    piece of players color, etc.)
- legal movement validator (e.g., no moving into check)


# these can be done at the end of a turn, after the board state has changed

- checkmate validator
- capture validator (when a move is capture, report the captured piece)
- opponent in check validator
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
