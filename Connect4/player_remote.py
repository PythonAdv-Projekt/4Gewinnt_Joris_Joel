from player import Player
import requests


class Player_Remote(Player):
    """ 
    Local Player Class (uses Methods of the Game directly).

    Inherits Methods an Attributes from Player Class

        Attributes:
            Inherits all Attributes from Remote Player

            The following attributes are only for Remote Player
            api_url (str): Address of Server, including Port Bsp: http://10.147.17.27:5000

        Methods:
        register_in_game(self) -> str
            sends a API request to the server and returns the icon if succesful
        is_my_turn(self) -> bool
            sends a API request to the server and returns a boolean if succeded
        get_game_status(self)->dict
            sends the a API request to the server and returns a dictionary if succesful
        make_move(self) -> int
            Player can make a move and sends a API request for checking the move and returns the column if succesful
        visualize(self) -> None
            gets the board with an API request and Visualizes Player the game board
        celebrate_win(self) -> None
            checks if the player has won, if player has won it is printed to the CLI
        
        """

    def __init__(self, api_url, **kwargs) -> None:
        """ 
        Initializes a local player.
        
        Parameters:
            api_url (str):Address of Server, including Port Bsp: http://10.147.17.27:5000


        Returns:
            Nothing
        
       """
        # Initialize id and icon from the abstract Player class
        super().__init__()  

        # Saves api_url to attribute self.api_url
        self.api_url = api_url
        
    def register_in_game(self) -> str:
        """
        Makes an API request to server for registration assigns the icon to the player and 
        returns the icon if registration is succesful.

        Parameters:
            None

        Returns:
            str: The player's icon.
        
        Raises:
            ValueError: if the Registration wasnt successful

        """
        #Player registrates himself in the game by using API request 
        registration = {"player_id": f"{self.id}"}
        response = requests.post(f"{self.api_url}/connect4/register", json = registration)
        response = response.json()

        #Assigns Player a icon and if not sucessfull raises ValueError
        self.icon = response.get("player_icon")
        if self.icon is None:
            raise ValueError("Failed to register the player in the game")
        
        return self.icon
        
    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn via Api request if its the players turn returns True.
        
        Parameters:
            None

        Returns:
            bool: True if it's the player's turn, False otherwise.

        """
        #Checking if the Active Player in the Game is the same as the Attribute
        response = requests.get(f"{self.api_url}/connect4/status")
        response = response.json()

        if response.get("active_player") == self.icon:
            return True
        else:
            return False

    def get_game_status(self)->dict:
        """
        Gets the game's current status by making a Api request.
        which contains:
            - who is the active player
            - is there a winner
            - what turn is it
        
        Parameters:
            None

        Returns:
            dict: Returns a Dictionary of the Actual Status of the Game
            
        """
        #Getting the status of the game and returns dictionary of status if request succesfull
        response = requests.get(f"{self.api_url}/connect4/status")
        if response.status_code == 200:
            response = response.json()
            return response
        else:
            return False
        
        
    def make_move(self) -> int:
        """ 
        Player gets Message to make a Move. Player can choose between (0..7). When Player makes a move
        API request is send to the server for checking. If Move is succesfull column is returned otherwise
        response is printed.
        
        Parameters:
            None

        Returns:
            int: The column chosen by the player for the move.

        """


        while True:
            try:
                column = int(input(f"Player {self.icon}, enter the column (0-7) where you wanna drop your chip"))
                move = {"column": column, "player_id": f"{self.id}"}
                response = requests.post(f"{self.api_url}/connect4/make_move", json = move)

                ##if API request returns True, we return the column
                if response.status_code == 200:
                    print(f"{response}") 
                    return column
                    
                    
                
                else:
                    # Invalid move, when response returns other than status_code 200
                    print(f"{response}")
                    print("bruh")

            except ValueError:
                # ValueError is generated when e.g. the inpust is not an integer.
                print("Invalid input: Please enter a number between 0-7")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        By making a API request to the server. Board is formatted into the correct way to
        show in the CLI if status_code of response == 200.
        
        Parameters:
            None
        
        Returns:
            Nothing

        """

        #get current board by making API rewuest to the server
        response = requests.get(f"{self.api_url}/connect4/board")
        if response.status_code == 200:
            board = response.json()
            board = board.get("board")
            for row in board:

            # Check each element, printing "X" in red and "O" in green
                print(" | ".join(
                    "\033[91mX\033[0m" if cell == "X" else
                    "\033[92mO\033[0m" if cell == "O" else
                    str(cell)
                    for cell in row
                ))
        else:
            print(f"Request error {response.status_code}")

    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player

        Parameters:
            None

        Returns:
            Nothing

        """
        response = requests.get(f"{self.api_url}/connect4/status")
        response = response.json()
        print(f"Congrats! Player {response.get('winner').get('icon')}, you have won the Game!")
        
            

        