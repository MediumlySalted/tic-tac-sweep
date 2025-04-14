
class Match:
    def __init__(self, game, host=True, connection=None):
        self.game = game
        self.host = host
        self.connection = connection
        self.wait_for_player = None

    def close_connection(self):
        print("\nConnection Closed")

class Matchmaker:
    def __init__(self):
        pass
        
    def find_servers(self):
        print("\nSearching for servers...")
        return [
            {"name": "Game 1", "address": "127.0.0.1", "port": 12345},
            {"name": "Game 2", "address": "192.168.0.5", "port": 54321}
        ]
