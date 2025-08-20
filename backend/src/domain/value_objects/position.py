from dataclasses import dataclass
from ..exceptions.game_error import InvalidMoveError


@dataclass(frozen=True, repr=True)
class Position:
    """Represents a position on the board."""
    row: int
    col: int

    def algebraic(self) -> str:
        """Returns the algebraic notation of the position."""
        file = "abcdefgh"[self.col]
        rank = 8 - self.row
        return f"{file}{rank}"

    @classmethod
    def from_algebraic(cls, notation: str) -> "Position":
        """Creates a Position object from algebraic notation (e.g., 'e4').
        Useful as an alternative constructor.
        """
        if not (
            isinstance(notation, str)
            and len(notation) == 2
            and "a" <= notation[0] <= "h"
            and "1" <= notation[1] <= "8"
        ):
            raise InvalidMoveError(f"Invalid algebraic notation: {notation}")

        col = "abcdefgh".index(notation[0])
        row = 8 - int(notation[1])
        return cls(row, col)


if __name__ == "__main__":

    pos = Position(0, 0)
    print(pos)  # Output: Position(row=0, col=0)
    print(repr(pos))  # Output: Position(row=0, col=0)

    print(pos.algebraic())  # Output: a8
    pos2 = Position(7, 7)
    print(pos2.algebraic())  # Output: h1
    pos3 = Position(3, 4)
    print(pos3.algebraic())  # Output: e5

    # Example of the alternative constructor
    pos_from_alg = Position.from_algebraic("e5")
    print(f"Position from 'e5': {pos_from_alg}")
    print(f"Are pos3 and pos_from_alg the same? {pos3 == pos_from_alg}")
