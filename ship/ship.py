from collections import defaultdict
import math
from gameManagement.vector import Vector
from ship.hull import Hull
from ship.engine import Engine, EngineOrder
from enum import Enum

DRAG = .95
CREW_WEIGHT = .5


class Experience(Enum):
    GUNNERY = 0
    REPAIR = 1
    BAILING = 2


class Jack:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def sample(self):
        return self.coeffs


class Ship:
    def __init__(self, name, engine, hull, guns, crew, officers, position, facing, jack):
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
        self.heading = facing  # range 0-2pi
        self.experience = defaultdict(lambda: 0)  # experience of the crew
        self.speed = 0
        self.sprite = None
        self.moveTarget = None
        self.shootTarget = None
        self.experience[Experience.GUNNERY] = .05
        self.crewAllocation = defaultdict(lambda: 1)
        self.reservedCrew = 0
        self.controller = None
        self.jack = jack
        self.autoPilot = False

    def __repr__(self):
        return self.name + " at " + str(self.position) + " facing " + str(self.heading) + " speed " + str(self.speed) + \
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
        self.heading = angle

    def move(self, timestep):
        self.speed += timestep * self.hull.efficiency * self.engine.power * self.engine.order.value \
                      / (3 * self.weight())
        self.speed = min(self.speed, self.hull.topSpeed)
        self.position += Vector(self.heading) * self.speed * timestep
        self.setFacing(self.heading + self.hull.rudderPosition * self.hull.turningSpeed * self.speed * timestep)
        self.speed *= DRAG**timestep

    def turnOrder(self, target, timestep):
        tVector = target - self.position
        # tVector = self.position - target
        tAngle = tVector.angle()
        dAngle = tAngle - self.heading
        dAngle %= 2 * math.pi
        if dAngle > math.pi:
            dAngle -= 2*math.pi
        target = dAngle / (.000000000000000000000000000001 + (self.speed * self.hull.turningSpeed * timestep))
        if dAngle < 0:
            self.hull.turningOrders(max(-1, target))
        else:
            self.hull.turningOrders(min(target, 1))

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
        self.reservedCrew = min(sum([g.crew for g in self.guns]),
                                self.crew * self.crewAllocation[Experience.GUNNERY]
                                    / sum([k for k in self.crewAllocation.values()]))
        for gun in self.guns:
            if gun.loaded:
                self.fire(gun, time)
            self.reload(gun, time)

    def doHull(self, time, timestep):
        bail = self.crewAllocation[Experience.BAILING]
        repair = self.crewAllocation[Experience.REPAIR]
        self.events += self.hull.bail(self.useCrew(int((self.crew - self.reservedCrew) * bail / (bail + repair))), time, timestep)
        self.events += self.hull.repair(self.useCrew(int((self.crew - self.reservedCrew) * bail / (bail + repair))), time, timestep)

    def jog(self, time, timestep):
        self.doGuns(time)
        self.doHull(time, timestep)

    def timeStep(self, timestep, time):
        # print(self)
        self.move(timestep)
        if self.autoPilot:
            self.goToTarget(self.moveTarget, timestep)
        self.hull.timeStep(timestep)
        self.jog(time, timestep)

    def hit(self, projectile):
        if type(hit := self.hull.hit(projectile.target - self.position, projectile.weight, self.heading)) is not bool:
            self.events += hit
            return True
        return False

    def weight(self):
        return self.hull.weight() + sum([gun.weight() for gun in self.guns]) + self.engine.weight() + self.crew * CREW_WEIGHT

    def sunk(self):
        return self.weight() >= self.hull.displacement

    @staticmethod
    def simpleShip(shipName='Ship'):
        return Ship(name=shipName, engine=Engine(), hull=Hull(200, 20000), guns=[], crew=100, officers={},
                    position=Vector(0, 0), facing=0, jack=Jack([1]))
