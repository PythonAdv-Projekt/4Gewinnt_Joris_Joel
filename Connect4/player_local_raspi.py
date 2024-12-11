import time
import random
from game import Connect4
from player_local import Player_Local


class Player_Raspi_Local(Player_Local):
    """ 
    Local Raspi Player 
        Same as Remote Player -> with some changed methods
        Uses Methods of SenseHat and interacts with gameobject

    Attributes:
        Inherits all Attributes from Local Player

        The following attributes are only for Local Raspi Player
        color (tuple): Color in RGB Format for the player
        sense (Sensehat): Sensehat instance for the player

    Methods:

        register_in_game(self)->None
            Uses Registration Method of Local Player and adds Color to the Raspi Player
        visualize_choice(self, column:int)->None
            Visualizes de Choice on the Raspberry Pi when moving the joystick
        visualize(self) -> None
            Visualizes the gameboard on the Raspberry Pi
        make_move(self) -> int
            Method to make a move on the Raspberry Pi
        celebrate_win(self) -> None
            Player celebrates if the game is won
        
    """

    def __init__(self, game:Connect4, **kwargs) -> None:
        """ 
        Initializes a local Raspi player with a shared SenseHat instance.
        Has a Game Object passed threw kwargs.

        Parameters:
            game (Connect4): Game instance.
            sense (SenseHat): Shared SenseHat instance for all players. (if SHARED option is used)

        Returns:
            Nothing
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.

        """
        # Initialize the parent class (Player_Local)
        kwargs['game'] = game
        super().__init__(**kwargs)

        # Extracts the SenseHat instance from kwargs
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")

        self.color:list = None
        

    
    def register_in_game(self):
        """
        Uses Registration Method of Local Player and adds a color to the Player dependend on
        the icon the registration reutrns.

        Parameters:
            None

        Returns:
            Nothing
        """
        # Calling Registration Method of Local Player to get Icon
        self.icon = super().register_in_game()

        #setting color of Player
        if self.icon == "X":
            self.color = (255,0,0)
            self.color_text = "red"
        if self.icon == "O":
            self.color = (0,255,0)  
            self.color_text = "green"    


        

    
    def visualize_choice(self, column:int)->None:
        """ 
        Visualizes the selection Process by toggling the LED on the sensehat.
        Only toggles on the top row on the sensehat

        Parameters:
            column (int):  selected Column during Selection Process
        
        Returns:
            Nothing
        """
        print(column)
        #Clear previous selected column
        for col in range(8):
            self.sense.set_pixel(col, 0, (0,0,0))
        
        #Light up the selected Column
        self.sense.set_pixel(column,0,self.color)

    
    def visualize(self) -> None:
        """
        Gets the gameboard of the Gameobject and visualizes on the sensehat.

        Parameters:
            None

        Returns:
            Nothing 
        """
        #Visualzation for Sensehat
        board = self.game.get_board()
        #Matrix for the sensehat
        pixel_matrix=[]

        # adds an empty row with the no color so that the matrix is 8x8
        for i in range(8):
            pixel_matrix.append((0,0,0))

        #for every Row and for every column in the gameboard there will be the colors set dependend on the icon and added to the pixel_matrix
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
                
        #pixel_matrix gets set on the sensehat
        self.sense.set_pixels(pixel_matrix)
        
        
        #Visualzation for CLI
        super().visualize()

        

    def make_move(self) -> int:
        """
        Ovverrides make_move method of Local Player. 
        Uses joystick to move left or right and select a column.
        If choice is made it gets checked by the check_move() method of the gameobject.

        Parameters:
            None

        Returns:
            col (int): the Selected column (0...7)
        """
        column = 0
        while True:
            self.sense.set_pixel(column,0,self.color)
            
            
            #watches the joystick events if left/right the method calls visualize_choice
            #if the joystick event is middle it calls the check_move method of the gameobject
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
        If the player has won there will be a Message on the sensehat and after that a Matrix rain effect.
        And it also gives the celebration on the CLI which is called from Local Player.

        Parameters:
            None

        Returns:
            Nothing
        """
        self.sense.show_message(f"Player {self.color_text} won!", text_colour = self.color, scroll_speed = 0.05)

        # Create a 8x8 grid of black (background)
        black = (0, 0, 0)
        matrix = [[black for _ in range(8)] for _ in range(8)]
        
        # Start the matrix rain effect
        while True:
            # Shift all rows down
            matrix = [row[:] for row in matrix]  # Copy current state
            
            # Randomly add green pixels to the top row (simulating falling rain)
            for col in range(8):
                if random.random() < 0.1:  # Adjust this value for more/less rain
                    matrix[0][col] = self.color  # New green pixel at the top
            
            # Shift all pixels down and remove the bottom row
            for row in range(7, 0, -1):
                for col in range(8):
                    matrix[row][col] = matrix[row - 1][col]

            # Clear the screen and update with new matrix
            self.sense.set_pixels([pixel for row in matrix for pixel in row])
            
            # Wait for a short time to simulate the fall of the rain
            time.sleep(0.1)

            if all(pixel == self.color for row in matrix for pixel in row):
                time.sleep(3)
                self.sense.clear()
                break

        
        

        # Optional: also do CLI celebration
        super().celebrate_win()