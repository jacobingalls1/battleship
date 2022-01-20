import pygame as pg
from display.shipSprite import ShipSprite
import math

SCREEN_SIZE = (1000,1000)
SCREEN_BORDERS = ((-500, -500), (500, 500))
margin = 100
pg.init()

class Display:
    def __init__(self, name):
        self.screen = pg.display.set_mode(SCREEN_SIZE)

    def getShipSprite(self, ship):
        return ShipSprite(ship)

    def drawShip(self, rect, ship):
        if rect[2] - rect[0] > rect[3] - rect[1]:
            rect[3] = rect[1] + rect[2] - rect[0]
        else:
            rect[2] = rect[0] + rect[3] - rect[1]
        xPos = (ship.position.x - rect[0]) / (rect[2] - rect[0])
        yPos = (ship.position.y - rect[1]) / (rect[3] - rect[1])
        xPos *= SCREEN_SIZE[0]
        yPos *= SCREEN_SIZE[1]
        #the ship sprite is as long as the ship in feet
        scale = SCREEN_SIZE[0] / (rect[2] - rect[0])
        surf = pg.transform.rotate(pg.transform.scale(ship.sprite.surf, (int(scale * ship.sprite.width), int(scale * ship.sprite.height))),
            180 * ship.facing / math.pi)
        xPos -= surf.get_size()[0] / 2
        yPos -= surf.get_size()[1] / 2
        self.screen.blit(surf, (xPos, yPos))

    def drawFrame(self, ships=[]):
        xn, xx = min([s.position.x for s in ships]), max([s.position.x for s in ships])
        yn, yx = min([s.position.y for s in ships]), max([s.position.y for s in ships])
        rect = [min(SCREEN_BORDERS[0][0], xn - margin), min(SCREEN_BORDERS[0][1], yn - margin),
                max(SCREEN_BORDERS[1][0], xx + margin), max(SCREEN_BORDERS[1][1], yx + margin)]
        self.screen.fill((0, 157, 196))
        for ship in ships:
            self.drawShip(rect, ship)
        pg.display.update()
        pg.display.flip()





