import pickle
import redis
import os



# redis database stuff
db = redis.Redis("localhost")
REDIS_TTL_S = 60*10 if os.environ.get('FLASK_DEV', False) else 60*60*12


def get_game(room_id):
    gm = db.get(room_id)
    if gm:
        return pickle.loads(gm)
    else:
        return None


def save_game(game):
    db.setex(game.room_id, REDIS_TTL_S, pickle.dumps(game))
