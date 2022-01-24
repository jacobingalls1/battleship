from event import Event, Projectile
from vector import Vector
import random
import math

class Gun:
    def __init__(self, ship=None, crew=5, fireRate=3, heft=4, shot=100, range=5, inaccuracy=5):
        self.crew = crew
        self.fireRate = fireRate #per hour
        self.fireSpeed = 60/fireRate #minutes per fire
        self.heft = heft #thousand pounds
        self.shot = shot #pounds
        self.range = range #miles
        self.inaccuracy = inaccuracy #percent variance
        self.loaded = True
        self.loading = False
        self.ship = ship

    def doReload(self):
        self.loaded = True
        self.loading = False

    def reloadTime(self, crew):
        return self.fireSpeed * self.crew / crew

    def reload(self, time, crew):
        if not crew or self.loading:
            return []
        self.loading = True
        return [Event(self.ship, time + self.reloadTime(crew), self.doReload, crew)]

    def travelTime(self, distance):
        return 1

    def aimTime(self):
        return 1

    def fire(self, time, position, target, gunnerySkill, angle=0): #requested angle of hit
        if not self.loaded or position is None:
            return []
        self.loaded = False
        distance = target.distance(position)
        variance = random.random() * 1 - ((1 - self.inaccuracy) * (1 - gunnerySkill))
        target += Vector(random.random()*2*math.pi) * variance
        return [Projectile(self.ship, time + self.travelTime(distance), target, self.shot)]

    def weight(self):
        return self.heft
