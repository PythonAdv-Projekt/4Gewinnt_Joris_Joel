import time

from sense_hat import SenseHat

from game import Connect4
from player_local import Player_Local


class Player_Raspi_Local(Player_Local):
    """ 
    Local Raspi Player 
        Same as Local Player -> with some changed methods
            (uses Methods of Game and SenseHat)
    """

    def __init__(self, game:Connect4, **kwargs) -> None:
        """ 
        Initialize a local Raspi player with a shared SenseHat instance.

        Parameters:
            game (Connect4): Game instance.
            sense (SenseHat): Shared SenseHat instance for all players. (if SHARED option is used)
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Local)
        super().__init__(**kwargs)

        # Extract the SenseHat instance from kwargs  (only if SHARED instance)
        # Remove Otherwise
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")

        self.color:list = None

    
    def register_in_game(self):
        """
        Register in game
            Set Player Icon 
            Set Player Color
        """
        # first do normal register
        self.icon = super().register_in_game()# call method of Parent Class (Player_Local)

        #setting color of Player
        if self.icon == "X":
            self.color = [255,0,0]
        if self.icon == "O":
            self.color = [0,255,0]        


        raise NotImplementedError(f"Override register_in_game of Player_Raspi_Locap")

    
    def visualize_choice(self, column:int)->None:
        """ 
        Visualize the SELECTION process of choosing a column
            Toggles the LED on the top row of the currently selected column

        Parameters:
            column (int):       potentially selected Column during Selection Process
        """

        self.sense.set_pixel(7,column,self.color[0],self.color[1],self.color[2])
        



        

    def visualize(self) -> None:
        """
        Override Visualization of Local Player
            Also Visualize on the Raspi 
        """

        # TODO: visualize Board on raspi

        # OPTIONAL: also visualize on CLI
        super().visualize()

        raise NotImplementedError(f" visualize on Raspi not yet implemented")

    def make_move(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            col (int):  Selected column (0...7)
        """

        while True:
            
            
            column = 0
            
            for event in self.sense.stick.get_events():
                if event.direction == "right":
                    if column < 7:
                        column += 1
                        self.visualize_choice(column)
                if event.direction == "left":
                    if column > 0:
                        column += 1
                        self.visualize_choice(column)
                if event.direction == "middle":

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

            
        
        
    
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Local Player
        """
        # TODO: Own Celebration Method on SenseHat

        # Optional: also do CLI celebration
        super().celebrate_win()