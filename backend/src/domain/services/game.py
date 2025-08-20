from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState
from src.domain.value_objects.piece_type import Color
from src.domain.services.go_chess_engine import GoChessEngine
from src.domain.value_objects.position import Position
from src.domain.entities.piece import Piece
from src.domain.value_objects.piece_type import PieceType


class ConsolePiece(Piece):
    """A console representation of a piece."""

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
        
class Game:
    """Build a board with game state, pieces, configuration, rules and a GoChessEngine instance."""

    def __init__(self, config):
        # TODO use config to set up the game
        self.board = Board()

        self.state = GameState(self.board, Color.WHITE)

        # TODO populate validator according to the config
        self.engine = GoChessEngine(self.state, [])
        self._build()

    def _build(self):
        """Builds the game with initial pieces and configurations."""

        # TODO this should actually build differents configurations but for now we will just use the standard one
        # insted of building a console-specific game

        # Place pieces on the board
        for i in range(8):  # placing pawns
            self.engine.place_piece(ConsolePiece(PieceType.PAWN, Color.WHITE), Position(6, i))
            self.engine.place_piece(ConsolePiece(PieceType.PAWN, Color.BLACK), Position(1, i))

        piece_positions = [
            (PieceType.KING, Color.WHITE, Position(7, 4)),
            (PieceType.QUEEN, Color.WHITE, Position(7, 3)),
            (PieceType.BISHOP, Color.WHITE, Position(7, 2)),
            (PieceType.BISHOP, Color.WHITE, Position(7, 5)),
            (PieceType.KNIGHT, Color.WHITE, Position(7, 6)),
            (PieceType.KNIGHT, Color.WHITE, Position(7, 1)),
            (PieceType.ROOK, Color.WHITE, Position(7, 7)),
            (PieceType.ROOK, Color.WHITE, Position(7, 0)),
            (PieceType.KING, Color.BLACK, Position(0, 4)),
            (PieceType.QUEEN, Color.BLACK, Position(0, 3)),
            (PieceType.BISHOP, Color.BLACK, Position(0, 2)),
            (PieceType.BISHOP, Color.BLACK, Position(0, 5)),
            (PieceType.KNIGHT, Color.BLACK, Position(0, 6)),
            (PieceType.KNIGHT, Color.BLACK, Position(0, 1)),
            (PieceType.ROOK, Color.BLACK, Position(0, 7)),
            (PieceType.ROOK, Color.BLACK, Position(0, 0))
        ]

        for piece_type, color, position in piece_positions:
            self.engine.place_piece(ConsolePiece(piece_type, color), position)

    def step(self):
        """Advance the game state by one turn."""

        print(self.board)
        # check whose turn it is
        current_color = self.state.current_player_color
        
        # TODO in reality, we would await for input here, managing time, timeouts and so on
        prompt = f"\n{current_color.name.capitalize()}'s turn:"
        print(prompt)
        from_pos = Position.from_algebraic(input(f"From: "))
        to_pos = Position.from_algebraic(input(f"To: "))
        
        # move the piece
        self.engine.move_piece(from_pos, to_pos)
        # at the end 
        self.state.switch_player()

    
    