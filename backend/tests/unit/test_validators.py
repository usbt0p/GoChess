import pytest
from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState
from src.domain.entities.piece import Piece
from src.domain.value_objects.position import Position
from src.domain.value_objects.piece_type import Color, PieceType
from src.domain.services.validators import CheckNowValidator


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def validator():
    return CheckNowValidator()


def test_king_in_check_by_rook(validator: CheckNowValidator, board: Board):
    king = Piece.create(PieceType.KING, Color.WHITE)
    rook = Piece.create(PieceType.ROOK, Color.BLACK)
    king_pos = Position.from_algebraic("e1")
    rook_pos = Position.from_algebraic("e8")

    board.place_piece(king, king_pos)
    board.place_piece(rook, rook_pos)
    
    state = GameState(board, Color.WHITE)
    assert validator.validate(state, Color.WHITE) is True


def test_king_not_in_check(validator: CheckNowValidator, board: Board):
    king = Piece.create(PieceType.KING, Color.WHITE)
    rook = Piece.create(PieceType.ROOK, Color.BLACK)
    king_pos = Position.from_algebraic("e1")
    rook_pos = Position.from_algebraic("a8")

    board.place_piece(king, king_pos)
    board.place_piece(rook, rook_pos)

    state = GameState(board, Color.WHITE)
    assert validator.validate(state, Color.WHITE) is False


def test_king_in_check_by_pawn(validator: CheckNowValidator, board: Board):
    king = Piece.create(PieceType.KING, Color.WHITE)
    pawn = Piece.create(PieceType.PAWN, Color.BLACK)
    king_pos = Position.from_algebraic("e4")
    pawn_pos = Position.from_algebraic("d5")

    board.place_piece(king, king_pos)
    board.place_piece(pawn, pawn_pos)

    state = GameState(board, Color.WHITE)
    assert validator.validate(state, Color.WHITE) is True


def test_king_in_check_by_knight(validator: CheckNowValidator, board: Board):
    king = Piece.create(PieceType.KING, Color.WHITE)
    knight = Piece.create(PieceType.KNIGHT, Color.BLACK)
    king_pos = Position.from_algebraic("e4")
    knight_pos = Position.from_algebraic("f6")

    board.place_piece(king, king_pos)
    board.place_piece(knight, knight_pos)

    state = GameState(board, Color.WHITE)
    assert validator.validate(state, Color.WHITE) is True


def test_check_is_blocked(validator: CheckNowValidator, board: Board):
    king = Piece.create(PieceType.KING, Color.WHITE)
    blocking_piece = Piece.create(PieceType.ROOK, Color.WHITE)
    attacking_rook = Piece.create(PieceType.ROOK, Color.BLACK)

    king_pos = Position.from_algebraic("e1")
    blocker_pos = Position.from_algebraic("e4")
    attacker_pos = Position.from_algebraic("e8")

    board.place_piece(king, king_pos)
    board.place_piece(blocking_piece, blocker_pos)
    board.place_piece(attacking_rook, attacker_pos)

    state = GameState(board, Color.WHITE)
    assert validator.validate(state, Color.WHITE) is False


def test_no_king_on_board(validator: CheckNowValidator, board: Board):
    rook = Piece.create(PieceType.ROOK, Color.BLACK)
    rook_pos = Position.from_algebraic("e8")
    board.place_piece(rook, rook_pos)

    state = GameState(board, Color.WHITE)
    assert validator.validate(state, Color.WHITE) is False


def test_checkmate_is_also_check(validator: CheckNowValidator, board: Board):
    # Setup a simple checkmate scenario (back-rank mate)
    white_king = Piece.create(PieceType.KING, Color.WHITE)
    black_king = Piece.create(PieceType.KING, Color.BLACK)
    black_rook = Piece.create(PieceType.ROOK, Color.BLACK)

    board.place_piece(white_king, Position.from_algebraic("h1"))
    board.place_piece(Piece.create(PieceType.PAWN, Color.WHITE), Position.from_algebraic("g2"))
    board.place_piece(Piece.create(PieceType.PAWN, Color.WHITE), Position.from_algebraic("h2"))
    board.place_piece(black_king, Position.from_algebraic("a3"))
    board.place_piece(black_rook, Position.from_algebraic("a1"))

    state = GameState(board, Color.BLACK)
    state.switch_player() # White's turn
    
    assert validator.validate(state, Color.WHITE) is True


def test_discovered_check(validator: CheckNowValidator, board: Board):
    # Setup: White bishop moves to reveal a check from the white rook.
    black_king = Piece.create(PieceType.KING, Color.BLACK)
    white_rook = Piece.create(PieceType.ROOK, Color.WHITE)
    white_bishop = Piece.create(PieceType.BISHOP, Color.WHITE)

    board.place_piece(black_king, Position.from_algebraic("e8"))
    board.place_piece(white_rook, Position.from_algebraic("e1"))
    # Bishop is blocking the check
    board.place_piece(white_bishop, Position.from_algebraic("e4"))

    state_before_move = GameState(board, Color.WHITE)
    assert validator.validate(state_before_move, Color.BLACK) is False

    # Move bishop to reveal the check
    board.move_piece(Position.from_algebraic("e4"), Position.from_algebraic("g6"))

    state_after_move = GameState(board, Color.BLACK) # Black's turn
    assert validator.validate(state_after_move, Color.BLACK) is True


def test_pinned_piece_moves_exposing_king_with_bishop(validator: CheckNowValidator, board: Board):
    # Setup: A white knight is pinned to the king by a black bishop.
    white_king = Piece.create(PieceType.KING, Color.WHITE)
    white_knight = Piece.create(PieceType.KNIGHT, Color.WHITE)
    black_bishop = Piece.create(PieceType.BISHOP, Color.BLACK)

    king_pos = Position.from_algebraic("c1")
    knight_pos = Position.from_algebraic("d2")
    bishop_pos = Position.from_algebraic("f4")

    board.place_piece(white_king, king_pos)
    board.place_piece(white_knight, knight_pos)
    board.place_piece(black_bishop, bishop_pos)

    state_before_move = GameState(board, Color.WHITE)
    assert validator.validate(state_before_move, Color.WHITE) is False

    # Move the pinned knight, exposing the king to check.
    board.move_piece(knight_pos, Position.from_algebraic("e4"))

    state_after_move = GameState(board, Color.WHITE)
    assert validator.validate(state_after_move, Color.WHITE) is True
