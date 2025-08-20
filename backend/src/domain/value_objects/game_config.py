from dataclasses import dataclass
from typing import Dict, Optional
from ..value_objects.piece_type import PieceType

 
@dataclass 
class GameConfigStandard:
    allowed_pieces: Dict[PieceType, int]
    max_placement_turns: Optional[int] = None
    pawn_promotion_distance: int = 2
    enable_castling: bool = True

# TODO it would be optimal to have the GameConfig as a base class that has
# all the possible attributes, and then have inherited specific modes like
# GameConfigStandard, GameConfigBlitz, etc, reading from a configuration file.

# then, weirder modes can be configured using a specific user config


