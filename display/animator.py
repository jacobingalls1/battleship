from collections import defaultdict
from display.animations import HitAnimation


class ActiveAnimation:
    def __init__(self, animation, location, time, timestep=-1):
        self.animation = animation
        self.position = location
        self.time = time
        self.frame = -1
        self.rotation = 0

    def __repr__(self):
        return "ActiveAnimation with " + str(self.animation)

    def nextFrame(self):
        self.frame += 1
        return self.animation.getFrame(self.frame)

    def drawable(self):
        return (self.nextFrame(), self.position, self.animation.size, self.rotation)

    def finished(self):
        return not bool(self.animation.getFrame(self.frame + 1))

class Animator:
    def __init__(self):
        self.animations = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:None)))
        self.activeAnimations = []

    def hit(self, time, length, location, timestep, size, hit):
        if acc := self.animations[timestep][HitAnimation][length]:
            self.activeAnimations.append(ActiveAnimation(acc, location, time, timestep))
            return
        self.animations[timestep][HitAnimation][length] = HitAnimation(length, timestep, size, hit)
        self.activeAnimations.append(ActiveAnimation(self.animations[timestep][HitAnimation][length], location, time, timestep))

    def locations(self):
        return [a.position for a in self.activeAnimations]

    def getActiveAnimations(self):
        ret = []
        for aa in self.activeAnimations:
            if aa.finished():
                self.activeAnimations.remove(aa)
            else:
                draw = aa.drawable
                ret.append(aa.drawable())
        print(ret)
        print(self.activeAnimations)
        return ret



