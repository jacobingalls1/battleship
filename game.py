from display.display import Display
from queue import PriorityQueue
from event import Event
import time
from vector import Vector


TIME_STEP = 1
FRAME_LIMIT = 30


class Game:
    def __init__(self, ships=[]):
        self.ships = ships
        self.display = Display("game")
        for ship in self.ships:
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

    def timeStepEvent(self, time):
        return time, Event(None, time, self.timeStep)

    def sink(self, ship):
        self.ships.remove(ship)

    def updateShip(self, ship):
        ship.jog(self.time)
        for event in ship.events:
            if event.time < self.time:
                raise Exception(event, self.time)
            self.events.put((event.time, event))
        for projectile in ship.projectiles:
            if projectile.time < self.time:
                raise Exception(projectile, self.time)
            self.projectiles.put((projectile.time, projectile))
        if ship.sunk():
            self.sink(ship)
        ship.projectiles = []
        ship.events = []

    def timeStep(self):
        print(self.time)
        for ship in self.ships:
            ship.timeStep(TIME_STEP, self.time)
            self.updateShip(ship)
        self.events.put(self.timeStepEvent(self.time + TIME_STEP))
        self.display.drawFrame(self.ships)
        time.sleep(.1)

    def doProjectile(self, proj):
        print("PROJECTILE", self.time)
        isHit = False
        for ship in self.ships:
            isHit |= ship.hit(proj)
        self.updateShip(proj.ship)
        self.display.hit(self.time, proj.weight/1000, proj.target, TIME_STEP, Vector(proj.weight, proj.weight), isHit)

    def nextEvent(self):
        if self.projectiles.empty() or self.projectiles.queue[0][0] > self.events.queue[0][0]:
            e = self.events.get()[1]
            self.time = e.time
            if e.ship:
                e.ship.doEvent(e)
                self.updateShip(e.ship)
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
