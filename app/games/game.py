


class Game():

    def __init__(self, room_id):
        self.room_id = room_id
        self.player_count = 0

        # id to name
        self.players = {}
        self.host_player = None


    def room_id(self):
        return self.room_id
    
    def game_name(self):
        raise NotImplementedError