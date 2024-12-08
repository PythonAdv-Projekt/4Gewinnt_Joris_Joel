from player import Player
import requests



class Player_Remote(Player):
    """ 
    Local Player Class (uses Methods of the Game directly).

    Inherits Methods an Attributes from Player Class

        Attributes:
            id (UUID): Unique identifier for the player.
            icon (str): The player's icon used in the game. (set during registration)
            board_width (int):  Number of Horizontal Elements 
            board_height (int): Number of Vertical Elements

        Methods:
        register_in_game(self) -> str
            Registers player in the game instance
        is_my_turn(self) -> bool
            Checks if its a players turn
        get_game_status(self)->dict
            gets the actual Status of the game
        make_move(self) -> int
            Player is promted to make move
        visualize(self) -> None
            Visualizes Player the game board
        celebrate_win(self) -> None
            player can celebrate if won
        
        """

    def __init__(self, api_url) -> None:
        """ 
        Initializes a local player.
        
        Parameters:
            game (Connect4): Instance of Connect4 game passed through kwargs.

        Returns:
            Nothing
        
       """
        # Initialize id and icon from the abstract Player class
        super().__init__()  

        # Saves Instance of game to Attribute self.game
        self.api_url = api_url
        
    def register_in_game(self) -> str:
        """
        Registers a player in the game and assigns the player an icon.

        Parameters:
            None

        Returns:
            str: The player's icon.

        """
        #Player registrates himself in the game by using the register_player Method of the Game
        registration = {"player_id": f"{self.id}"}
        response = requests.post(f"{self.api_url}/connect4/register", json = registration)
        response = response.json()

        self.icon = response.get("player_icon")
        if self.icon is None:
            raise ValueError("Failed to register the player in the game")
        
        return self.icon
        
    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.
        
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
        Gets the game's current status by using the get_status() Method of the Game.
        which contains:
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
        
        Parameters:
            None

        Returns:
            dict: Returns a Dictionary of the Actual Status of the Game
            
        """
        response = requests.get(f"{self.api_url}/connect4/status")
        if response.status_code == 200:
            response = response.json()
            return response
        else:
            return False
        
        
    def make_move(self) -> int:
        """ 
        Player gets Message to make a Move.
        The Move gets checked by using the Method check_move of the game and
        if the Move is valid ther will be returned the Column.

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

                #if check_move returns True, we check if the column has space left and the place the chip
                if response.status_code == 200:
                    print(f"{response}") 
                    return column
                    
                    # Find the lowest available row in the selected column
                    #for row in range(6,-1,-1):
                        #if self.game.Board[row, column] == 0: #Checking for an empty cell
                            #self.game.Board[row, column] = self.icon #Change cell from empty to the icon of the player
                            #print(f"Player {self.icon} placed a chip in column {column}")
                            #return column
                
                else:
                    # Invalid move, when check_move returns false
                    print(f"{response}")
                    print("bruh")

            except ValueError:
                # ValueError is generated when e.g. the inpust is not an integer.
                print("Invalid input: Please enter a number between 0-7")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        
        Parameters:
            None
        
        Returns:
            Nothing

        """

        #get current board by calling the get_board() Method
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
        
            

        