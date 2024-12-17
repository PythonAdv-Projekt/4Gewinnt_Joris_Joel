from player import Player
import requests
import numpy as np
import random


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
            None
        
       """
        # Initialize id and icon from the abstract Player class
        super().__init__()  

        # Saves api_url to attribute self.api_url
        self.api_url: str = api_url
        
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

    def get_game_status(self) -> dict:
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
                    return column
                    
                    
                
                else:
                    # Invalid move, when response returns other than status_code 200
                    print(f"{response}")
                    print("bruh")

            except ValueError:
                # ValueError is generated when e.g. the inpust is not an integer.
                print("Invalid input: Please enter a number between 0-7")

    def check_bot(self):
        column = self.bot()
        print(column)
        move = {"column": column, "player_id": f"{self.id}"}
        response = requests.post(f"{self.api_url}/connect4/make_move", json = move)

        ##if API request returns True, we return the column
        if response.status_code == 200:
            return column

    def bot(self) -> int:
        status = requests.get(f"{self.api_url}/connect4/status").json()
        active_player_icon = status.get("active_player")
        response = requests.get(f"{self.api_url}/connect4/board")
        if response.status_code == 200:
            board = response.json()
            board = board.get("board")
            board_np = np.array(board, dtype=object)
            rows , cols = board_np.shape

            #1. Checking for Winning or Blocking moves
            #horizontally
            for row in range(rows):
                for col in range(cols - 3):  # Look at 4-cell sequences
                    h_myself = 0
                    h_opponent = 0
                    h_free_col = None

                    for i in range(4):  # Check each cell in the 4-cell sequence
                        if board_np[row, col + i] == active_player_icon:
                            h_myself += 1
                        elif board_np[row, col + i] != 0: 
                            h_opponent += 1
                        else:  # Empty
                            h_free_col = col + i

                    # Check if there are 3 of the same chips and one free space
                    if h_myself == 3 and h_free_col is not None:  # Active player can win
                        if row == rows - 1 or board_np[row + 1, h_free_col] != 0:  # check if there is no 'air'
                            return h_free_col 

                    if h_opponent == 3 and h_free_col is not None:  # Opponent can win
                        if row == rows - 1 or board_np[row + 1, h_free_col] != 0:  # chekc if there is no 'air'
                            return h_free_col  # Block the opponent

            #vertically
            for col in range(cols):
                for row in range(rows - 3): 
                    v_myself = 0
                    v_opponent = 0

                    for i in range(4):  # Check each cell in the 4-cell sequence
                        if board_np[row + i, col] == active_player_icon:
                            v_myself += 1
                        elif board_np[row + i, col] != 0:
                            v_opponent += 1

                    if v_myself == 3 and board_np[row, col] == 0:  # Active player can win
                        return col 

                    if v_opponent == 3 and board_np[row, col] == 0:  # Opponent can win
                        return col  # Block the opponent

            #diagonally (left to right)
            for col in range(cols - 3):
                for row in range(rows - 3):
                    d_lr_myself = 0
                    d_lr_opponent = 0
                    d_lr_free_row, d_lr_free_col = None, None

                    for i in range(4):  # Check each cell in the diagonal
                        if board_np[row + i, col + i] == active_player_icon:
                            d_lr_myself += 1
                        elif board_np[row + i, col + i] != 0:
                            d_lr_opponent += 1
                        else:  # Empty
                            d_lr_free_row, d_lr_free_col = row + i, col + i

                    if d_lr_myself == 3 and d_lr_free_row is not None:
                        if d_lr_free_row == rows - 1 or board_np[d_lr_free_row + 1, d_lr_free_col] != 0:  # check that there's no 'air'
                            return d_lr_free_col  # Return column to place the chip

                    if d_lr_opponent == 3 and d_lr_free_row is not None:
                        if d_lr_free_row == rows - 1 or board_np[d_lr_free_row + 1, d_lr_free_col] != 0:  # check that there's no 'air'
                            return d_lr_free_col  # Block opponent

            # diagonally right to left
            for col in range(3, cols):
                for row in range(rows - 3):
                    d_rl_myself = 0
                    d_rl_opponent = 0
                    d_rl_free_row, d_rl_free_col = None, None

                    for i in range(4):  # Check each cell in the diagonal
                        if board_np[row + i, col - i] == active_player_icon:
                            d_rl_myself += 1
                        elif board_np[row + i, col - i] != 0:
                            d_rl_opponent += 1
                        else:  # Empty
                            d_rl_free_row, d_rl_free_col = row + i, col - i

                    if d_rl_myself == 3 and d_rl_free_row is not None:
                        if d_rl_free_row == rows - 1 or board_np[d_rl_free_row + 1, d_rl_free_col] != 0:  # check that there's no 'air'
                            return d_rl_free_col

                    if d_rl_opponent == 3 and d_rl_free_row is not None:
                        if d_rl_free_row == rows - 1 or board_np[d_rl_free_row + 1, d_rl_free_col] != 0:  # check that there's no 'air'
                            return d_rl_free_col  # Block opponent

            #2. Checking for pairs
            # horizontally           
            for row in range(rows):
                for col in range(cols - 2):
                    h_myself = 0
                    h_opponent = 0
                    free_cols = []  # Stores indices of free columns

                    for i in range(3):  # Check each cell in the 3-cell sequence
                        if board_np[row, col + i] == active_player_icon:
                            h_myself += 1
                        elif board_np[row, col + i] != 0:  # opponent
                            h_opponent += 1
                        else:  # Empty
                            free_cols.append(col + i)

                    # Active player has a pair and at least one free space
                    if h_myself == 2 and len(free_cols) > 0:
                        for free_col in free_cols:  # Check if the free space is valid
                            if row == rows - 1 or board_np[row + 1, free_col] != 0:  # no 'air'
                                return free_col  # Place chip to form a three-in-a-row

                    # Opponent has a pair and at least one free space
                    if h_opponent == 2 and len(free_cols) > 0:
                        for free_col in free_cols:  # Check if the free space is valid
                            if row == rows - 1 or board_np[row + 1, free_col] != 0:  # no 'air'
                                return free_col  # Block the opponent so he can't form 3-in-a-row
                            
            # vertically
            for col in range(cols):
                for row in range(rows - 2):  # Look at 3-cell vertical sequences
                    if board_np[row, col] == active_player_icon and board_np[row + 1, col] == active_player_icon:
                        if board_np[row + 2, col] == 0:  # check if there's free space on top
                            return col  # Place chip to form a three-in-a-row (column)

                    if board_np[row, col] != 0 and board_np[row + 1, col] != 0 and board_np[row, col] != active_player_icon:
                        if board_np[row + 2, col] == 0:  # Free space to block
                            return col  # Block the opponent
                        
            # diagonally (left to right)
            for col in range(cols - 2):
                for row in range(rows - 2): 
                    d_lr_myself = 0
                    d_lr_opponent = 0
                    free_row, free_col = None, None

                    for i in range(3):  # Check each 3-cell-sequences in the diagonal
                        if board_np[row + i, col + i] == active_player_icon:
                            d_lr_myself += 1
                        elif board_np[row + i, col + i] != 0:
                            d_lr_opponent += 1
                        else:
                            free_row, free_col = row + i, col + i

                    if d_lr_myself == 2 and free_row is not None:
                        if free_row == rows - 1 or board_np[free_row + 1, free_col] != 0:  # no 'air'
                            return free_col  # Form a three-in-a-row

                    if d_lr_opponent == 2 and free_row is not None:
                        if free_row == rows - 1 or board_np[free_row + 1, free_col] != 0:  # no 'air'
                            return free_col  # Block the opponent
                        
            # diagonally (right to left)
            for col in range(2, cols):  # start at column 3
                for row in range(rows - 2):
                    d_rl_myself = 0
                    d_rl_opponent = 0
                    free_row, free_col = None, None

                    for i in range(3):  # Check each 3-cell-sequences in the diagonal
                        if col - i >= 0:  #makes sure we stay in the board
                            if board_np[row + i, col - i] == active_player_icon:
                                d_rl_myself += 1
                            elif board_np[row + i, col - i] != 0:
                                d_rl_opponent += 1
                            else:
                                free_row, free_col = row + i, col - i

                    if d_rl_myself == 2 and free_row is not None:
                        if free_row == rows - 1 or board_np[free_row + 1, free_col] != 0:  # no air
                            return free_col  # to form a three-in-a-row

                    if d_rl_opponent == 2 and free_row is not None:
                        if free_row == rows - 1 or board_np[free_row + 1, free_col] != 0:  # no air
                            return free_col  # Block the opponent's 3-in-a-row
                        
            # 3. Move when none of the above two is the case and centre is free at the bottom

            if board_np[0, 3] == 0 and board_np[0,4] == 0:  # Checks if the two center columns are free at the bottom
                return random.randrange(3,5) #3 or 4 (random)
            if board_np[0, 4] == 0:  # center right column
                return 4
            if board_np[0, 3] == 0:  # center left column
                return 3
            
            # 4. Move when none of the above is the case (random move)
            valid_cols = [col for col in range(cols) if board_np[0, col] == 0]
            if valid_cols:
                return random.choice(valid_cols)

    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        By making a API request to the server. Board is formatted into the correct way to
        show in the CLI if status_code of response == 200.
        
        Parameters:
            None
        
        Returns:
            None

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
            print("\n")
        else:
            print(f"Request error {response.status_code}")

    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player

        Parameters:
            None

        Returns:
            None

        """
        response = requests.get(f"{self.api_url}/connect4/status")
        response = response.json()
        print(f"\033[1mCongrats! Player {response.get('winner').get('icon')}, you have won the Game!\033[0m")
        
            

        