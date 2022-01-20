from display.display import Display
from queue import PriorityQueue
from event import Event
import time


TIME_STEP = .1
FRAME_LIMIT = 30


class Game:
    def __init__(self, ships=[]):
        self.ships = ships
        self.display = Display("game")
        for ship in self.ships:
            print(ship)
            ship.sprite = self.display.getShipSprite(ship)
            ship.sprite.update()
        self.time = -1
        self.events = PriorityQueue()

    def timeStepEvent(self, time):
        return (time, Event(None, time, self.timeStep))

    def addEvents(self, ship):
        for event in ship.events:
            if event.time < self.time:
                raise Exception(event, self.time)
            self.events.put((event.time, event))
        ship.events = []

    def timeStep(self):
        for ship in self.ships:
            ship.timeStep(TIME_STEP)
            self.addEvents(ship)
        self.events.put(self.timeStepEvent(self.time + TIME_STEP))
        self.display.drawFrame(self.ships)
        time.sleep(.1)

    def nextEvent(self):
        e = self.events.get()[1]
        self.time = e.time
        if e.ship:
            e.ship.doEvent(e)
            self.addEvents(e.ship)
        else:
            e.callBack()

    def playGame(self, timeLimit=-1):
        self.events.put(self.timeStepEvent(self.time + TIME_STEP))
        while self.time < timeLimit:
            self.nextEvent()
