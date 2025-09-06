class GameError(Exception):
    """Base class for exceptions in the game."""
    pass

'''A distinction:
"Invalid" means the move/placement is impossible (
    e.g., moving a knight like a bishop, placing a piece out of bounds, etc.)
"Illegal" means the move/placement breaks the rules of the game, be it chess or go-chess (
    e.g., moving into check, placing on an occupied square, etc.)
For some cases the distinction is blurry, so we'll see how it goes.
'''

class InvalidMoveError(GameError):
    """Raised when a move is invalid."""
    pass

class IllegalMoveError(GameError):
    """Raised when a move is illegal, e.g., moving to an occupied square,
      moving into check."""
    pass

class InvalidPlacementError(GameError):
    """Raised when a piece placement is invalid."""
    pass

class IllegalPlacementError(GameError):
    """Raised when a piece placement is illegal."""
    pass
