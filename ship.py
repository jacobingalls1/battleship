from collections import defaultdict
import math
from vector import Vector
from gun import Gun
from event import Event
from hull import Hull
from engine import Engine, EngineOrder
from officer import Officer
from enum import Enum


DRAG = .95


class Experience(Enum):
    GUNNERY = 0


class Ship:
    def __init__(self, name, engine, hull, guns, crew, officers, position, facing):
        self.name = name
        self.events = []
        self.projectiles = []
        self.engine = engine
        self.engine.ship = self
        self.hull = hull
        self.hull.ship = self
        self.guns = guns
        for gun in self.guns:
            gun.ship = self
        self.crew = crew
        self.officers = officers
        self.position = position  # position dead center
        self.facing = facing  # range 0-2pi
        self.experience = defaultdict(lambda: 0)  # experience of the crew
        self.speed = 0
        self.sprite = None
        self.moveTarget = None
        self.shootTarget = None

    def __repr__(self):
        return self.name + " at " + str(self.position) + " facing " + str(self.facing) + " speed " + str(self.speed) + \
               " weight " + str(self.weight()) + ' target ' + str(self.moveTarget) + " engine " + str(self.engine.order)

    def findExperience(self, task):
        return self.experience[task]

    def reload(self, gun, time):
        self.events += gun.reload(time, self.useCrew(gun.crew))

    def fire(self, gun, time):
        self.projectiles += gun.fire(time, self.position, self.shootTarget, self.findExperience(Experience.GUNNERY))
        self.reload(gun, time)

    def useCrew(self, num):
        num = min(num, self.crew)
        self.crew -= num
        return num

    def doEvent(self, event):
        event.callBack()
        self.crew += event.crew

    def setFacing(self, angle):
        angle %= 2 * math.pi
        self.facing = angle

    def move(self, timestep):
        self.speed += timestep * self.hull.efficiency * self.engine.power * self.engine.order.value \
                      / (3 * self.weight())
        self.speed = min(self.speed, self.hull.topSpeed)
        self.position += Vector(self.facing) * self.speed * timestep
        self.setFacing(self.facing + self.hull.rudderPosition * self.hull.turningSpeed * self.speed * timestep)
        self.speed *= DRAG**timestep

    def turnOrder(self, target, timestep):
        tVector = target - self.position
        # tVector = self.position - target
        tAngle = tVector.angle()
        dAngle = tAngle - self.facing
        dAngle %= 2 * math.pi
        if dAngle > math.pi:
            dAngle -= 2*math.pi
        if dAngle < 0:
            self.hull.turningOrders(max(-1, dAngle / (self.speed * self.hull.turningSpeed * timestep)))
        else:
            self.hull.turningOrders(min(dAngle / (self.speed * self.hull.turningSpeed * timestep), 1))

    def goToTarget(self, target, timestep):
        if target is None:
            return
        distance = self.moveTarget.distance(self.position)
        if distance > 2 * self.hull.length:
            self.engine.engineOrder(EngineOrder.FULL_AHEAD)
        elif self.hull.length < distance < self.hull.length * 2:
            self.engine.engineOrder(EngineOrder.SLOW_ASTERN)
        else:
            self.engine.engineOrder(EngineOrder.STOP)
        if self.speed:
            self.turnOrder(target, timestep)

    def doGuns(self, time):
        for gun in self.guns:
            if gun.loaded:
                self.fire(gun, time)
            else:
                self.reload(gun, time)

    def jog(self, time):
        self.doGuns(time)

    def timeStep(self, timestep, time):
        # print(self)
        self.move(timestep)
        self.goToTarget(self.moveTarget, timestep)
        self.hull.leak()
        self.jog(time)

    def hit(self, projectile):
        if type(hit := self.hull.hit(projectile.target, projectile.weight)) is not bool:
            self.events += hit
            return True
        return False

    def weight(self):
        return self.hull.weight() + sum([gun.weight() for gun in self.guns]) + self.engine.weight() + self.crew/10

    def sunk(self):
        return self.weight() >= self.hull.displacement

    @staticmethod
    def simpleShip(shipName='Ship'):
        return Ship(name=shipName, engine=Engine(), hull=Hull(), guns=[], crew=100, officers={},
                    position=Vector(0, 0), facing=0)
