

from game import Connect4
from player import Player



class Player_Local(Player):
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

    def __init__(self, **kwargs) -> None:
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
        self.game = kwargs['game']
        
    def register_in_game(self) -> str:
        """
        Registers a player in the game and assigns the player an icon.

        Parameters:
            None

        Returns:
            str: The player's icon.

        """
        #Player registrates himself in the game by using the register_player Method of the Game
        self.icon = self.game.register_player(self.id)
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
        if self.game.active_player["icon"] == self.icon and self.game.active_player["id"] == self.id:
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
        return self.game.get_status()
        
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
                
                #if check_move returns True, we check if the column has space left and the place the chip
                if self.game.check_move(column, self.id): 
                    
                    # Find the lowest available row in the selected column
                    for row in range(6,-1,-1):
                        if self.game.Board[row, column] == 0: #Checking for an empty cell
                            self.game.Board[row, column] = self.icon #Change cell from empty to the icon of the player
                            print(f"Player {self.icon} placed a chip in column {column}")
                            return column
                
                else:
                    # Invalid move, when check_move returns false
                    print(f"Invalid move! Please try again.")

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
        board = self.game.get_board()
        for row in board:
            # Check each element, printing "X" in red and "O" in green
            print(" | ".join(
                "\033[91mX\033[0m" if cell == "X" else
                "\033[92mO\033[0m" if cell == "O" else
                str(cell)
                for cell in row
            ))

    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player

        Parameters:
            None

        Returns:
            Nothing

        """

        #celebration = self.get_game_status()
        #test
        
        #winner_found = celebration.get("winner")
        #if winner_found !=None:
        print(f"Congrats! Player {self.game.active_player['icon']} you have won the Game now you can celebrate.")
        #print(celebration)
            

        