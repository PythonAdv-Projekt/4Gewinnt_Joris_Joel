import socket                                               # to get own IP
from flask import Flask, request, jsonify                   # for api
from flask_swagger_ui import get_swaggerui_blueprint        # for swagger documentation

# local includes
from game import Connect4


class Connect4Server:
    """
    Connect4Server: A Flask-based API server for playing Connect 4.

    This server provides endpoints to manage a game of Connect 4, including player registration,
    retrieving game status, viewing the board, and making moves. It also includes a Swagger UI.

    Attributes:
        game (Connect4): Instance of the Connect 4 game containing game logic and rules.
        app (Flask): Flask application instance managing the server.

    Endpoints:
        /: Provides a welcome message.
        /connect4/status: Retrieves the current game status.
        /connect4/register: Allows a new player to register.
        /connect4/board: Returns the current game board state.
        /connect4/make_move: Allows a player to make a move.

    Swagger Configuration:
        URL: '/swagger/connect4/'
        Static JSON File: '/static/swagger.json'

    Methods:
        setup_routes():
                Defines API endpoints and their logic.
        run(debug, host, port):
                Starts the Flask server.
    """

    def __init__(self) -> None:
        """
        Initializes the Connect4Server instance.

        Sets up the Connect 4 game instance, Flask server, Swagger UI configuration,
        and API endpoints.

        Parameters:
        None

        Returns:
        None
        """

        self.game: Connect4 = Connect4()  # Connect4 game instance
        self.app: Flask = Flask(__name__)  # Flask app instance

        # Swagger UI Configuration
        SWAGGER_URL = '/swagger/connect4/'
        API_URL = '/static/swagger.json'  # This should point to your static swagger.json file
        
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={  # Swagger UI config overrides
                'app_name': "Connect 4 API",
                'layout': "BaseLayout"  # You can choose other layouts
            }
        )

        # Register the Swagger UI blueprint
        self.app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


        # Define API routes within the constructor
        self.setup_routes()

    def setup_routes(self) -> None:
        """
        Defines API routes for the Connect 4 server.

        Endpoints include:
            - /connect4/status: Retrieve game status.
            - /connect4/register: Register a new player.
            - /connect4/board: Get the current board state.
            - /connect4/make_move: Make a move in the game.
        
        Parameters:
        None

        Returns:
        None
        """

        # Overall Description
        @self.app.route('/')
        def index():
            return "Welcome to the Connect 4 API!"



        # 1. Expose get_status method
        @self.app.route('/connect4/status', methods=['GET'])
        def get_status():
            status = self.game.get_status()
            if self.game.player1 and self.game.player2:
                return jsonify({"active_player": status.get("active_player"), 
                                "active_id": status.get("active_id"),
                                "winner":status.get("winner"),
                                "turn_number":status.get("turn number")}), 200
            else:
                return jsonify({"status": "false"}), 400


        # 2. Expose register_player method
        @self.app.route('/connect4/register', methods=['POST'])
        def register_player():
            data = request.get_json()
            player_id = data.get("player_id")

            if not player_id:
                return jsonify({"message": "no player_id provided"}), 400
            
            else:
                registration = self.game.register_player(player_id)
                return jsonify({"player_icon": registration}), 200


        # 3. Expose get_board method
        @self.app.route('/connect4/board', methods=['GET'])
        def get_board():
            board = self.game.get_board().tolist()
            return jsonify({"board": board})


            

        # 4. Expose move method
        @self.app.route('/connect4/make_move', methods=['POST'])
        def make_move():
            data = request.get_json()
            column = data.get("column")
            player_id = data.get("player_id")

            #saving the icon from the player who made the move, because if check_move is true, it's gonna change the active_player
            for player in [self.game.player1, self.game.player2]:
                if player["id"] == player_id:
                    player_icon = player["icon"]
            
            if self.game.check_move(column, player_id):
                #Find the lowest available row in the selected column
                    for row in range(6,-1,-1):
                        if self.game.Board[row, column] == 0: #Checking for an empty cell
                            self.game.Board[row, column] = player_icon #Change cell from empty to the icon of the player who made the move
                            self.game.update_status()
                            #print(f"Player {self.icon} placed a chip in column {column}")
                            return jsonify({"column": column, "player_id": player_id}), 200
            else:
                return jsonify({"success": False}), 400


    def run(self, debug=True, host='0.0.0.0', port=5000):
        # Get and display the local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Server is running on {local_ip}:{port}")

        # Start the Flask app
        self.app.run(debug=debug, host=host, port=port)



# If you want to run the server directly:
if __name__ == '__main__':
    server = Connect4Server()  # Initialize the Connect4Server
    server.run()               # Start the Flask app