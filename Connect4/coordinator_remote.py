from time import sleep
from player_remote import Player_Remote
import requests


class Coordinator_Remote:
    """ 
    Coordinator for two Remote players
        - either playing over CLI or
        - playing over SenseHat

    This class manages the game flow, player registration, turn management, 
    and game status updates for Remote players using the Server.


    Attributes:
        api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        player (Player):    Local Instance of ONE remote Player (Raspi or Normal)
        sense (SenseHat):   Optional Local Instance of a SenseHat (if on Raspi)
    """

    def __init__(self, api_url: str) -> None:
        """
        Initialize the Coordinator_Remote.

        Parameters:
            api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        """
        self.api_url = api_url
        self.player = Player_Remote(api_url)

    def wait_for_second_player(self):
        """
        Waits for the second player to connect.

        This method checks the game status until the second player is detected,
        indicating that the game can start.
        """
        if self.player.get_game_status():
            print("waiting")
            return True
        return False
        

    def play(self):
        """ 
        Main function to play the game with two remote players.

        This method manages the game loop, where players take turns making moves,
        checks for a winner, and visualizes the game board.
        """
        self.player.register_in_game()
        if self.wait_for_second_player():
            
            self.player.visualize()
            self.player.make_move()
            #check for a winner
            if self.player.get_game_status().get("winner"):
                self.player.visualize()
                self.player.celebrate_win()
                return
            self.player.get_game_status()


# To start a game
if __name__ == "__main__":
    #api_url = "http://192.168.1.104:5000"  # Connect 4 API server URL
    
    # Uncomment the following lines to specify different URLs
    # pc_url = "http://172.19.176.1:5000"
    # pc_url = "http://10.147.97.97:5000"
    api_url = "http://127.0.1.1:5000"

    # Initialize the Coordinator
    c_remote = Coordinator_Remote(api_url=api_url)
    c_remote.play()