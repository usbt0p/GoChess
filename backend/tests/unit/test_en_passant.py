import pytest
from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState
from src.domain.entities.piece import Pawn
from src.domain.value_objects.position import Position
from src.domain.value_objects.piece_type import Color
from src.domain.services.go_chess_engine import GoChessEngine


def test_en_passant_capture():
    # Setup the board for en passant
    board = Board()
    state = GameState(board, Color.WHITE)
    engine = GoChessEngine(state, [])

    white_pawn = Pawn(Color.WHITE)
    black_pawn = Pawn(Color.BLACK)

    # 1. White pawn moves e2 -> e4
    engine.place_piece(white_pawn, Position.from_algebraic("e2"))
    engine.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
    state.switch_player()

    # 2. Black makes a non-pawn move
    engine.place_piece(black_pawn, Position.from_algebraic("h7"))
    engine.move_piece(Position.from_algebraic("h7"), Position.from_algebraic("h6"))
    state.switch_player()

    # 3. White pawn moves e4 -> e5
    engine.move_piece(Position.from_algebraic("e4"), Position.from_algebraic("e5"))
    state.switch_player()

    # 4. Black pawn moves d7 -> d5, making it vulnerable to en passant
    engine.place_piece(black_pawn, Position.from_algebraic("d7"))
    engine.move_piece(Position.from_algebraic("d7"), Position.from_algebraic("d5"))
    
    # After black's move, en passant should be possible for white
    assert state.en_passant_target is not None
    assert state.en_passant_target.algebraic() == "d6"
    state.switch_player()

    # 5. White pawn at e5 captures black pawn at d5 via en passant by moving to d6
    white_pawn_pos = Position.from_algebraic("e5")
    
    # Check if en passant is a possible move
    possible_moves = state.board.get_piece(white_pawn_pos).get_possible_moves(white_pawn_pos, state)
    en_passant_move = Position.from_algebraic("d6")
    assert en_passant_move in possible_moves

    # Perform the en passant move
    engine.move_piece(white_pawn_pos, en_passant_move)

    # Assertions
    # The white pawn should be at d6
    assert board.get_piece(en_passant_move) is white_pawn
    # The original white pawn position should be empty
    assert board.get_piece(white_pawn_pos) is None
    # The captured black pawn at d5 should be gone
    print(board)
    assert board.get_piece(Position.from_algebraic("d5")) is None
    # The en passant target should be cleared
    assert state.en_passant_target is None
