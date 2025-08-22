import pytest
from src.domain.entities.board import Board
from src.domain.value_objects.position import Position
from src.domain.entities.piece import Piece
from src.domain.value_objects.piece_type import PieceType
from src.domain.value_objects.color import Color


class MockPiece(Piece):
    def get_possible_moves(self, position: Position, board: 'Board') -> list[Position]:
        return []


def test_board_initialization():
    board = Board(size=8)
    assert board.size == 8
    assert len(board._grid) == 8
    assert all(all(cell is None for cell in row) for row in board._grid)


def test_place_and_get_piece():
    board = Board()
    piece = MockPiece(PieceType.PAWN, Color.WHITE)
    pos = Position(0, 0)
    board.place_piece(piece, pos)
    assert board.get_piece(pos) == piece
