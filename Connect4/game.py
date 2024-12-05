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

        Attributes:
            Board:np.ndarray
                Actual Gameboard
            player1:dict
                Player1 of the Game with Player ID and Icon
            player2:dict
                Player2 of the Game with Player ID and Icon
            active_player:dict
                contains Player ID and Icon of player which is active
            turncounter:int
                Number of turns
            winner:dict
                If theres a winner the dict of active_player is set to te Attribute

        Methods:
        get_status()
            gets the Status of the game who is active and is there a winner and which turn is it
        register_player(self, player_id:uuid.UUID)->str
            registers a player with the uuid and returns icon
        get_board()
            Returns the current state of the Board
        check_move(column:int, player_Id:uuid.UUID) -> bool
            Checks if a move of a certain player is legal and not and if its the players turn
        __update_status()
            Makes a Status Update of the game is used by the get_status() Method
        __detect_win(self)->bool
            Detects if there is a Winner or not is used by the __update_status() Method
        
        """
    
    def __init__(self) -> None:
        """ 
        Init a Connect 4 Game
            - Creates an empty Board
            - Creates two (non - registered and empty) players.
            - Sets the Turn Counter to 0
            - Sets the Winner to None
            - makes dict with keys "id" and "icon"
        Parameters:
            None
        
        """
        self.Board:np.ndarray = np.zeros((7,8),dtype=object)
        self.player1:dict = None
        self.player2:dict = None
        self.active_player:dict = {"id": None, "icon": None}
        self.turncounter:int = 0
        self.winner:dict = None
        
    """
    Methods to be exposed to the API later on
    """
    def get_status(self):
        """
        Uses the __update.status Method to Update the Status and returns the updatet Status.
        - Who is the Active Player.
        - Is there a Winner.
        - Which turn is it.

        Parameters:
            None

        Returns:
            dict: Returns a Dictionary of the Actual Status of the Game
        """
        
        self.__update_status()
        
        status = {
            "active_player": self.active_player["icon"],
            "winner": self.winner,
            "turn number": self.turncounter
        }
        
        return status

    def register_player(self, player_id:uuid.UUID)->str:
        """ 
        Registers a Player with a uuid  and Saves the Player to 
        a Attribut in form of a Dictionary which contains the player_id and the icon.
        
        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon (str):       Player Icon (or None if failed)
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
        Returns the Current State of the Board.

        Parameters:
            None

        Returns:
            board (np.ndarray): Returns the Board
        """

        #Return the current board
        return self.Board


    def check_move(self, column:int, player_Id:uuid.UUID) -> bool:
        """ 
        Checks the move of a certain player if it is legal.
        and checks if the Player is allowed to make a move.

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        
        Returns:
            bool: Returns a Bool if the Move is valid or not
        """
        
        #Checking if Id matches with Player who wants to make a move
        print(self.player1)
        print(self.player2)
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
        Ckecks if there is a Winner. 
        Updates the Values for the Status after a Succesfull move:
            - active player
            - active ID
            - winner
            - turn_number

        Parameters:
            None
        
        Returns:
            Nothing
        """

        #checking if there's a winner
        if not self.winner and self.__detect_win():
            self.winner = self.active_player

        if not self.winner:
            #Updating the Active Player, the ID and the turncounter
            if self.active_player["id"] == self.player1["id"]:
                self.turncounter += 1 
                self.active_player["id"] = self.player2["id"]
                self.active_player["icon"] = self.player2["icon"]

            else:
                self.turncounter += 1 
                self.active_player["id"] = self.player1["id"]
                self.active_player["icon"] = self.player1["icon"]
            
    

    def __detect_win(self)->bool:
        """ 
        Detect if there are 4 Pieces in one Row horizontally, vertically
        or diagonally. And returns a bool if so.

        Parameters:
            None
        
        Returns:
            bool: True if there's a winner, False otherwise
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
                    self.Board[row + 2,col] == self.active_player["icon"] and
                    self.Board[row + 3,col] == self.active_player["icon"]):
                    return True
                
        #Checking if theres a winner diagonally from left to right
        for col in range(cols-3):
            for row in range(rows-3):
                if (self.Board[row,col] == self.active_player["icon"] and
                    self.Board[row+1,col+1] == self.active_player["icon"] and
                    self.Board[row+2,col+2] == self.active_player["icon"] and
                    self.Board[row+3,col+3] == self.active_player["icon"]):
                    return True
        
        #Checking if there a winner diagonally from right to left
        for col in range(cols-1,2,-1):
            for row in range(rows-3):
                if (self.Board[row,col] == self.active_player["icon"] and
                    self.Board[row+1,col-1] == self.active_player["icon"] and
                    self.Board[row+2,col-2] == self.active_player["icon"] and
                    self.Board[row+3,col-3] == self.active_player["icon"]):
                    return True

        return False