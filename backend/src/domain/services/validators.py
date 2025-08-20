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
- piece movement validator

- valid movement (inside board, not occupied by own piece, etc.)
- legal movement validator (e.g., no moving into check)
- check validator
- checkmate validator
- stalemate validator
- castling validator
- en passant validator
- promotion validator
- draw by repetition validator
- draw by insufficient material validator
- time control validator
- etc.
'''