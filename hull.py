from armor import Armor
import random

class Hull:
    def __init__(self, length=100, displacement=1000, efficiency=1.0, topSpeed=30, turningSpeed=.005, armor=Armor(), ship=None):
        self.length = length #feet
        self.beam = displacement / length
        self.displacement = displacement #tons
        self.efficiency = efficiency #speed scaling factor
        self.topSpeed = topSpeed * 1.687810 #given in knots, converted to ft/s
        self.turningSpeed = turningSpeed #radians per foot travel
        self.rudderPosition = 0 #varies between -1 and 1 positive for port
        self.armor = armor
        self.ship = ship
        self.leakRate = 0 #tons per minute
        self.water = 0 #tons

    def turningOrders(self, rudder):
        self.rudderPosition = rudder

    def leak(self):
        self.water += self.leakRate

    def hit(self, location, weight, angle=0):  # position in 0 <= x,y <= 1 portion of hull
        if location.distance(self.ship.position) > self.length:
            return False
        # TODO check for miss within range
        # exit()
        self.leakRate += weight/10 * random.random()
        print('HIT', self.ship, self.leakRate)
        return []

    def weight(self):
        return (.5 + self.armor.weight()) * self.length + self.water


