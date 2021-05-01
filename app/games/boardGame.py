from flask_socketio import emit

from .game import Game


class BoardGame(Game):
    # Key for game objects not owned by any one player.
    # For now it's a string, but eventually maybe something the user can't pick as a name would be nice
    public_key = "table"

    def __init__(self, room_id):
        Game.__init__(self, room_id, 1, 1000) # min/max player counts might be optional, this is easier than checking
        self.objs = {}

    def setup_game(self, roles):
        pass

    def add_player(self, player_id, player_name, ready=False):
        ret = super().add_player(player_id, player_name, ready)
        if ret != None:
            ret.objs = {}
        return ret

    def write(self, msg, pred=None):
        payload = {'msg':msg}
        if pred != None:
            payload['targets'] = [player.name for player in self.players.values() if pred(player)]
        emit('message', payload, room=self.room_id)

    # You gotta implement `input`, it's like process_message but you can throw stuff
    def process_message(self, player_name, msg):
        try:
            self.input(player_name, msg)
        except Exception as e:
            self.write(f"Command caused exception: {e}", lambda x: x.name == player_name)

    def find_player(self, name):
        name = name.lower()
        ret = []
        for p in self.players.values():
            other = p.name.lower()
            if other.startswith(name):
                if other == name:
                    return p
                ret.append(p)
        if len(ret) == 1:
            return ret[0]
        if len(ret) == 0:
            raise Exception(f"Name {name} doesn't match any player")
        names = [r.name for r in ret]
        raise Exception(f"Name '{name}' is ambiguous among {names}")
