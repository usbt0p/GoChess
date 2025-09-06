from src.domain.entities.board import Board
from src.domain.entities.game_state import GameState, GamePhase
from src.domain.entities.piece import Piece, Pawn, Knight, Bishop, Rook, Queen, King 

from src.domain.value_objects.piece_type import Color, PieceType
from src.domain.value_objects.position import Position

from src.domain.services.go_chess_engine import GoChessEngine
from src.domain.services.validators import CheckNowValidator


        
class Game:
    """Build a board with game state, pieces, configuration, rules and a GoChessEngine instance."""

    def __init__(self, config):
        # TODO use config to set up the game
        board = Board()
        self.config = config # TODO this must be its own type


        self.state = GameState(board, 
                               Color.WHITE, 
                               config.get("phase"))
        
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
            self.state.board.place_piece(Pawn(Color.WHITE), Position(6, i))
            self.state.board.place_piece(Pawn(Color.BLACK), Position(1, i))

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
            self.state.board.place_piece(piece_type(color), position)
    
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
        
        # depending on the game phase, we either place or move a piece
        
        if self.state.phase == GamePhase.PLACEMENT:
            prompt = f"\n{current_color.name.capitalize()}'s turn to place a piece:"
            print(prompt)

            piece, position = self.placement_prompt()
            placed = self.engine.place_piece(piece, position)

        elif self.state.phase == GamePhase.MOVEMENT:

            # TODO in reality, we would await for input here, managing time, timeouts and so on
            prompt = f"\n{current_color.name.capitalize()}'s turn to move:"
            print(prompt)
            from_pos = Position.from_algebraic(input(f"From: "))
            to_pos = Position.from_algebraic(input(f"To: "))
            moved = self.engine.move_piece(from_pos, to_pos)
        

        # at the end 
        self.state.switch_player()

        # TODO check end conditions, if check then check checkmate
        # stalemate: no valid moves left for any piece of the current player

    def placement_prompt(self): 
        """Prompt the user for piece placement."""

        st = "Pieces: P, R, N, B, Q, K (ex.: Nb3): "
        algebraic = input(st).strip()
        # divide into piece type and position
        algebraic_piece, algebraic_position = algebraic[0].upper(), algebraic[1:].lower()
        match algebraic_piece:
            case 'P': piece_type = PieceType.PAWN
            case 'R': piece_type = PieceType.ROOK
            case 'N': piece_type = PieceType.KNIGHT
            case 'B': piece_type = PieceType.BISHOP
            case 'Q': piece_type = PieceType.QUEEN
            case 'K': piece_type = PieceType.KING
            case _: raise ValueError("Invalid piece type")
        
        piece = Piece.create(piece_type, self.state.current_player_color)
        position = Position.from_algebraic(algebraic_position)
        return piece, position
    