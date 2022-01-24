import pygame as pg


class Animation:
    def __init__(self, length, timestep, size):
        self.frames = [None for frame in range(max(1, int(length // timestep)))]
        self.length = length
        self.timestep = timestep  # number of frames is length // timestep
        self.size = size

    def __repr__(self):
        return "%s: %i frames, size: %s"%(str(type(self)), len(self.frames), str(self.size))

    def getBlank(self, width, height):
        surf = pg.Surface((width, height))
        surf.fill((0, 0, 0))
        surf.set_colorkey((0, 0, 0))
        return surf

    def drawFrame(self, frame):
        raise NotImplementedError

    def getFrame(self, frame):
        if frame >= len(self.frames):
            return False
        if self.frames[frame]:
            return self.frames[frame]
        drawing = self.drawFrame(frame)
        self.frames[frame] = drawing
        return drawing

    def animate(self):
        for frame in range(self.length // self.timestep):
            self.getFrame(frame)


class HitAnimation(Animation):
    def __init__(self, length, timestep, size, hit):
        super().__init__(length, timestep, size)
        self.hit = hit

    def drawFrame(self, frame):
        portion = frame/len(self.frames)
        # radius = int(self.size.x * frame/len(self.frames))
        # radius = int((-0.0625 * portion**4 + 0.65 * portion**3 - 2.035 * portion**2 + 1.794 * portion + 0.5239) * self.size.x)
        radius = int((.8 - portion**2 + .6 * portion) * self.size.x / 2)
        # radius = int((.8 - 2 * portion**2 + 1.2 * portion) * self.size.x / 2)
        color = (255, 127, 0) if self.hit else (230, 230, 230)
        surf = self.getBlank(self.size.x, self.size.y)
        pg.draw.circle(surf, color, (int(self.size.x / 2), int(self.size.y / 2)), radius)
        return surf




