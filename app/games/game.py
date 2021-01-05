import sys

class Player():

    def __init__(self, _id, name, ready=False):
        self.id = _id
        self.name = name
        self.ready = ready

    def info(self):
        return (self.id, self.name, self.ready)

    def to_dict(self):
        out_dict = {
            "id": self.id,
            "name": self.name,
            "ready": self.ready
        }
        return out_dict

class Game():

    def __init__(self, room_id, max_players):
        self.room_id = room_id
        self.player_count = 0
        self.max_players = max_players
        self.started = False
        self.players = {}
        self.host_player = None

    def add_player(self, player_id, player_name, ready=False):
        if self.player_count == 0:
            self.host_player = (player_id, player_name)
        
        self.player_count += 1
        self.players[player_id] = Player(player_id, player_name, ready)

    def remove_player(self, player_id, player_name):
        if self.player_count == 0:
            print("!!!!!!! ERROR !!!!! Cannot remove player from empty game.", file=sys.stderr)
            return
        if player_id not in self.players.keys():
            print("!!!!!!! ERROR !!!!! Could not find this player in game to remove.", file=sys.stderr)
            return

        self.player_count-=1
        del self.players[player_id]

    def get_players(self, is_dict=False):
        if(is_dict):
            return [x.to_dict() for x in self.players.values()]

        return self.players.values()
    
    def game_name(self):
        raise NotImplementedError