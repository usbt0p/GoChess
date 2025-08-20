from abc import ABC, abstractmethod
from ..entities.game_state import GameState

class Validator(ABC):
    """Abstract class for a rule validator."""

    @abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        ...


# TODO: Implement specific rule validators
'''
- phase switch validator
- piece placement validator
- piece movement rules validator (pawns move forward, etc)

- algebraic notation validator
    - grammar
    - syntax
    - correspondence with piece movement and board state

- valid movement (inside board, not occupied by own piece, 
    piece of players color, etc.)
- legal movement validator (e.g., no moving into check)
- check validator
- capture validator (when a move is capture, report the captured piece)
- checkmate validator

- stalemate validator
- castling validator
- en passant validator
- promotion validator
- draw by repetition validator
- draw by insufficient material validator
- time control validator
- timeout
- etc.
'''