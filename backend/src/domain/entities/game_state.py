from enum import Enum, auto
from .board import Board
from ..value_objects.position import Position
from ..value_objects.piece_type import Color, PieceType


class GamePhase(Enum):
    PLACEMENT = auto()
    MOVEMENT = auto()


class GameState:
    """Represents the state of the game."""

    def __init__(self, board: Board, 
                 current_player_color: Color,
                 phase: GamePhase = GamePhase.MOVEMENT,
                 en_passant_target: Position | None = None,
                 castling_rights: dict | None = None):
        
        self.board = board
        self.current_player_color = current_player_color
        self.phase = phase
        self.winner = None
        self.move_history = []

        # number of the column where en passant is possible
        if en_passant_target:
            self.en_passant_target = en_passant_target
        else:
            self.en_passant_target: Position | None = None
        
        ## Castling states
        if castling_rights:
            self.castling_rights : dict[dict] = castling_rights
        else:
            self.castling_rights = {
                Color.WHITE: {'kingside': True, 'queenside': True},
                Color.BLACK: {'kingside': True, 'queenside': True}
            }
        
        # if the player's move is a castle, indicate with the piece side (king or queen)
        self.castle_next_move : dict[dict] = {
            Color.WHITE: {'kingside': None, 'queenside': None}, 
            Color.BLACK: {'kingside': None, 'queenside': None}
        }

    def switch_phase(self):
        """Switches the game phase."""
        if self.phase == GamePhase.PLACEMENT:
            self.phase = GamePhase.MOVEMENT
        else:
            self.phase = GamePhase.PLACEMENT
    
    def switch_player(self):
        """Switches the current player."""
        if self.current_player_color == Color.WHITE:
            self.current_player_color = Color.BLACK
        else:
            self.current_player_color = Color.WHITE

    def is_checkmate(self) -> bool:
        # TODO
        return False

    def is_stalemate(self) -> bool:
        # TODO
        return False
    
    def add_move_to_history(self, move):
        """Adds a move to the history."""
        # TODO
