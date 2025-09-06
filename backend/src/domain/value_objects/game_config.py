import yaml
from dataclasses import dataclass, field, fields
from enum import Enum, auto
from pathlib import Path

from src.domain.entities.game_state import GamePhase


class KingPlacementRule(Enum):
    """Defines rules for when the king can be placed."""
    ANY = auto()
    FIRST = auto()
    LAST = auto()

def _default_max_pieces():
    """Factory for the default max_pieces dictionary."""
    return {"PAWN": 8, "ROOK": 2, "KNIGHT": 2, "BISHOP": 2, "QUEEN": 1}

@dataclass(frozen=True)
class GameConfig:
    """Holds all configuration parameters for a game, loaded from a file."""
    phase : GamePhase = GamePhase.PLACEMENT
    placement_turns: int = 20
    max_pieces: dict[str, int] = field(default_factory=_default_max_pieces)
    place_king_as_piece: bool = False
    king_placement_rule: KingPlacementRule = KingPlacementRule.ANY
    pawn_placement_rank_limit: int = 4

    @classmethod
    def from_yaml(cls, file_path: str | Path):
        """
        Loads configuration from a YAML file.
        Uses dataclass defaults for any missing values in the file.
        """
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)

        # Convert string from YAML to KingPlacementRule enum member
        if 'king_placement_rule' in data:
            rule_str = data['king_placement_rule'].upper()
            try:
                data['king_placement_rule'] = KingPlacementRule[rule_str]
            except KeyError:
                # If the value in the file is invalid, it will fall back to the default
                del data['king_placement_rule']

        # Filter out any keys from the file that are not fields in this dataclass
        class_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in class_fields}

        return cls(**filtered_data)



