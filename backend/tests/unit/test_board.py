import pytest
from src.domain.entities.board import Board
from src.domain.value_objects.position import Position
from src.domain.entities.piece import Piece
from src.domain.value_objects.piece_type import PieceType, Color




def test_board_initialization():
    board = Board(size=8)
    assert board.size == 8
    assert len(board._grid) == 8
    assert all(all(cell is None for cell in row) for row in board._grid)


def test_place_and_get_piece():
    board = Board()
    piece = Piece.create(PieceType.PAWN, Color.WHITE)
    pos = Position(0, 0)
    board.place_piece(piece, pos)
    assert board.get_piece(pos) is piece


def test_place_piece_invalid_position():
    board = Board()
    piece = Piece.create(PieceType.PAWN, Color.WHITE)
    with pytest.raises(ValueError):
        board.place_piece(piece, Position(-1, 0))
    with pytest.raises(ValueError):
        board.place_piece(piece, Position(0, 8))


def test_place_invalid_piece():
    board = Board()
    with pytest.raises(ValueError):
        board.place_piece(None, Position(0, 0))


def test_get_piece_empty_square():
    board = Board()
    assert board.get_piece(Position(0, 0)) is None


def test_get_piece_invalid_position():
    board = Board()
    assert board.get_piece(Position(-1, 0)) is None
    assert board.get_piece(Position(0, 8)) is None


def test_remove_piece():
    board = Board()
    piece = Piece.create(PieceType.PAWN, Color.WHITE)
    pos = Position(0, 0)
    board.place_piece(piece, pos)
    board.remove_piece(pos)
    assert board.get_piece(pos) is None


def test_remove_piece_from_empty_square():
    board = Board()
    pos = Position(0, 0)
    board.remove_piece(pos)
    assert board.get_piece(pos) is None


def test_remove_piece_invalid_position():
    board = Board()
    with pytest.raises(ValueError):
        board.remove_piece(Position(-1, 0))


def test_move_piece():
    board = Board()
    piece = Piece.create(PieceType.ROOK, Color.BLACK)
    from_pos = Position(3, 3)
    to_pos = Position(3, 5)
    board.place_piece(piece, from_pos)
    board.move_piece(from_pos, to_pos)
    assert board.get_piece(from_pos) is None
    assert board.get_piece(to_pos) is piece


def test_move_piece_from_empty_square():
    board = Board()
    from src.domain.exceptions.game_error import InvalidMoveError
    from_pos = Position(3, 3)
    to_pos = Position(3, 5)
    with pytest.raises(InvalidMoveError):
        board.move_piece(from_pos, to_pos)


def test_move_piece_to_invalid_position():
    board = Board()
    piece = Piece.create(PieceType.ROOK, Color.BLACK)
    from_pos = Position(3, 3)
    to_pos = Position(8, 5)
    board.place_piece(piece, from_pos)
    with pytest.raises(ValueError):
        board.move_piece(from_pos, to_pos)


def test_is_valid_position():
    board = Board()
    assert board.is_valid_position(Position(0, 0))
    assert board.is_valid_position(Position(7, 7))
    assert not board.is_valid_position(Position(-1, 0))
    assert not board.is_valid_position(Position(0, 8))
    assert not board.is_valid_position(Position(8, 8))


def test_board_copy():
    board = Board()
    piece = Piece.create(PieceType.QUEEN, Color.WHITE)
    pos = Position(4, 4)
    board.place_piece(piece, pos)

    new_board = board.copy()

    assert new_board is not board
    assert new_board.get_piece(pos) is piece

    # Modify original board and check if copy is unaffected
    board.remove_piece(pos)
    assert board.get_piece(pos) is None
    assert new_board.get_piece(pos) is piece

    # Modify copy and check if original is unaffected
    new_piece = Piece.create(PieceType.KING, Color.BLACK)
    new_pos = Position(0, 0)
    new_board.place_piece(new_piece, new_pos)
    assert new_board.get_piece(new_pos) is new_piece
    assert board.get_piece(new_pos) is None


def test_board_representation():
    board = Board(size=2)
    repr_str = str(board)
    expected_repr = "□ ▨\n▨ □"
    assert repr_str == expected_repr

    piece = Piece.create(PieceType.PAWN, Color.WHITE)
    board.place_piece(piece, Position(0, 0))
    repr_str = str(board)
    expected_repr_with_piece = "♟ ▨\n▨ □"
    assert repr_str == expected_repr_with_piece
