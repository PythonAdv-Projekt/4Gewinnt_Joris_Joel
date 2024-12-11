import time
import random
import requests
import numpy as np
from player_remote import Player_Remote


class Player_Raspi_Remote(Player_Remote):
    """ 
    Remote Raspi Player 
        Same as Remote Player -> with some changed methods
        Uses Methods of SenseHat and makes API-Requests to the Server

    Attributes:
        Inherits all Attributes from Remote Player

        The following attributes are only for Remote Raspi Player
        color (tuple): Color in RGB Format for the player
        sense (Sensehat): Sensehat instance for the player

    Methods:

        register_in_game(self)->None
            Uses Registration Method of Player_Remote but adds then a color to the player
        visualize_choice(self, column:int)->None
            Visualizes de Choice on the Raspberry Pi when moving the joystick
        visualize(self) -> None
            Visualizes the gameboard on the Raspberry Pi
        make_move(self) -> int
            Method to make a move on the Raspberry Pi
        celebrate_win(self) -> None
            Player celebrates if the game is won
        
        """

    def __init__(self, api_url:str, **kwargs) -> None:
        """ 
        Initialize a local Raspi player with a shared SenseHat instance.

        Parameters:
            api_url (str): Address of Server, including Port Bsp: http://10.147.17.27:5000
            sense (SenseHat): SenseHat instance for the player
        
        Returns:
            Nothing
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Local)
        kwargs['api_url']= api_url
        super().__init__(**kwargs)

        # Extracts the SenseHat instance from kwargs 
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")

        self.color:tuple = None
        

    
    def register_in_game(self)->None:
        """
        Rwgisters a player in the game by using the Method of Player Remote then assigns
        a colot to the player.

        Parameters:
            None

        Returns:
            Nothing
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
        Visualizes the selection Process by toggling the LED on the sensehat.
        Only toggles on the top row on the sensehat 

        Parameters:
            column (int): Column during Selection Process
        
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
        Makes an API-request to get the gameboard and visualizes it on the sensehat.

        Parameters:
            None

        Returns:
            Nothing
        """
       
        #Gets the gameboard from the server and makes it to a array
        response = requests.get(f"{self.api_url}/connect4/board")
        if response.status_code == 200:
            board = response.json().get("board")
            board = np.array(board).reshape(7, 8)
            
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
        
        #if the request failed the status code is printed
        else:
            print(f"Request error {response.status_code}")
                
        #pixel_matrix gets set on the sensehat
        self.sense.set_pixels(pixel_matrix)
        
        
        #Visualzation for CLI
        super().visualize()

        

    def make_move(self) -> int:
        """
        ovverrides make_move from Remote Player 
        Uses joystick to move left or right and select a column.
        If move made sends API request to valid the move if its valid the column is returned
        otherwise there will be a redcross on the sensehat.

        Parameters:
            None

        Returns:
            col (int): the selected column (0...7)
        """
        column = 0
        while True:
            self.sense.set_pixel(column,0,self.color)
            
            
            #watches the joystick events if left/right the method calls visualize_choice
            #if the joystick event is middle it sends an API request to valid the move
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
                    move = {"column": column, "player_id": f"{self.id}"}
                    response = requests.post(f"{self.api_url}/connect4/make_move", json = move)

                    #if API request returns True, we return the column
                    if response.status_code == 200:
                        print(f"{response}")
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
        And it also gives the celebration on the CLI which is called from Remote Player

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

        # CLI celebration
        super().celebrate_win()