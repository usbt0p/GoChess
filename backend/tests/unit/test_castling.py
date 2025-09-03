import pytest
from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState
from src.domain.entities.piece import King, Rook
from src.domain.value_objects.position import Position
from src.domain.value_objects.piece_type import Color
from src.domain.services.go_chess_engine import GoChessEngine


def test_kingside_castling():
    board = Board()
    state = GameState(board, Color.WHITE)
    engine = GoChessEngine(state, [])

    king = King(Color.WHITE)
    rook = Rook(Color.WHITE)

    # Place pieces for kingside castling
    king_pos = Position.from_algebraic("e1")
    rook_pos = Position.from_algebraic("h1")
    engine.place_piece(king, king_pos)
    engine.place_piece(rook, rook_pos)

    # Check if castling is a possible move
    possible_moves = king.get_possible_moves(king_pos, state)
    castling_move = Position.from_algebraic("g1")
    assert castling_move in possible_moves

    # Perform the castling move
    engine.move_piece(king_pos, castling_move)

    # Assertions
    assert board.get_piece(castling_move) is king
    assert board.get_piece(Position.from_algebraic("f1")) is rook
    assert board.get_piece(king_pos) is None
    assert board.get_piece(rook_pos) is None
    assert not state.castling_rights[Color.WHITE]['kingside']
    assert not state.castling_rights[Color.WHITE]['queenside']


def test_queenside_castling():
    board = Board()
    state = GameState(board, Color.WHITE)
    engine = GoChessEngine(state, [])

    king = King(Color.WHITE)
    rook = Rook(Color.WHITE)

    # Place pieces for queenside castling
    king_pos = Position.from_algebraic("e1")
    rook_pos = Position.from_algebraic("a1")
    engine.place_piece(king, king_pos)
    engine.place_piece(rook, rook_pos)

    # Check if castling is a possible move
    possible_moves = king.get_possible_moves(king_pos, state)
    castling_move = Position.from_algebraic("c1")
    assert castling_move in possible_moves

    # Perform the castling move
    engine.move_piece(king_pos, castling_move)

    # Assertions
    assert board.get_piece(castling_move) is king
    assert board.get_piece(Position.from_algebraic("d1")) is rook
    assert board.get_piece(king_pos) is None
    assert board.get_piece(rook_pos) is None
    assert not state.castling_rights[Color.WHITE]['kingside']
    assert not state.castling_rights[Color.WHITE]['queenside']

def test_castling_in_check():
    board = Board()
    state = GameState(board, Color.WHITE)
    engine = GoChessEngine(state, [])

    white_king = King(Color.WHITE)
    white_rook = Rook(Color.WHITE)
    white_rook2 = Rook(Color.WHITE)
    black_rook = Rook(Color.BLACK)

    # Place pieces for castling
    white_king_pos = Position.from_algebraic("e1")
    white_rook_pos = Position.from_algebraic("h1")
    white_rook2_pos = Position.from_algebraic("a1")
    black_rook_pos = Position.from_algebraic("e8")
    engine.place_piece(white_king, white_king_pos)
    engine.place_piece(white_rook, white_rook_pos)
    engine.place_piece(white_rook2, white_rook2_pos)
    engine.place_piece(black_rook, black_rook_pos)
    

    # Check that castling is not a possible move when in check
    possible_moves = white_king.get_possible_moves(white_king_pos, state)
    kingside_castling_move = Position.from_algebraic("g1")
    queenside_castling_move = Position.from_algebraic("c1")
    assert state.castling_rights[Color.WHITE]['kingside']
    assert state.castling_rights[Color.WHITE]['queenside']
    assert kingside_castling_move not in possible_moves
    assert queenside_castling_move not in possible_moves


    # Move black rook to a non-attacking position
    state.switch_player()
    engine.move_piece(black_rook_pos, Position.from_algebraic("a8"))
    state.switch_player()
    possible_moves = white_king.get_possible_moves(white_king_pos, state)
    assert kingside_castling_move in possible_moves
    assert queenside_castling_move in possible_moves
    # Perform queenside castling
    engine.move_piece(white_king_pos, queenside_castling_move)
    # Assertions
    assert board.get_piece(queenside_castling_move) is white_king
    assert board.get_piece(Position.from_algebraic("d1")) is white_rook2
    assert board.get_piece(white_king_pos) is None
    assert board.get_piece(white_rook2_pos) is None
    assert not state.castling_rights[Color.WHITE]['kingside']
    assert not state.castling_rights[Color.WHITE]['queenside']
    # Check that kingside castling is no longer possible
    possible_moves = white_king.get_possible_moves(queenside_castling_move, state)
    assert kingside_castling_move not in possible_moves
    assert queenside_castling_move not in possible_moves   

def test_castling_trough_check():
    board = Board()
    state = GameState(board, Color.WHITE)
    engine = GoChessEngine(state, [])

    white_king = King(Color.WHITE)
    white_rook = Rook(Color.WHITE)
    black_rook = Rook(Color.BLACK)

    # Place pieces for castling
    white_king_pos = Position.from_algebraic("e1")
    white_rook_pos = Position.from_algebraic("h1")
    black_rook_pos = Position.from_algebraic("f8")
    engine.place_piece(white_king, white_king_pos)
    engine.place_piece(white_rook, white_rook_pos)
    engine.place_piece(black_rook, black_rook_pos)

    # Check that castling is not a possible move when passing through check
    possible_moves = white_king.get_possible_moves(white_king_pos, state)
    kingside_castling_move = Position.from_algebraic("g1")
    assert state.castling_rights[Color.WHITE]['kingside']
    assert kingside_castling_move not in possible_moves

    # Move black rook to a non-attacking position
    state.switch_player()
    engine.move_piece(black_rook_pos, Position.from_algebraic("a8"))
    state.switch_player()
    possible_moves = white_king.get_possible_moves(white_king_pos, state)
    assert kingside_castling_move in possible_moves

    # Perform kingside castling
    engine.move_piece(white_king_pos, kingside_castling_move)

    # Assertions
    assert board.get_piece(kingside_castling_move) is white_king
    assert board.get_piece(Position.from_algebraic("f1")) is white_rook
    assert board.get_piece(white_king_pos) is None
    assert board.get_piece(white_rook_pos) is None
    assert not state.castling_rights[Color.WHITE]['kingside']
    assert not state.castling_rights[Color.WHITE]['queenside'] 




    
