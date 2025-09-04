import pytest
from unittest.mock import MagicMock

from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState
from src.domain.entities.piece import Pawn, Rook
from src.domain.value_objects.position import Position
from src.domain.value_objects.piece_type import Color, PieceType
from src.domain.services.go_chess_engine import GoChessEngine

def setup_engine_for_promotion(color: Color, pawn_pos_alg: str, promotion_piece: PieceType):
    """Helper function to set up the board for a promotion test."""
    board = Board()
    state = GameState(board, color)
    engine = GoChessEngine(state, [])
    
    pawn = Pawn(color)
    pawn_pos = Position.from_algebraic(pawn_pos_alg)
    engine.place_piece(pawn, pawn_pos)

    # Mock the promotion prompt to avoid waiting for user input
    engine.promotion_prompt = MagicMock(return_value=promotion_piece)
    
    return engine, state, pawn_pos

def test_white_pawn_promotes_to_queen():
    """Tests a standard white pawn promotion to a Queen."""
    engine, state, pawn_pos = setup_engine_for_promotion(Color.WHITE, "e7", PieceType.QUEEN)
    board = state.board
    
    promotion_pos = Position.from_algebraic("e8")
    engine.move_piece(pawn_pos, promotion_pos)
    
    promoted_piece = board.get_piece(promotion_pos)
    assert promoted_piece is not None
    assert promoted_piece.type == PieceType.QUEEN
    assert promoted_piece.color == Color.WHITE
    assert board.get_piece(pawn_pos) is None

def test_black_pawn_promotes_to_knight():
    """Tests a standard black pawn promotion to a Knight (underpromotion)."""
    engine, state, pawn_pos = setup_engine_for_promotion(Color.BLACK, "d2", PieceType.KNIGHT)
    board = state.board

    promotion_pos = Position.from_algebraic("d1")
    engine.move_piece(pawn_pos, promotion_pos)
    
    promoted_piece = board.get_piece(promotion_pos)
    assert promoted_piece is not None
    assert promoted_piece.type == PieceType.KNIGHT
    assert promoted_piece.color == Color.BLACK
    assert board.get_piece(pawn_pos) is None

def test_white_pawn_promotes_with_capture():
    """Tests pawn promotion that occurs on a capturing move."""
    engine, state, pawn_pos = setup_engine_for_promotion(Color.WHITE, "g7", PieceType.ROOK)
    board = state.board
    
    # Place a piece to be captured
    capture_pos = Position.from_algebraic("h8")
    engine.place_piece(Rook(Color.BLACK), capture_pos)
    
    # check valid moves are correct
    possible_moves = board.get_piece(pawn_pos).get_possible_moves(pawn_pos, state)
    assert possible_moves == [Position.from_algebraic("g8"), Position.from_algebraic("h8")]

    engine.move_piece(pawn_pos, capture_pos)
    
    promoted_piece = board.get_piece(capture_pos)
    assert promoted_piece is not None
    assert promoted_piece.type == PieceType.ROOK
    assert promoted_piece.color == Color.WHITE
    assert board.get_piece(pawn_pos) is None

def test_promotion_to_invalid_piece_type_raises_error():
    """Edge Case: Tests that attempting to promote to an invalid piece type raises an error."""
    engine, state, pawn_pos = setup_engine_for_promotion(Color.WHITE, "a7", PieceType.PAWN) # Invalid promotion
    
    promotion_pos = Position.from_algebraic("a8")
    
    with pytest.raises(ValueError, match="Invalid piece type for promotion"):
        engine.move_piece(pawn_pos, promotion_pos)

def test_pawn_move_to_non_promotion_square():
    """Edge Case: Tests that a regular pawn move does not trigger promotion logic."""
    engine, state, pawn_pos = setup_engine_for_promotion(Color.WHITE, "b6", PieceType.QUEEN)
    board = state.board
    
    move_pos = Position.from_algebraic("b7")
    engine.move_piece(pawn_pos, move_pos)
    
    moved_pawn = board.get_piece(move_pos)
    assert moved_pawn is not None
    assert moved_pawn.type == PieceType.PAWN
    # Check that the mocked prompt was not called
    engine.promotion_prompt.assert_not_called()

@pytest.mark.parametrize("promotion_piece", [
    PieceType.BISHOP,
    PieceType.ROOK,
])
def test_white_pawn_underpromotion(promotion_piece):
    """Tests underpromotion to pieces other than a Queen."""
    engine, state, pawn_pos = setup_engine_for_promotion(Color.WHITE, "c7", promotion_piece)
    board = state.board
    
    promotion_pos = Position.from_algebraic("c8")
    engine.move_piece(pawn_pos, promotion_pos)
    
    promoted_piece = board.get_piece(promotion_pos)
    assert promoted_piece is not None
    assert promoted_piece.type == promotion_piece
    assert promoted_piece.color == Color.WHITE