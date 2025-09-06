import sys
import os
from src.domain.entities.game_state import GamePhase


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.services.game import Game
from src.domain.value_objects.game_config import GameConfig
from src.domain.exceptions.game_error import InvalidMoveError, IllegalMoveError

def main():
    """Main function to run the console game."""

    print("--- Go-Chess Console ---")

    # Load configuration from a file
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'default.yaml')
    config = GameConfig.from_yaml(config_path)
    
    print(f"Phase: {config.phase.name}")
    print(f"\nConfiguration loaded: {config}\n")

    # You will need to update the Game class to accept a GameConfig object
    game = Game(config=config)
    
    flag = True
    while flag:
        try:
            game.step()
            print(game.state.board)
            phase = input(f"Change phase? Current phase is {game.state.phase.name}. (y/n): ")
            if phase.lower() == 'y':
                game.state.switch_phase()          

        except (InvalidMoveError, IllegalMoveError) as e:
            print(f"Invalid move: {e}, try again.")

        except KeyboardInterrupt as e:
            flag = False
        
        



if __name__ == "__main__":
    main()
