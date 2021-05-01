import os

impl = os.environ.get('SOCIAL_CACHE', 'redis')

if impl == 'redis':
    from .db_impl.redis import get_game, save_game
elif impl == 'mem':
    from .db_impl.mem import get_game, save_game
else:
    raise ValueError('env var "SOCIAL_CACHE" may only have values "redis" or "mem", not "%s"' % impl)
