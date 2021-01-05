
class Game():

    def __init__(self, room_id):
        self.room_id = room_id
        self.player_count = 0

        # id to name
        self.players = []
        self.host_player = None

    def add_player(self, player_id, player_name):
        if self.player_count == 0:
            self.host_player = (player_id, player_name)
        
        self.player_count += 1
        self.players.append((player_id, player_name))
    
    def game_name(self):
        raise NotImplementedError