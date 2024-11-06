

from game import Connect4
from player import Player



class Player_Local(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, **kwargs) -> None:
        """ 
        Initializes a local player. And Inherits Attributes and Methods from Player Class.
        Methods are implemented in this class.
        

        Parameters:
            game (Connect4): Instance of Connect4 game passed through kwargs.

        Returns:
            Nothing
        
       
        """
        super().__init__()  # Initialize id and icon from the abstract Player class

        self.game = kwargs['game']
        
    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Parameters:
            None

        Returns:
            str: The player's icon.
        """
        
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

    def get_game_status(self):
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
        
        Parameters:
            None

        Returns:
            Nothing
      
        """
        
        return self.game.get_status()
        
    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

        Parameters:
            None

        Returns:
            int: The column chosen by the player for the move.
        """
        while True:
            try:
                column = int(input(f"Player {self.icon}, enter the column (0-7) where you wanna drop your chip"))
                if self.game.check_move(column, self.id): #if check_move returns True, we check if the column has space left and the place the chip
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
        """
        #celebration = self.get_game_status()
        
        
        #winner_found = celebration.get("winner")
        #if winner_found !=None:
        print(f"Congrats! Player {self.game.active_player['icon']} you have won the Game now you can celebrate.")
        #print(celebration)
            

        