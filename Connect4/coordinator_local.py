

from game import Connect4
from player import Player


class Coordinator_Local:
    """ 
    Coordinator for two Local players
    
    This class manages the game flow, player registration, turn management, 
    and game status updates for local players.


    Attributes:
        game (Connect4):    Local Instance of a Connect4 Game
        player1 (Player):   Local Instance of a Player 
        player2 (Player):   Local Instance of a Player
    """
    

    def __init__(self) -> None:
        """
        Initialize the Coordinator_Local with a Game and 2 Players
        """
        self.game = Connect4()
        self.player1 = Player()
        self.player2 = Player()
        
    

    def play(self):
        """ 
        Main function to run the game with two local players.
        
            This method handles player registration, turn management, 
            and checking for a winner until the game concludes.
            
            1. We have to registrate the Players
        """
        # register Player 1
        self.game.register_player(1)
        self.player1.register_in_game()
        # register Player 2
        self.game.register_player(2)
        self.player1.register_in_game()
        raise NotImplementedError(f"You need to write this code first")



if __name__ == "__main__":
    # Create a coordinator
    # play a game
    # TODO
    raise NotImplementedError(f"You need to write this code first")
