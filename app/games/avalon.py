from .game import Game

class Avalon(Game):

    def __init__(self, room_id):
        Game.__init__(self, room_id)


    def game_name(self):
        return "Avalon"



