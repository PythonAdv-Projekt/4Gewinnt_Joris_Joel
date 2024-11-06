

from game import Connect4
from player import Player
from player_local import Player_Local



class Coordinator_Local:
    """ 
    Coordinator for two Local players
    
    This class manages the game flow, player registration, turn management, 
    and game status updates for local players.


    Attributes:
        game (Connect4):    Local Instance of a Connect4 Game
        player1 (Player):   Local Instance of a Player 
        player2 (Player):   Local Instance of a Player

    Methods:
        def play(self)
            Runs the game until theres a winner

    """
    

    def __init__(self) -> None:
        """
        Initialize the Coordinator_Local with a Game and 2 Players

        Parameters:
            None

        Returns:
            Nothing

        """
        self.game = Connect4()
        self.player1 = Player_Local(game = self.game)
        self.player2 = Player_Local(game = self.game)
        
    

    def play(self):
        """ 
        Main function to run the game with two local players.
        
            This method handles player registration, turn management, 
            and checking for a winner until the game concludes.

        Parameters:
            None
        
        Returns:
            Nothing

        """

        #Registrationprocess

        # register Player 1
        self.player1.register_in_game()
        # register Player 2
        self.player2.register_in_game()


        
        #Defining which player is starting
        
        #Set Starting Player to player1
        self.game.active_player["id"] = self.player1.id
        self.game.active_player["icon"] = self.player1.icon



        
        #Main Loop to run the game

        while True:
            
            #Checking if its player1 turn
            if self.player1.is_my_turn():

                #if True the Board gets visualized and player1 can make his move 
                self.player1.visualize()
                self.player1.make_move()

                #player1 gets status and saves winner to winner_found
                status = self.player1.get_game_status()
                winner_found = status.get("winner")

                #If winner is not equal to None player1 has won the game
                if winner_found != None:
                    self.player1.visualize()
                    self.player1.celebrate_win()
                    return
                
            #checking if its player2 turn    
            if self.player2.is_my_turn():

                #if True the Board gets visualized and player2 can make his move
                self.player2.visualize()
                self.player2.make_move()

                #player2 gets status and saves winner to winner_found
                status = self.player2.get_game_status()
                winner_found = status.get("winner")

                #If winner is not equal to None player2 has won the game
                if winner_found != None:
                    self.player2.visualize()
                    self.player2.celebrate_win()
                    return
                

#gets called when running the coordinator_local-py
if __name__ == "__main__":

    #Initializes Object called coordinater and runs the Method play()
    coordinator = Coordinator_Local()
    coordinator.play()

    
