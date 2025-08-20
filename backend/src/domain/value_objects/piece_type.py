from enum import Enum, auto

class Color(Enum):
    WHITE = 0
    BLACK = 1

class PieceType(Enum):
    PAWN = 0
    KNIGHT = auto()
    BISHOP = auto()
    ROOK = auto()
    QUEEN = auto()
    KING = auto()

    @property
    def algebraic(self) -> str:
        """
        Returns the character for algebraic notation.
        Returns an empty string for PAWN, as is standard.
        """
        if self == PieceType.PAWN:
            return ""
        # For other pieces, use the first letter of their name, except for KNIGHT.
        return "N" if self == PieceType.KNIGHT else self.name[0]
    
if __name__ == "__main__":
    # Example usage
    print(PieceType.PAWN.algebraic)  # Output: ""
    print(PieceType.KNIGHT.algebraic)  # Output: "N"
    print(PieceType.BISHOP.algebraic)  # Output: "B"
    print(PieceType.ROOK.algebraic)  # Output: "R"
    print(PieceType.QUEEN.algebraic)  # Output: "Q"
    print(PieceType.KING.algebraic)  # Output: "K"

    print(PieceType.PAWN)  # Output: PieceType.PAWN
    print(PieceType.KNIGHT)  # Output: PieceType.KNIGHT
    print(PieceType.BISHOP)  # Output: PieceType.BISHOP
