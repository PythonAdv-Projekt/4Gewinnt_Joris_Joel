

from game import Connect4
from player import Player


class Player_Local(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, **kwargs) -> None:
        """ 
        Initialize a local player.
            Must Implement all Methods from Abstract Player Class

        Parameters:
            game (Connect4): Instance of Connect4 game passed through kwargs.
        
       
        """
        super().__init__()  # Initialize id and icon from the abstract Player class

        self.game = kwargs['game']
        
    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

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

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        Connect4.get_status()

        raise NotImplementedError(f"You need to write this code first")

    def get_game_status(self):
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
      
        """
        Connect4.get_status()

        raise NotImplementedError(f"You need to write this code first")

    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

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
                    #If the for-loop exits, it means that the column is full
                    print(f"Column {column} is already full. Choose another column.")
                else:
                    # Invalid move, when check_move returns false
                    print(f"Invalid move! Please try again.")
            except ValueError:
                # ValueError is generated when e.g. the inpust is not an integer.
                print("Invalid input: Please enter a number between 0-7")

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")


    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")