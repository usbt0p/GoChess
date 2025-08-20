class GameError(Exception):
    """Base class for exceptions in the game."""
    pass


class InvalidMoveError(GameError):
    """Raised when a move is invalid."""
    pass
