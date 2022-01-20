from armor import Armor

class Hull:
    def __init__(self, length=100, displacement=100, efficiency=1.0, topSpeed=15, turningSpeed=.005, armor=Armor(), ship=None):
        self.length = length #feet
        self.displacement = displacement #tons
        self.efficiency = efficiency #speed scaling factor
        self.topSpeed = topSpeed * 1.687810 #given in knots, converted to ft/s
        self.turningSpeed = turningSpeed #radians per foot travel
        self.rudderPosition = 0 #varies between -1 and 1 positive for port
        self.armor = armor
        self.ship = ship

    def turningOrders(self, rudder):
        self.rudderPosition = rudder

    def hit(self, position, angle):  # position in 0 <= x,y <= 1 portion of hull
        pass

    def weight(self):
        return (.5 + self.armor.weight()) * self.length


