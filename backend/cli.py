import sys
import os
from src.domain.entities.game_state import GamePhase


# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.services.game import Game
from src.domain.value_objects.position import Position
from src.domain.exceptions.game_error import InvalidMoveError, IllegalMoveError

def main():
    """Main function to run the console game."""

    print("--- Go-Chess Console ---")
    print("Phase: PLACEMENT")

    # Simple placement phase for demonstration
    
    print("\nGame ready. This is a skeleton. Implement further interactions.")
    game = Game(
        config={
            "phase": GamePhase.PLACEMENT
            })  # Assuming config is a dictionary for now
    
    flag = True
    while flag:
        try:
            game.step()

        except (InvalidMoveError, IllegalMoveError) as e:
            print(f"Invalid move: {e}, try again.")

        except KeyboardInterrupt as e:
            flag = False



if __name__ == "__main__":
    main()
