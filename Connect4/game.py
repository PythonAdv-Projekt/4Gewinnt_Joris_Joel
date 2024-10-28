import uuid
import random

import numpy as np


class Connect4:
    """
    Connect 4 Game Class

        Defines rules of the Game
            - what is a win
            - where can you set / not set a coin
            - how big is the playing field

        Also keeps track of the current game  
            - what is its state
            - who is the active player?

        Is used by the Coordinator
            -> executes the methods of a Game object
    """
    
    def __init__(self) -> None:
        """ 
        Init a Connect 4 Game
            - Create an empty Board
            - Create two (non - registered and empty) players.
            - Set the Turn Counter to 0
            - Set the Winner to False
            - etc.
        """
        self.Board = np.zeros((7,8),dtype=object)
        self.player1 = None
        self.player2 = None
        self.active_player = {"id": None, "icon": None}
        self.turncounter = 0
        self.winner = False
        raise NotImplementedError(f"You need to write this code first")

    """
    Methods to be exposed to the API later on
    """
    def get_status(self):
        """
        Get the game's status.
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
        """
        return f"Active Player: {self.active_player["icon"]}"

        raise NotImplementedError(f"You need to write this code first")

    def register_player(self, player_id:uuid.UUID)->str:
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon:       Player Icon (or None if failed)
        """
        if self.player1 is None:
            self.player1 = {"id": player_id, "icon": "X"}
            return "X"
        elif self.player2 is None:
            self.player2 = {"id": player_id, "icon": "O"}
            return "O"
        else:
            return None

    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board
        """
        #Return the current board
        return self.Board


    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        """
        #setting Active Player
        self.active_player["id"] = player_Id
        #Checking if Id matches with Player who wants to make a move
        if player_Id != self.player1["id"] and player_Id != self.player2["id"]:
            return False

        #Checking if column number is valid
        if column < 0 or column >= self.Board.shape[1]:
            return False
        
        #Cheching column has space left
        if self.Board[0, column] != 0: #Checks if the first row in the column isn't empty
            return False
        
        return True

    """ 
    Internal Method (for Game Logic)
    """
    def __update_status(self):
        """ 
        Update all values for the status (after each successful move)
            - active player
            - active ID
            - winner
            - turn_number
        """
        #Updating the Active Player and the ID
        if self.check_move == True:

            self.turncounter += 1 #Increase the turn counter by 1

            if self.active_player["id"] == self.player1["id"]:
                self.active_player["id"] = self.player2["id"]
                self.active_player["icon"] = self.player2["icon"]
            else:
                self.active_player["id"] = self.player1["id"]
                self.active_player["icon"] = self.player1["icon"]
    

    def __detect_win(self)->bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            True if there's a winner, False otherwise
        """  
        #save rows and cols into a variable
        rows , cols = self.Board.shape
        #Checking if there is a Winner Horizontaly
        for row in range(rows):
            for col in range(cols-3):
                if (self.Board[row,col] == self.active_player["icon"] and
                    self.Board[row,col + 1] == self.active_player["icon"] and
                    self.Board[row,col + 2] == self.active_player["icon"] and
                    self.Board[row,col + 3] == self.active_player["icon"]):
                    return True
        
        # Checking if there is a Winner Vertically
        for col in range(cols):
            for row in range(rows-3):
                if (self.Board[row,col] == self.active_player["icon"] and
                    self.Board[row + 1,col] == self.active_player["icon"] and
                    self.Board[row + 2,] == self.active_player["icon"] and
                    self.Board[row + 3,col] == self.active_player["icon"]):
                    return True
                
        #Checking if theres a winner diagonally


        raise NotImplementedError(f"You need to write this code first")