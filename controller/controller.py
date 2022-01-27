from abc import ABC
import math
import ship.ship
from gameManagement.vector import Vector
from ship.engine import EngineOrder
from gameManagement.game import Flag

class Controller:
    def __init__(self, ship):
        self.ship = ship
        self.ship.controller = self
        self.target = None

    def allocateCrew(self):
        raise NotImplementedError

    def update(self, flags, time, timestep):
        self.ship.jog(time, timestep)
        self.ship.crewAllocation[ship.ship.Experience.GUNNERY], \
            self.ship.crewAllocation[ship.ship.Experience.REPAIR], \
            self.ship.crewAllocation[ship.ship.Experience.BAILING] = self.allocateCrew()
        if not flags:
            return


class CartesianController(Controller, ABC):
    def __init__(self, ship):
        super().__init__(ship)
        self.ship.autopilot = True

    def shootingTarget(self, flags):
        raise NotImplementedError

    def pilotingTarget(self, flags):
        raise NotImplementedError

    def update(self, flags, time, timestep):
        super().update(flags, time, timestep)
        self.ship.shootTarget = self.shootingTarget(flags)
        self.ship.moveTarget = self.pilotingTarget(flags)


class PolarController(Controller, ABC):
    def rudderOrders(self, flags):
        raise NotImplementedError

    def engineOrders(self, flags):
        raise NotImplementedError

    def shootingOrders(self, flags):
        raise NotImplementedError

    def update(self, flags, time, timestep):
        flags = [Flag((f.position - self.ship.position).polar(), f.jack) for f in flags]
        for f in flags:
            f.position.theta -= self.ship.heading
        self.ship.hull.turningOrders(self.rudderOrders(flags))
        self.ship.engine.engineOrder(self.engineOrders(flags))
        shooting = self.shootingOrders(flags)
        shooting.theta += self.ship.heading
        self.ship.shootTarget = shooting.cartesian()


class BasicDescartes(CartesianController):
    def allocateCrew(self):
        return 1, 1, 1

    def shootingTarget(self, flags):
        if not flags:
            return self.ship.position
        return flags[0].position

    def pilotingTarget(self, flags):
        if not flags:
            return Vector(1000, 1000)
        direction = self.ship.position - flags[0].position
        return direction.rotate(1) + flags[0].position


class BasicPolar(PolarController):
    def allocateCrew(self):
        return 1, 1, 1

    def rudderOrders(self, flags):
        pos = flags[0].position
        diff = pos.theta
        if abs(diff) < 1:
            return diff
        return diff / abs(diff)

    def engineOrders(self, flags):
        pos = flags[0].position
        diff = min(300, pos.r) // 100
        if abs(pos.theta - math.pi) < math.pi / 2:
            diff = -diff
        return EngineOrder(diff)

    def shootingOrders(self, flags):
        pos = flags[0].position
        return pos
