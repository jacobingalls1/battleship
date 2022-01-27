from ship.armor import Armor
import random
from gameManagement.event import Event

CREW_REPAIR = .1
CREW_BAIL = 1

def message():
    pass

class Hull:
    def __init__(self, length=100, displacement=10000, efficiency=10.0, topSpeed=30, turningSpeed=0.005, armor=Armor(), ship=None):
        self.length = length #feet
        self.beam = displacement / length / 5
        self.displacement = displacement #tons
        self.efficiency = efficiency #speed scaling factor
        self.topSpeed = topSpeed * 1.687810 #given in knots, converted to ft/s
        self.turningSpeed = turningSpeed #radians per foot travel
        self.rudderPosition = 0 #varies between -1 and 1 positive for port
        self.armor = armor
        self.ship = ship
        self.leakRate = 0 #tons per minute
        self.water = 0 #tons
        self.bailing = 0
        self.repairing = 0
        self.height = 50

    def turningOrders(self, rudder):
        self.rudderPosition = rudder

    def leak(self):
        self.water += self.leakRate

    def onShip(self, location, angle):
        print(location)
        if location.magnitude() > self.length / 2:
            return False
        location = location.rotate(-angle)
        print(location)
        # exit()
        if abs(location.x) < self.length and abs(location.y) < self.beam:  # check for miss within range
            return True
        return False

    def hit(self, location, weight, angle=0):  # position in 0 <= x,y <= 1 portion of hull
        if not self.onShip(location, angle):
            return False
        self.leakRate += weight/10 * random.random()
        print('HIT', self.ship, self.leakRate)
        return []

    def weight(self):
        return (.5 + self.armor.weight()) * self.length + self.water

    def bail(self, crew, time, timestep):
        if not crew:
            return []
        self.bailing += crew * CREW_BAIL * timestep
        return [Event(self.ship, time + timestep, message, crew)]

    def repair(self, crew, time, timestep):
        if not crew:
            return []
        self.repairing += crew * CREW_REPAIR * timestep
        return [Event(self.ship, time + timestep, message, crew)]

    def timeStep(self, timestep):
        self.leak()
        self.water = max(0, self.water - self.bailing * timestep)
        self.bailing = 0
        self.leakRate = max(0, self.leakRate - self.bailing * timestep)
        self.repairing = 0




