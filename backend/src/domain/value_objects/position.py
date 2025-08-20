from dataclasses import dataclass


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


if __name__ == "__main__":

    pos = Position(0, 0)
    print(pos)  # Output: Position(row=0, col=0)
    print(repr(pos))  # Output: Position(row=0, col=0)

    print(pos.algebraic())  # Output: a8
    pos2 = Position(7, 7)
    print(pos2.algebraic())  # Output: h1
    pos3 = Position(3, 4)
    print(pos3.algebraic())  # Output: e5