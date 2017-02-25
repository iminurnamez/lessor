

class Player(object):
    def __init__(self, player_dict=None):
        if player_dict is None:
            self.cash = 20000
        else:
            self.cash = player_dict["cash"]

    def save_to_dict(self):
        d = {}
        d["cash"] = self.cash
