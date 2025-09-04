from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState
from src.domain.entities.piece import Piece, Pawn, Knight, Bishop, Rook, Queen, King 

from src.domain.value_objects.piece_type import Color
from src.domain.value_objects.position import Position

from src.domain.services.go_chess_engine import GoChessEngine
from src.domain.services.validators import CheckNowValidator


        
class Game:
    """Build a board with game state, pieces, configuration, rules and a GoChessEngine instance."""

    def __init__(self, config):
        # TODO use config to set up the game
        board = Board()
        self.state = GameState(board, Color.WHITE)

        # TODO populate validator according to the config
        self.engine = GoChessEngine(self.state, [
            # TODO
            CheckNowValidator()
        ])
        self._build()

    def _build(self):
        """Builds the game with initial pieces and configurations."""

        # TODO this should actually build differents configurations but for now we will just use the standard one
        # insted of building a console-specific game

        # Place pieces on the board
        for i in range(8):  # placing pawns
            self.engine.place_piece(Pawn(Color.WHITE), Position(6, i))
            self.engine.place_piece(Pawn(Color.BLACK), Position(1, i))

        piece_positions = [
            (King, Color.WHITE, Position(7, 4)),
            (Queen, Color.WHITE, Position(7, 3)),
            (Bishop, Color.WHITE, Position(7, 2)),
            (Bishop, Color.WHITE, Position(7, 5)),
            (Knight, Color.WHITE, Position(7, 6)),
            (Knight, Color.WHITE, Position(7, 1)),
            (Rook, Color.WHITE, Position(7, 7)),
            (Rook, Color.WHITE, Position(7, 0)),
            (King, Color.BLACK, Position(0, 4)),
            (Queen, Color.BLACK, Position(0, 3)),
            (Bishop, Color.BLACK, Position(0, 2)),
            (Bishop, Color.BLACK, Position(0, 5)),
            (Knight, Color.BLACK, Position(0, 6)),
            (Knight, Color.BLACK, Position(0, 1)),
            (Rook, Color.BLACK, Position(0, 7)),
            (Rook, Color.BLACK, Position(0, 0))
        ]

        for piece_type, color, position in piece_positions:
            self.engine.place_piece(piece_type(color), position)

        # testing normal movements and checks
        # TODO remove this in production
        # self.engine.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
        # self.state.switch_player() # TODO maybe this should be done within moving, or might cause problems
        # self.engine.move_piece(Position.from_algebraic("e7"), Position.from_algebraic("e5"))
        # self.state.switch_player() 
        # self.engine.move_piece(Position.from_algebraic("f2"), Position.from_algebraic("f4"))
        # self.state.switch_player()  
        # self.engine.move_piece(Position.from_algebraic("d8"), Position.from_algebraic("h4"))
        # self.state.switch_player()

        # test en passant capture
        # self.engine.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
        # self.state.switch_player() 
        # self.engine.move_piece(Position.from_algebraic("a7"), Position.from_algebraic("a5"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("e4"), Position.from_algebraic("e5"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("d7"), Position.from_algebraic("d5"))
        # self.state.switch_player()

        # test castling on kingside
        # self.engine.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("g7"), Position.from_algebraic("g6"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("g1"), Position.from_algebraic("f3"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("g8"), Position.from_algebraic("f6"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("f1"), Position.from_algebraic("c4"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("f8"), Position.from_algebraic("g7"))
        # self.state.switch_player()

        # test castling on queenside
        # self.engine.move_piece(Position.from_algebraic("d2"), Position.from_algebraic("d4"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("d7"), Position.from_algebraic("d5"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("c1"), Position.from_algebraic("g5"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("c8"), Position.from_algebraic("g4"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("b1"), Position.from_algebraic("c3"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("b8"), Position.from_algebraic("c6"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("d1"), Position.from_algebraic("d2"))
        # self.state.switch_player()
        # self.engine.move_piece(Position.from_algebraic("d8"), Position.from_algebraic("d7"))
        # self.state.switch_player()

        # test promotion 
        self.engine.move_piece(Position.from_algebraic("e2"), Position.from_algebraic("e4"))
        self.state.switch_player()
        self.engine.move_piece(Position.from_algebraic("a7"), Position.from_algebraic("a5"))
        self.state.switch_player()
        self.engine.move_piece(Position.from_algebraic("e4"), Position.from_algebraic("e5"))
        self.state.switch_player()
        self.engine.move_piece(Position.from_algebraic("a5"), Position.from_algebraic("a4"))
        self.state.switch_player()
        self.engine.move_piece(Position.from_algebraic("e5"), Position.from_algebraic("e6"))
        self.state.switch_player()
        self.engine.move_piece(Position.from_algebraic("d7"), Position.from_algebraic("d5"))
        self.state.switch_player()
        self.engine.move_piece(Position.from_algebraic("e6"), Position.from_algebraic("f7"))
        self.state.switch_player()
        self.engine.move_piece(Position.from_algebraic("e8"), Position.from_algebraic("d7"))
        self.state.switch_player()


    def step(self):
        """Advance the game turn by turn."""
        
        # check whose turn it is
        current_color = self.state.current_player_color
        print(self.state.board)
            
        # TODO in reality, we would await for input here, managing time, timeouts and so on
        prompt = f"\n{current_color.name.capitalize()}'s turn:"
        print(prompt)
        from_pos = Position.from_algebraic(input(f"From: "))
        to_pos = Position.from_algebraic(input(f"To: "))
        
        # move the piece
        moved = self.engine.move_piece(from_pos, to_pos)
        # at the end 
        self.state.switch_player()

        # TODO check end conditions, if check then check checkmate
        # stalemate: no valid moves left for any piece of the current player

    
    