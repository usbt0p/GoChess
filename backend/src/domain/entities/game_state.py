from enum import Enum, auto
from .board import Board
from ..value_objects.color import Color


class GamePhase(Enum):
    PLACEMENT = auto()
    MOVEMENT = auto()


class GameState:
    """Represents the state of the game."""

    def __init__(self, board: Board, current_player_color: Color):
        self.board = board
        self.current_player_color = current_player_color
        self.phase = GamePhase.PLACEMENT
        self.winner = None
        self.move_history = []

    def switch_phase(self):
        """Switches the game phase."""
        if self.phase == GamePhase.PLACEMENT:
            self.phase = GamePhase.MOVEMENT
        else:
            # TODO
            pass

    def is_checkmate(self) -> bool:
        # TODO
        return False

    def is_stalemate(self) -> bool:
        # TODO
        return False
    
    def add_move_to_history(self, move):
        """Adds a move to the history."""
        # TODO
