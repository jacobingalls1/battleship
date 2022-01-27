from display.display import Display
from queue import PriorityQueue
from gameManagement.event import Event
import time
from gameManagement.vector import Vector, PolarVector
from ship.ship import Jack

TIME_STEP = 1
FRAME_LIMIT = 30
EARTH_RADIUS = 20902231


class Flag:
    def __init__(self, pos, jack):
        self.position = pos
        self.jack = jack

    def polar(self):
        self.position = self.position.polar()

    def cartesian(self):
        self.position = self.position.cartesian()

class Game:
    def __init__(self, controllers=[]):
        self.controllers = controllers
        self.display = Display("game")
        for c in self.controllers:
            ship = c.ship
            print(ship)
            ship.sprite = self.display.getShipSprite(ship)
            ship.sprite.update()
        print()
        print()
        print()
        self.time = -1
        self.events = PriorityQueue()
        self.projectiles = PriorityQueue()
        self.toDraw = []

    def getShipsInSight(self, ship):
        sight = ((EARTH_RADIUS + ship.hull.height)**2 - EARTH_RADIUS^2)**.5
        return [c.ship for c in self.controllers if c.ship is not ship and (c.ship.position - ship.position).magnitude() < sight]

    def getFlags(self, exclude=None):
        return [Flag(Vector(1000, 0), Jack([0]))]
        return [Flag(c.ship.position, c.ship.jack) for c in self.controllers if c is not exclude]

    def timeStepEvent(self, time):
        return time, Event(None, time, self.timeStep)

    def sink(self, controller):
        if controller in self.controllers:
            self.controllers.remove(controller)

    def updateShip(self, controller):
        ship = controller.ship
        otherShips = self.getFlags(controller)
        controller.update(otherShips, self.time, TIME_STEP)
        for event in ship.events:
            if event.time < self.time:
                raise Exception(event, self.time)
            self.events.put((event.time, event))
        for projectile in ship.projectiles:
            if projectile.time < self.time:
                raise Exception(projectile, self.time)
            self.projectiles.put((projectile.time, projectile))
        if ship.sunk():
            self.sink(controller)
        ship.projectiles = []
        ship.events = []

    def timeStep(self):
        for c in self.controllers:
            ship = c.ship
            print(ship)
            self.updateShip(c)
            ship.timeStep(TIME_STEP, self.time)
        self.events.put(self.timeStepEvent(self.time + TIME_STEP))
        self.display.drawFrame([c.ship for c in self.controllers])
        time.sleep(.1)

    def doProjectile(self, proj):
        print("PROJECTILE", self.time)
        isHit = False
        for c in self.controllers:
            ship = c.ship
            if isHit := ship.hit(proj):
                self.updateShip(c)
                break
        self.updateShip(proj.ship.controller)
        self.display.hit(self.time, proj.weight/10, proj.target, TIME_STEP, Vector(proj.weight/5, proj.weight/5), isHit)

    def nextEvent(self):
        if self.projectiles.empty() or self.projectiles.queue[0][0] > self.events.queue[0][0]:
            e = self.events.get()[1]
            self.time = e.time
            if e.ship:
                e.ship.doEvent(e)
                self.updateShip(e.ship.controller)
            else:
                e.callBack()
        else:
            p = self.projectiles.get()[1]
            self.time = p.time
            self.doProjectile(p)

    def playGame(self, timeLimit=-1):
        self.events.put(self.timeStepEvent(self.time + TIME_STEP))
        while self.time < timeLimit:
            self.nextEvent()
