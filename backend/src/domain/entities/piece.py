from abc import ABC, abstractmethod
from ..value_objects.piece_type import PieceType, Color
from ..value_objects.position import Position
from ..entities.board import Board
from ..entities.game_state import GameState


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
    def get_possible_moves(self, position: Position, game_state: GameState) -> list[Position]:
        """
        Returns a list of pseudo-legal moves for the piece.
        Pseudo-legal moves are all possible moves a piece can make,
        without considering whether the king is in check.
        """
        pass

    def _get_sliding_moves(
        self, position: Position, board: Board, directions: list[tuple[int, int]]
    ) -> list[Position]:
        moves = []
        for dr, dc in directions:
            for i in range(1, board.size):
                row, col = position.row + i * dr, position.col + i * dc
                if not board.is_valid_position(Position(row, col)):
                    break

                target_pos = Position(row, col)
                piece_at_target = board.get_piece(target_pos)

                if piece_at_target is None:
                    moves.append(target_pos)
                elif piece_at_target.color != self.color:
                    moves.append(target_pos)  # Capture
                    break
                else:
                    break  # Blocked by own piece
        return moves

    def __repr__(self) -> str:
        return f"{self.color.name.capitalize()} {self.type.name.capitalize()}"
    
    def __str__(self):
        '''Use the unicode chess character for the piece in the console'''
        
        chess_set = '♙♘♗♖♕♔♟♞♝♜♛♚'
        # assuming the background is black... so white pieces are actually black
        if self.color == Color.WHITE:
            return chess_set[self.type.value + 6]
        else:
            return chess_set[self.type.value]


class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(PieceType.PAWN, color)

    def get_possible_moves(self, position: Position, game_state: GameState) -> list[Position]:
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        start_row = 6 if self.color == Color.WHITE else 1
        board = game_state.board

        # 1. Forward move
        one_step = Position(position.row + direction, position.col)
        if board.is_valid_position(one_step) and board.get_piece(one_step) is None:
            moves.append(one_step)

            # 2. Double step from start
            if position.row == start_row:
                two_steps = Position(position.row + 2 * direction, position.col)
                if (
                    board.is_valid_position(two_steps)
                    and board.get_piece(two_steps) is None
                ):
                    moves.append(two_steps)

        # 3. Captures
        for dc in [-1, 1]:
            capture_pos = Position(position.row + direction, position.col + dc)
            if board.is_valid_position(capture_pos):
                target_piece = board.get_piece(capture_pos)
                if target_piece and target_piece.color != self.color:
                    moves.append(capture_pos)

        # 4. En passant
        # TODO if this becomes a propblem, offload en passant logic to a validator and just read from the game state here
        if game_state.en_passant_target:
            # The capturing pawn must be on the 5th rank for White or 4th for Black
            correct_rank = (self.color == Color.WHITE and position.row == 3) or \
                           (self.color == Color.BLACK and position.row == 4)

            if correct_rank:
                # The target square must be diagonal to the current pawn's file
                if abs(position.col - game_state.en_passant_target.col) == 1:
                    # The target square must be on the correct destination rank
                    if (self.color == Color.WHITE and game_state.en_passant_target.row == position.row - 1) or \
                       (self.color == Color.BLACK and game_state.en_passant_target.row == position.row + 1):
                        moves.append(game_state.en_passant_target)
        
        return moves


class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(PieceType.KNIGHT, color)

    def get_possible_moves(self, position: Position, game_state: GameState) -> list[Position]:
        moves = []
        deltas = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1),
        ]
        board = game_state.board

        for dr, dc in deltas:
            target_pos = Position(position.row + dr, position.col + dc)
            if board.is_valid_position(target_pos):
                target_piece = board.get_piece(target_pos)
                if target_piece is None or target_piece.color != self.color:
                    moves.append(target_pos)
        return moves


class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(PieceType.BISHOP, color)

    def get_possible_moves(self, position: Position, game_state: GameState) -> list[Position]:
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._get_sliding_moves(position, game_state.board, directions)


class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(PieceType.ROOK, color)

    def get_possible_moves(self, position: Position, game_state: GameState) -> list[Position]:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._get_sliding_moves(position, game_state.board, directions)


class Queen(Piece):
    def __init__(self, color: Color):
        super().__init__(PieceType.QUEEN, color)

    def get_possible_moves(self, position: Position, game_state: GameState) -> list[Position]:
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Rook moves
            (1, 1), (1, -1), (-1, 1), (-1, -1),  # Bishop moves
        ]
        return self._get_sliding_moves(position, game_state.board, directions)


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(PieceType.KING, color)

    def get_possible_moves(self, position: Position, game_state: GameState) -> list[Position]:
        moves = []
        deltas = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
        ]
        board = game_state.board

        for dr, dc in deltas:
            target_pos = Position(position.row + dr, position.col + dc)
            if board.is_valid_position(target_pos):
                target_piece = board.get_piece(target_pos)
                if target_piece is None or target_piece.color != self.color:
                    moves.append(target_pos)
        
        # TODO: Castling logic
        # add in the movement a record of king moves and rook moves to validate castling rights in the movement loop in engine
        # also, we'll need to check if the squares the king passes through are under attack
        # if this becomes a problem, offload castling logic to a validator and just read from the game state here
        castling_rights = game_state.castling_rights[self.color]
        
        if castling_rights[PieceType.KING]:
            # Kingside castling
            # cool use of the for-else construct!
            for c in range(position.col + 1, board.size - 1):
                if board.get_piece(Position(position.row, c)) is not None:
                    break
            else:
                move = Position(position.row, board.size - 2)
                moves.append(move) 
                game_state.castle_next_move[self.color] = move
        
        if castling_rights[PieceType.QUEEN]:
            # Queenside castling
            for c in range(position.col - 1, 0, -1): # reverse to break on the first piece found
                if board.get_piece(Position(position.row, c)) is not None:
                    break
            else:
                move = Position(position.row, 2)
                moves.append(move)
                game_state.castle_next_move[self.color] = move
        
        return moves
