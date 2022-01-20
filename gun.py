from event import Event

class Gun:
    def __init__(self, crew=5, fireRate=20, weight=4, range=5, accuracy=10):
        self.crew = crew
        self.fireRate = fireRate #per hour
        self.fireSpeed = 60/fireRate
        self.weight = weight #thousand pounds
        self.range = range #miles
        self.accuracy = accuracy #meters variance
        self.loaded = True

    def doReload(self):
        self.loaded = True

    def reloadTime(self, crew):
        return self.fireSpeed * self.crew / len(crew)

    def reload(self, time, crew):
        return Event(time + self.reloadTime(crew), self.doReload, crew)

    def weight(self):
        return self.weight