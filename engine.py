from enum import Enum


class EngineOrder(Enum):
    FULL_ASTERN = -3
    HALF_ASTERN = -2
    SLOW_ASTERN = -1
    STOP = 0
    SLOW_AHEAD = 1
    HALF_AHEAD = 2
    FULL_AHEAD = 3


POWER_TO_WEIGHT = 1


class Engine:
    def __init__(self, power=100):
        self.ship = None
        self.power = power # ft/s/s
        self.order = EngineOrder.STOP

    def engineOrder(self, order):
        self.order = order

    def weight(self):
        return self.power * POWER_TO_WEIGHT

        
