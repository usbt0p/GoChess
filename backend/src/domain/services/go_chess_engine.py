from ..entities.game_state import GameState
from ..value_objects.position import Position
from ..entities.piece import Piece
from .validators import CheckNextValidator, Validator, is_capture, CheckNowValidator
from ..exceptions.game_error import *

class GoChessEngine:
    """The main engine for the Go-Chess game."""

    def __init__(self, game_state: GameState, validators: list[Validator]):
        self._game_state = game_state
        self._validators = validators

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
        # TODO validators are held in a list, and share the same interface
        # except for the arguments they take
        # we can iterate and pass all the arguments, and let them sort it out
        # or we can modify in some way the interface to accept the game state which has the board 

        # TODO this should be offloaded to a validator until next todo
        piece = self._game_state.board.get_piece(from_pos)
        print("Piece at pos: ", piece)
        if not piece:
            raise InvalidMoveError("No piece at the source position")
        
        if piece.color != self._game_state.current_player_color:
            raise InvalidMoveError("It's not your turn to move this piece")
    
        # Check if the move is valid
        possible_moves = piece.get_possible_moves(from_pos, self._game_state.board)
        print("Possible moves: ", [pos.algebraic() for pos in possible_moves])
        if to_pos not in possible_moves:
            raise InvalidMoveError("Invalid move for this piece")

        if is_capture(self._game_state.board, to_pos, piece.color):
            # Handle capture logic
            print(f"Capture detected from {piece} at {to_pos.algebraic()}")

        check_now = CheckNowValidator()
        check_next = CheckNextValidator()

        # simulate the move and check if the current player's king would be in check
        if check_next.validate(self._game_state.board, from_pos, to_pos, piece.color):
            raise InvalidMoveError("Move would leave king in check")

        # after all is good, move the piece
        self._game_state.board.move_piece(from_pos, to_pos)

        # see if the move gives check to the opposing king AFTER a valid state is reached
        print("Checking for check...")
        if check_now.validate(self._game_state.board, ~piece.color):
            print(f"Move results in check to {(~piece.color).name.capitalize()}")


        # TODO until here

        return True
    
    
