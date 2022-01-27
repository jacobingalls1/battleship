from gameManagement.game import Game
from gameManagement.vector import Vector
from ship.ship import Ship
from ship.gun import Gun
from controller.controller import BasicDescartes, BasicPolar
import random

# s1 = Ship.simpleShip('s1')
# s2 = Ship.simpleShip('s2')
# s1.position = Vector(-200, -200)
# s1.facing = .3
# s1.speed = 0
# s1.moveTarget = Vector(200, 150)
# s1.shootTarget = Vector(200, 200)
# s1.hull.rudderPosition = 1
# for i in range(1):
#     s1.guns.append(Gun(s1))
# s2.position = Vector(200, 200)
# s2.facing = .7
# g = Game([BasicController(s1), BasicController(s2)])
# g.playGame(1000)

numShips = 1
numGuns = 1

ships = [Ship.simpleShip('Ship %i'%i) for i in range(numShips)]
controllers = []
random.seed(0)
for ship in ships:
    ship.position = Vector(random.random()*500 - 250, random.random()*500 - 250)
    ship.heading = random.random() * 6.2
    for g in range(numGuns):
        ship.guns.append(Gun(ship, g / numGuns))
    controllers.append(BasicPolar(ship))
g = Game(controllers)
g.playGame(1000)

