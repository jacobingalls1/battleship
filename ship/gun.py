from gameManagement.event import Event, Projectile
from gameManagement.vector import Vector
import random
import math

BLOCK_ANGLE = 1

class Gun:
    def __init__(self, ship, position, crew=5, fireRate=3, heft=4, shot=100, range=5, inaccuracy=.9):
        self.crew = crew
        self.fireRate = fireRate #per hour
        self.fireSpeed = 60/fireRate #minutes per fire
        self.heft = heft #thousand pounds
        self.shot = shot #pounds
        self.range = range #miles
        self.inaccuracy = inaccuracy # percent variance
        self.loaded = True
        self.loading = False
        self.ship = ship
        self.position = position # percentage from aft to forward

    def __repr__(self):
        return "Loading %s" % (str(self.loading))

    def doReload(self):
        self.loaded = True
        self.loading = False

    def reloadTime(self, crew):
        variance = .25
        return (variance * random.random() + 1 - variance) * self.fireSpeed * self.crew / crew

    def reload(self, time, crew):
        if not crew or self.loading:
            self.ship.crew += crew
            return []
        self.loading = True
        return [Event(self.ship, time + self.reloadTime(crew), self.doReload, crew)]

    def blocked(self, target):
        if abs(target.angle() - self.ship.heading) < BLOCK_ANGLE and self.position < .5:
            return True
        if abs(abs(target.angle() - self.ship.heading) - math.pi) < BLOCK_ANGLE and self.position > .5:
            return True
        return False

    def travelTime(self, distance):
        return 1

    def aimTime(self):
        return 1

    def fire(self, time, position, target, gunnerySkill, angle=0): #requested angle of hit
        if not self.loaded or not target or self.blocked(target):
            return []
        self.loaded = False
        distance = target.distance(position)
        variance = random.random() * (1 - ((1 - self.inaccuracy) * gunnerySkill)) / 10
        target += Vector(random.random()*2*math.pi) * variance * distance
        return [Projectile(self.ship, time + self.travelTime(distance), target, self.shot)]

    def weight(self):
        return self.heft
