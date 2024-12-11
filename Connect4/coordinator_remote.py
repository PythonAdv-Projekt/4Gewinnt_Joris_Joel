from time import sleep
from player_remote import Player_Remote
from player_remote_raspi import Player_Raspi_Remote


class Coordinator_Remote:
    """ 
    Coordinator for two Remote players
        - either playing over CLI or
        - playing over SenseHat on Raspberry Pi

    This class manages the game flow, player registration, turn management, 
    and game status updates for Remote players using the Server.


    Attributes:
        api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        player (Player):    Local Instance of ONE remote Player (Raspi or Normal)
        sense (SenseHat):   Optional Local Instance of a SenseHat (if on Raspi)

    Methods:
        wait_for_second_player(self)
            Waits for the second player to connect
        play(self)
            Main function to playe the game
    """

    def __init__(self, api_url: str, on_raspi:bool) -> None:
        """
        Initializes the Coordinator_Remote.

        Parameters:
            api_url (str):      Address of Server, including Port
            on_raspi(bool):     True when player on raspi, False when not
        """
        self.api_url = api_url
        self.player = Player_Remote(api_url)
        
        if on_raspi:
            try:
                from sense_hat import SenseHat
                self.sense = SenseHat()
                self.player = Player_Raspi_Remote(api_url = api_url,sense = self.sense)
                
            except ImportError:
                raise RuntimeError("SenseHat Library not available. Make sure you're on a Raspberry Pi")

    def wait_for_second_player(self):
        """
        Waits for the second player to connect.

        This method checks the game status until the second player is detected,
        indicating that the game can start.

        Parameters:
            None
        
        Returns:
            Nothing
        """
        #the second player is registered when game_status gets returned
        if self.player.get_game_status():
            return True
        print("Waiting for other Connect4 Player to register..")
        #waiting for 2 seconds till next GET-Request
        sleep(2)
        return False
        

    def play(self):
        """ 
        Main function to play the game with two remote players.

        This method manages the game loop, where players take turns making moves,
        checks for a winner, and visualizes the game board.

        Parameters:
            None

        Returns:
            Nothing
        """
        #register the player into the game
        self.player.register_in_game()
        
        while True:
            #wait till booth player are registered
            if self.wait_for_second_player():
                #wait till it's the players turn
                if self.player.is_my_turn():
                    print("\033[1m" + "It's your turn!" + "\033[0m")
                    self.player.visualize()
                    self.player.make_move()
                    self.player.visualize()
                    print(self.player.get_game_status())
                    #checking for a Win
                    if self.player.get_game_status().get("winner"):
                        self.player.visualize()
                        self.player.celebrate_win()
                        return
                    print("Waiting on other Player to make his move...")
                #checking if the other player has won
                elif not self.player.is_my_turn():
                    if self.player.get_game_status().get("winner"):
                        self.player.visualize()
                        print("You have lost the Game!")
                        return
                    elif self.player.get_game_status().get("turn_number") == 2:
                        print("Your opponent registered to the game! Wait now till he made his first move.")
                        sleep(2)
                    

# To start a game
if __name__ == "__main__":
    #api_url = "http://192.168.1.104:5000"  # Connect 4 API server URL
    
    # Uncomment the following lines to specify different URLs
    # pc_url = "http://172.19.176.1:5000"
    # pc_url = "http://10.147.97.97:5000"
    #api_url = "http://127.0.0.1:5000"
    api_url = "http://192.168.43.4:5000"

    # Initialize the Coordinator
    c_remote = Coordinator_Remote(api_url=api_url, on_raspi=False) #on_raspi=True when player on Raspberry Pi with SenseHat
    c_remote.play()