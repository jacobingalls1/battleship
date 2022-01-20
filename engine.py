from enum import Enum


class EngineOrder(Enum):
    FULL_ASTERN = -3
    HALF_ASTERN = -2
    SLOW_ASTERN = -1
    STOP = 0
    SLOW_AHEAD = 1
    HALF_AHEAD = 2
    FULL_AHEAD = 3


POWER_TO_WEIGHT = 10


class Engine:
    def __init__(self, power=1):
        self.ship = None
        self.power = power # ft/s/s

    def engineOrder(self, order):
        self.ship.speed += self.ship.hull.efficiency * self.power * order.value / (3 * self.ship.weight())
        self.ship.speed = min(self.ship.speed, self.ship.hull.topSpeed)

    def weight(self):
        return self.power * POWER_TO_WEIGHT

        
