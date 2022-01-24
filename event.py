from vector import Vector


class Event:
    def __init__(self, ship, time, callBack, crew=0):
        self.ship = ship
        self.time = time
        self.callBack = callBack
        self.crew = crew

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return "Event at " + str(self.time)


class Projectile:
    def __init__(self, ship, time=0, target=Vector(0, 0), weight=100):
        self.ship = ship
        self.time = time
        self.target = target
        self.weight = weight

    def __lt__(self, other):
        return self.time < other.time


    def __repr__(self):
        return "Projectile at " + str(self.time) + " " + str(self.target)