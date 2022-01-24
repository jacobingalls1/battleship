from ship import Ship
from game import Game
from vector import Vector
from gun import Gun

s1 = Ship.simpleShip('s1')
s2 = Ship.simpleShip('s2')
s1.position = Vector(-200, -200)
s1.facing = .3
s1.speed = 0
s1.moveTarget = Vector(200, -200)
s1.shootTarget = Vector(200, 200)
s1.hull.rudderPosition = 1
s1.guns.append(Gun(s1))
s2.position = Vector(200, 200)
s2.facing = .7
g = Game([s1, s2])
g.playGame(100)
