import pygame as pg

class ShipSprite:
    def __init__(self, ship):
        self.ship = ship
        self.surf = None
        self.width = -1
        self.height = -1

    def update(self):
        width = int(self.ship.hull.length)
        height = int(self.ship.hull.beam)
        self.width = width
        self.height = height
        surf = pg.Surface((width, height))
        surf.fill((255, 255, 255))
        surf.set_colorkey((255, 255, 255))
        pg.draw.ellipse(surf, (200, 200, 200), (0, 0, width, height))
        pg.draw.circle(surf, (255, 0, 0), (int(3 * width / 4), int(height/2)), int(height/4))
        self.surf = surf

    def getSurface(self):
        if not self.surf:
            self.update()
        return self.surf