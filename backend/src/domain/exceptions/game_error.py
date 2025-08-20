class GameError(Exception):
    """Base class for exceptions in the game."""
    pass

class InvalidMoveError(GameError):
    """Raised when a move is invalid."""
    pass

class IllegalMoveError(GameError):
    """Raised when a move is illegal, e.g., moving to an occupied square,
      moving into check."""
    pass
