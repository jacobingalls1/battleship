import pygame as pg
from display.shipSprite import ShipSprite
import math
from display.animator import Animator
from gameManagement.vector import Vector

SCREEN_SIZE = (1000, 1000)
SCREEN_BORDERS = ((-500, -500), (500, 500))
margin = 100
pg.init()

class Display:
    def __init__(self, name='battleship'):
        self.screen = pg.display.set_mode(SCREEN_SIZE)
        pg.display.set_caption(name)
        self.animator = Animator()
        self.dims = [SCREEN_BORDERS[0][0], SCREEN_BORDERS[0][1], SCREEN_BORDERS[1][0], SCREEN_BORDERS[1][1]]

    def getShipSprite(self, ship):
        return ShipSprite(ship)

    def doDims(self, toDraw):
        xn, xx = min([p.x for p in toDraw]), max([p.x for p in toDraw])
        yn, yx = min([p.y for p in toDraw]), max([p.y for p in toDraw])
        rect = [min(SCREEN_BORDERS[0][0], xn - margin), min(SCREEN_BORDERS[0][1], yn - margin),
                max(SCREEN_BORDERS[1][0], xx + margin), max(SCREEN_BORDERS[1][1], yx + margin)]
        if rect[2] - rect[0] > rect[3] - rect[1]:
            rect[3] = rect[1] + rect[2] - rect[0]
        else:
            rect[2] = rect[0] + rect[3] - rect[1]
        for c in range(4):
            self.dims[c] = (self.dims[c] + rect[c]) / 2


    def drawObject(self, surface, position, size, rotation=0):
        rect = self.dims
        xPos = (position.x - rect[0]) / (rect[2] - rect[0])
        yPos = (position.y - rect[1]) / (rect[3] - rect[1])
        xPos *= SCREEN_SIZE[0]
        yPos *= SCREEN_SIZE[1]
        scale = SCREEN_SIZE[0] / (rect[2] - rect[0])
        surf = pg.transform.rotate(
            pg.transform.scale(surface, (int(scale * size.x), int(scale * size.y))),
            180 * (2 * math.pi - rotation) / math.pi)
        xPos -= surf.get_size()[0] / 2
        yPos -= surf.get_size()[1] / 2
        self.screen.blit(surf, (xPos, yPos))

    def drawShip(self, ship):
        #the ship sprite is as long as the ship in feet
        self.drawObject(ship.sprite.surf, ship.position, Vector(ship.sprite.width, ship.sprite.height), ship.heading)

    def drawWater(self):
        self.screen.fill((0, 157, 196))

    def hit(self, time, length, location, timestep, size, hit=True):
        self.animator.hit(time, length, location, timestep, size, hit)

    def drawFrame(self, ships=[]):
        self.doDims([s.position for s in ships] + self.animator.locations())
        self.drawWater()
        for ship in ships:
            self.drawShip(ship)
        for aa in self.animator.getActiveAnimations():
            self.drawObject(*aa)
        pg.display.update()
        pg.display.flip()





