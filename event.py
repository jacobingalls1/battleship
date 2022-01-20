
class Event:
    def __init__(self, ship, time=0, callBack=lambda: None, crew=0):
        self.ship = ship
        self.time = time
        self.callBack = callBack
        self.crew = crew

    def __lt__(self, other):
        return self.time < other.time
