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
        kwargs['game'] = game
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
            self.color = (255,0,0)
            self.color_text = "red"
        if self.icon == "O":
            self.color = (0,255,0)  
            self.color_text = "green"    


        

    
    def visualize_choice(self, column:int)->None:
        """ 
        Visualize the SELECTION process of choosing a column
            Toggles the LED on the top row of the currently selected column

        Parameters:
            column (int):       potentially selected Column during Selection Process
        """
        print(column)
        #Clear previous selected column
        for col in range(8):
            self.sense.set_pixel(col, 0, (0,0,0))
        
        #Light up the selected Column
        self.sense.set_pixel(column,0,self.color)

    
    def visualize(self) -> None:
        """
        Override Visualization of Local Player
            Also Visualize on the Raspi 
        """
        #Visualzation for Sensehat
        board = self.game.get_board()
        pixel_matrix=[]

        for i in range(8):
            pixel_matrix.append((0,0,0))
        
        for row in range(7):
            for col in range(8):
                if row < 7 and col < 8:
                    if board[row, col] == 0:
                        pixel_matrix.append((0,0,0))
                    elif board[row, col] == "X":
                        pixel_matrix.append((255,0,0))
                    elif board[row, col] == "O":
                        pixel_matrix.append((0,255,0))
                    else:
                        pixel_matrix.append((0,0,0))
                

        self.sense.set_pixels(pixel_matrix)
        
        
        #Visualzation for CLI
        super().visualize()

        

    def make_move(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            col (int):  Selected column (0...7)
        """
        column = 0
        while True:
            self.sense.set_pixel(column,0,self.color)
            
            
            
            for event in self.sense.stick.get_events():
                
                print(f"Joystick event: {event.direction}")
                if event.direction == "right" and event.action =="pressed":
                    if column < 7:
                        print(event)
                        column += 1
                        self.visualize_choice(column)
                        time.sleep(0.1)
                if event.direction == "left" and event.action == "pressed":
                    if column > 0:
                        print(event)
                        column -= 1
                        self.visualize_choice(column)
                        time.sleep(0.1)
                if event.direction == "middle" and event.action == "pressed":
                    print(event)

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
                        red = (255, 0, 0)
                        white = (0, 0, 0)
                        red_cross_matrix = [
                                        white, white, white, red,   red,   white, white, white,
                                        white, white, white, red,   red,   white, white, white,
                                        white, white, white, red,   red,   white, white, white,
                                        red,   red,   red,   red,   red,   red,   red,   red,
                                        red,   red,   red,   red,   red,   red,   red,   red,
                                        white, white, white, red,   red,   white, white, white,
                                        white, white, white, red,   red,   white, white, white,
                                        white, white, white, red,   red,   white, white, white
                                    ]
                        self.sense.set_pixels(red_cross_matrix)
                        time.sleep(0.5)
                        self.visualize()
                        print(f"Invalid move! Please try again.")

            
        
        
    
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Local Player
        """
        self.sense.show_message(f"Player {self.color_text} won!", text_colour = self.color)

        #self.sense.load_image("c4e4385986fd571.png")
        #time.sleep(0.5)
        #self.sense.show_message(f"{self.game.active_player['icon']} won")

        # Optional: also do CLI celebration
        super().celebrate_win()