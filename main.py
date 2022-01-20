from ship import Ship
from game import Game
from vector import Vector

s1 = Ship()
s2 = Ship()
s1.position = Vector(-200, -200)
s1.facing = .3
s1.speed = 100
s1.hull.rudderPosition = 1
s2.position = Vector(200, 200)
s2.facing = .7
g = Game([s1, s2])
g.playGame(100)
