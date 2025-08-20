from ..entities.game_state import GameState
from ..value_objects.position import Position
from ..entities.piece import Piece
from .validators import Validator
from ..exceptions.game_error import InvalidMoveError


class GoChessEngine:
    """The main engine for the Go-Chess game."""

    def __init__(self, game_state: GameState, validators: list[Validator]):
        self._game_state = game_state
        self._validators = validators
        self.board = game_state.board

    def place_piece(self, piece: Piece, position: Position) -> bool:
        """A placement is an introducion of a new piece on the board.
        If the placement is valid, the board state is updated, therefore
        placing is an atomic operation, it either happens at once or it doesn't.
        """
        # TODO Validation logic will be added here

        # after all is good, place the piece
        self._game_state.board.place_piece(piece, position)
        return True

    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        """A movement is a change of position of an existing piece.
        If the movement is valid, the board state is updated, therefore
        moving is an atomic operation, it either happens at once or it doesn't."""

        # TODO Validation logic will be added here
        # this should be offloaded to a validator

        piece = self.board.get_piece(from_pos)
        if not piece:
            raise InvalidMoveError("No piece at the source position")
        
        if piece.color != self._game_state.current_player_color:
            raise InvalidMoveError("It's not your turn to move this piece")
    
        # Check if the move is valid
        if to_pos not in piece.get_possible_moves(from_pos, self.board):
            raise InvalidMoveError("Invalid move for this piece")

        # after all is good, move the piece
        self._game_state.board.move_piece(from_pos, to_pos)
        return True
    
    
