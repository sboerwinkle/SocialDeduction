import uuid

class Player():

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.name = ""