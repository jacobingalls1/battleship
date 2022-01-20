from collections import defaultdict
import math
from vector import Vector
from gun import Gun
from event import Event
from hull import Hull
from engine import Engine
from officer import Officer


DRAG = .95


class Ship:
    def __init__(self, engine=Engine(), hull=Hull(), guns=[], crew=0, officers={}, position=Vector(0, 0), facing=0):
        self.events = []
        self.engine = engine
        self.engine.ship = self
        self.hull = hull
        self.hull.ship = self
        self.guns = guns
        self.crew = crew
        self.officers = officers
        self.position = position
        self.facing = facing  # range 0-2pi
        self.experience = defaultdict(lambda: 0)
        self.speed = 0
        self.sprite = None

    def __repr__(self):
        return "Ship at " + str(self.position) + " facing " + str(self.facing) + " speed " + str(self.speed) + " weight " + str(self.weight()) + '\n'

    def useCrew(self, num):
        if num > self.crew:
            num = self.crew
        self.crew -= num
        return num

    def doEvent(self, event):
        event.callBack()
        self.crew += event.crew

    def setFacing(self, angle):
        if angle > 2*math.pi:
            angle -= 2*math.pi
        if angle < 0:
            angle += 2*math.pi
        self.facing = angle

    def move(self, timestep):
        self.position += Vector(self.facing) * self.speed * timestep
        self.setFacing(self.facing + self.hull.rudderPosition * self.hull.turningSpeed * self.speed * timestep)
        self.speed *= DRAG**timestep

    def timeStep(self, timestep):
        self.move(timestep)

    def turnOrder(self, target):
        tVector = target - self.ship.position
        tAngle = tVector.angle()
        dAngle = self.facing - tAngle
        if dAngle > math.pi:
            dAngle -= math.pi
        if dAngle < -math.pi:
            dAngle += math.pi
        if dAngle < 0:
            self.hull.turningOrders(max(-1, dAngle / self.speed * self.hull.turningSpeed))
        else:
            self.hull.turningOrders(min(dAngle / self.speed * self.hull.turningSpeed, 1))

    def nextTime(self):
        return self.events.queue[0].time

    def weight(self):
        return self.hull.weight() + sum([gun.weight() for gun in self.guns]) + self.engine.weight() + self.crew/10
