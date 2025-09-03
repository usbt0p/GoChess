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
        possible_moves = piece.get_possible_moves(from_pos, self._game_state)
        print("Possible moves: ", [pos.algebraic() for pos in possible_moves])
        if to_pos not in possible_moves:
            raise InvalidMoveError("Invalid move for this piece")

        # Validators for check conditions
        check_now = CheckNowValidator()
        check_next = CheckNextValidator()

        # simulate the move and check if the current player's king would be in check
        if check_next.validate(self._game_state, from_pos, to_pos, piece.color):
            raise InvalidMoveError("Move would leave king in check")

        # get info and do sanity checks
        if is_capture(self._game_state, to_pos, piece.color):
            # Handle capture logic
            print(f"Capture detected from {piece} at {to_pos.algebraic()}")

        if self._game_state.en_passant_target: # only do this if en passant is possible       
            if is_en_passant_capture(self._game_state, from_pos, to_pos, piece.color):
                print(f"En Passant capture detected by {piece} at {to_pos.algebraic()}")
                
                # Remove the captured pawn
                captured_pawn_pos = Position(from_pos.row, to_pos.col)
                self._game_state.board.remove_piece(captured_pawn_pos)
                print(f"Captured pawn removed from {captured_pawn_pos.algebraic()}")
                
                # Clear en passant target after the capture
                self._game_state.en_passant_target = None


        # see if the move gives check to the opposing king AFTER a valid state is reached
        # just to inform the players
        print("Checking for check...")
        if check_now.validate(self._game_state, ~piece.color):
            print(f"Move results in check to {(~piece.color).name.capitalize()}")

        # after all is good, move the piece
        self._game_state.board.move_piece(from_pos, to_pos)

        # update states like en passant target and castling rights
        if piece.type == PieceType.PAWN:
            # if a pawn moved two squares forward, set the en passant target
            print("validating en passant...", abs(from_pos.row - to_pos.row) == 2)
            if abs(from_pos.row - to_pos.row) == 2:
                direction = -1 if piece.color == Color.WHITE else 1
                self._game_state.en_passant_target = Position(from_pos.row + direction, from_pos.col)
            else:
                self._game_state.en_passant_target = None
        
        possible_castles = self._game_state.castle_next_move[piece.color]
        # use the castle_next_move to determine the available castles and move the rook accordingly

        # TODO pending: A player may not castle out of, through, or into check.
       
        if possible_castles[PieceType.KING] is not None:
            # move the rook, king already moves by itself to the correct position (relative to king)
            if possible_castles[PieceType.KING] == Position(from_pos.row, from_pos.col + 2):
                rook_from_pos = Position(from_pos.row, from_pos.col + 3)
                rook_to_pos = Position(from_pos.row, from_pos.col + 1)
            elif possible_castles[PieceType.KING] == Position(from_pos.row, from_pos.col - 2):
                rook_from_pos = Position(from_pos.row, from_pos.col - 4)
                rook_to_pos = Position(from_pos.row, from_pos.col - 1)
            
            rook = self._game_state.board.get_piece(rook_from_pos)
            if rook and rook.type == PieceType.ROOK and rook.color == piece.color:
                self._game_state.board.move_piece(rook_from_pos, rook_to_pos)
                print(f"Castling performed: Rook moved from {rook_from_pos.algebraic()} to {rook_to_pos.algebraic()}")

            else:
                raise InvalidMoveError("Invalid castling move: Rook not in the correct position")
            
        # update castling rights if a king or rook has moved 
        match piece.type:
            case PieceType.KING:
                self._game_state.castling_rights[piece.color][PieceType.KING] = False
                self._game_state.castling_rights[piece.color][PieceType.QUEEN] = False
            case PieceType.ROOK:
                if from_pos.col == 0:
                    self._game_state.castling_rights[piece.color][PieceType.QUEEN] = False
                elif from_pos.col == self._game_state.board.size - 1:
                    self._game_state.castling_rights[piece.color][PieceType.KING] = False  
                  

        # if piece.type == PieceType.KING or piece.type == PieceType.ROOK:
        #     # update castling rights
        #     self._game_state.castling_rights[piece.color][piece.type] = False
            
        #     # if the move is a castle, move the rook as well
        #     if piece.type == PieceType.KING and abs(from_pos.col - to_pos.col) == 2:
        #         rook_from_col = 0 if to_pos.col < from_pos.col else self._game_state.board.size - 1
        #         rook_to_col = from_pos.col - 1 if to_pos.col < from_pos.col else from_pos.col + 1
        #         rook_from_pos = Position(from_pos.row, rook_from_col)
        #         rook_to_pos = Position(from_pos.row, rook_to_col)
                
        #         rook = self._game_state.board.get_piece(rook_from_pos)
        #         if rook and rook.type == PieceType.ROOK and rook.color == piece.color:
        #             self._game_state.board.move_piece(rook_from_pos, rook_to_pos)
        #             print(f"Castling performed: Rook moved from {rook_from_pos.algebraic()} to {rook_to_pos.algebraic()}")
        #         else:
        #             raise InvalidMoveError("Invalid castling move: Rook not in the correct position")

        return True
    
    
