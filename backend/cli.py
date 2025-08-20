import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState
from src.domain.value_objects.color import Color
from src.domain.services.go_chess_engine import GoChessEngine
from src.domain.value_objects.position import Position
from src.domain.entities.piece import Piece
from src.domain.value_objects.piece_type import PieceType


class ConsolePiece(Piece):
    """A console representation of a piece."""

    # def __str__(self):
    #     char = self.type.name[0]
    #     return char.upper() if self.color == Color.WHITE else char.lower()

    def get_possible_moves(self, position, board):
        pass

    def __str__(self):
        '''Use the unicode chess character for the piece in the console'''
        
        chess_set = '♙♘♗♖♕♔♟♞♝♜♛♚'
        # assuming the background is black... so white pieces are actually black
        if self.color == Color.WHITE:
            return chess_set[self.type.value + 6]
        else:
            return chess_set[self.type.value]


def main():
    """Main function to run the console game."""
    board = Board()
    game_state = GameState(board, Color.WHITE)
    engine = GoChessEngine(game_state, [])

    print("--- Go-Chess Console ---")
    print("Phase: PLACEMENT")

    # Simple placement phase for demonstration
    
    print("\nGame ready. This is a skeleton. Implement further interactions.")

    engine.place_piece(ConsolePiece(PieceType.KING, Color.WHITE), Position(7, 4))
    engine.place_piece(ConsolePiece(PieceType.QUEEN, Color.WHITE), Position(7, 3))
    engine.place_piece(ConsolePiece(PieceType.BISHOP, Color.WHITE), Position(7, 2))
    engine.place_piece(ConsolePiece(PieceType.BISHOP, Color.WHITE), Position(7, 5))
    engine.place_piece(ConsolePiece(PieceType.KNIGHT, Color.WHITE), Position(7, 6))
    engine.place_piece(ConsolePiece(PieceType.KNIGHT, Color.WHITE), Position(7, 1))
    engine.place_piece(ConsolePiece(PieceType.ROOK, Color.WHITE), Position(7, 7))
    engine.place_piece(ConsolePiece(PieceType.ROOK, Color.WHITE), Position(7, 0))

    for i in range(8):  # placing pawns
        engine.place_piece(ConsolePiece(PieceType.PAWN, Color.WHITE), Position(6, i))

    engine.place_piece(ConsolePiece(PieceType.KING, Color.BLACK), Position(0, 4))
    engine.place_piece(ConsolePiece(PieceType.QUEEN, Color.BLACK), Position(0, 3))
    engine.place_piece(ConsolePiece(PieceType.BISHOP, Color.BLACK), Position(0, 2))
    engine.place_piece(ConsolePiece(PieceType.BISHOP, Color.BLACK), Position(0, 5))
    engine.place_piece(ConsolePiece(PieceType.KNIGHT, Color.BLACK), Position(0, 6))
    engine.place_piece(ConsolePiece(PieceType.KNIGHT, Color.BLACK), Position(0, 1))
    engine.place_piece(ConsolePiece(PieceType.ROOK, Color.BLACK), Position(0, 7))
    engine.place_piece(ConsolePiece(PieceType.ROOK, Color.BLACK), Position(0, 0))

    for i in range(8):  # placing pawns
        engine.place_piece(ConsolePiece(PieceType.PAWN, Color.BLACK), Position(1, i))

    print(board)
    engine.move_piece(Position(6, 4), Position(4, 4)) # e5
    print("\nAfter moving a piece:")
    print(board)

    


if __name__ == "__main__":
    main()
