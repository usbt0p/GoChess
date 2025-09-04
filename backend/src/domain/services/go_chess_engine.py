from ..entities.game_state import GameState
from ..value_objects.position import Position
from ..entities.piece import Piece
from .validators import *
from ..exceptions.game_error import *
from ..value_objects.piece_type import Color, PieceType

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
        # this is the last step ideally
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

        # -------- MUST-HAVE VALIDATIONS BEFORE THE MOVE -----------

        # TODO this should be offloaded to a validator until next "section"
        piece = self._game_state.board.get_piece(from_pos)
        print("Piece at pos: ", piece)
        if not piece:
            raise InvalidMoveError("No piece at the source position")
        
        if piece.color != self._game_state.current_player_color:
            raise InvalidMoveError("It's not your turn to move this piece")
    
        # Check if the move is valid
        possible_moves = piece.get_possible_moves(from_pos, self._game_state)
        print("Possible moves: ", [pos.algebraic() for pos in possible_moves])
        if to_pos not in possible_moves:
            raise InvalidMoveError("Invalid move for this piece")

        # Validators for check conditions
        check_next = CheckNextValidator()

        # simulate the move and check if the current player's king would be in check
        if check_next.validate(self._game_state, from_pos, to_pos, piece.color):
            raise InvalidMoveError("Move would leave king in check")

        if self._game_state.en_passant_target: # only do this if en passant is possible       
            if is_en_passant_capture(self._game_state, from_pos, to_pos, piece.color):
                print(f"En Passant capture detected by {piece} at {to_pos.algebraic()}")
                
                # Remove the captured pawn
                captured_pawn_pos = Position(from_pos.row, to_pos.col)
                self._game_state.board.remove_piece(captured_pawn_pos)
                print(f"Captured pawn removed from {captured_pawn_pos.algebraic()}")
                
                # Clear en passant target after the capture
                self._game_state.en_passant_target = None

        # TODO this should be done after everything else... or figure out a good order
        # after all is good, move the piece
        self._game_state.board.move_piece(from_pos, to_pos)

        # -------- CHECKS MADE AFTER THE MOVE -----------

        # update en passant target after a two-square pawn move
        if piece.type == PieceType.PAWN:
           
            if abs(from_pos.row - to_pos.row) == 2:
                direction = -1 if piece.color == Color.WHITE else 1
                self._game_state.en_passant_target = Position(from_pos.row + direction, from_pos.col)
            else:
                self._game_state.en_passant_target = None
        
        # update castling rights if a king or rook has moved
        if piece.type == PieceType.KING:
            self._game_state.castling_rights[piece.color]['kingside'] = False
            self._game_state.castling_rights[piece.color]['queenside'] = False
            # check if the move was a castle, if so move the rook as well
            if abs(from_pos.col - to_pos.col) == 2:
                # kingside
                if to_pos.col > from_pos.col:
                    rook_from = Position(from_pos.row, 7)
                    rook_to = Position(from_pos.row, 5)
                # queenside
                else:
                    rook_from = Position(from_pos.row, 0)
                    rook_to = Position(from_pos.row, 3)
                self._game_state.board.move_piece(rook_from, rook_to)

        if piece.type == PieceType.ROOK:
            if from_pos.col == 0 and from_pos.row == (7 if piece.color == Color.WHITE else 0):
                self._game_state.castling_rights[piece.color]['queenside'] = False
            elif from_pos.col == 7 and from_pos.row == (7 if piece.color == Color.WHITE else 0):
                self._game_state.castling_rights[piece.color]['kingside'] = False

        # promotion triggers when a pawn move reaches the last rank
        if piece.type == PieceType.PAWN:
            if ((piece.color == Color.WHITE and to_pos.row == 0) 
                or 
                (piece.color == Color.BLACK and to_pos.row == 7)):
                self.handle_promotion(to_pos, self.promotion_prompt)

        # get info and do sanity checks
        if is_capture(self._game_state, to_pos, piece.color):
            # Handle capture logic
            print(f"Capture detected from {piece} at {to_pos.algebraic()}")

        # see if the move gives check to the opposing king AFTER a valid state is reached
        check_now = CheckNowValidator()
        print("Checking for check...")
        if check_now.validate(self._game_state, ~piece.color):
            print(f"Move results in check to {(~piece.color).name.capitalize()}")

        return True
    
    # TESTTTTTTT!!!!!!!!!!!!!!!!!!!!

    def handle_promotion(self, position: Position, promotion_prompt : callable) -> bool:
        """Handles the promotion of a pawn that has reached the last rank."""
        piece = self._game_state.board.get_piece(position)
        if not piece or piece.type != PieceType.PAWN:
            raise InvalidMoveError("No pawn at the promotion position")
        
        new_piece_type = promotion_prompt()

        if new_piece_type not in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
            raise ValueError("Invalid piece type for promotion")
        
        # Replace the pawn with the new piece
        new_piece = Piece.create (new_piece_type, piece.color)
        self._game_state.board.place_piece(new_piece, position)
        return True

    def promotion_prompt(self) -> PieceType:
        # TODO move to services??
        """A simple console-based prompt for choosing a promotion piece.
        In a real application, this would be replaced with a GUI component or similar."""
        
        new_piece_type = input("Promote to (Q, R, B, N): ").strip().upper()
        while True:
            match new_piece_type:
                case 'Q': new_piece_type = PieceType.QUEEN; break
                case 'R': new_piece_type = PieceType.ROOK; break
                case 'B': new_piece_type = PieceType.BISHOP; break
                case 'N': new_piece_type = PieceType.KNIGHT; break
                case _: raise ValueError("Invalid input for promotion")
        
        return new_piece_type

