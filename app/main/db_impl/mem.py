storage = {}

def get_game(room_id):
    return storage.get(room_id, None)

def save_game(game):
    storage[game.room_id] = game
