import math
import numpy as np


def dotproduct(v1, v2):
    return v1.x*v2.x + v1.y*v2.y


def length(v):
    return dotproduct(v, v)**.5


def angle(v1, v2):
    v = np.array([v1.list()])
    inv = np.arctan2([v1.y], [v1.x])
    return inv[0]

    # return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

class Vector:
    def __init__(self, x, y=None):
        if y is None:
            self.x = math.cos(x)
            self.y = math.sin(x)
        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return "(%f, %f)" % (self.x, self.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, other):
        if type(other) != Vector:
            raise TypeError
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)

    def __divmod__(self, other):
        return Vector(self.x/other, self.y/other)

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return self - other

    def __rmul__(self, other):
        return self * other

    def list(self):
        return [self.x, self.y]

    def angle(self):
        facing = angle(self, Vector(1, 0))
        # if abs(self.x - 0) < .000001:
        #     return facing if self.y > 0 else facing + math.pi
        # facing += math.pi * ((1, 1/2), (3/2, 0))[self.x > -0.0000001][self.y > -0.0000001]
        return facing % (2 * math.pi)

    def magnitude(self):
        return (self.x * self.x + self.y * self.y)**.5

    def distance(self, other):
        return (self - other).magnitude()

    def rotate(self, angle):
        return Vector(self.angle() + angle) * self.magnitude()

    def polar(self):
        return PolarVector(self.angle(), self.magnitude())


class PolarVector:
    def __init__(self, angle, size):
        self.theta = angle
        self.r = size

    def cartesian(self):
        return Vector(self.theta) * self.r

# print(Vector(1,0).angle())
# print(Vector(1,1).angle())
# print(Vector(0,1).angle())
# print(Vector(-1,1).angle())
# print(Vector(-1,0).angle())
# print(Vector(-1,-1).angle())
# print(Vector(0,-1).angle())
# print(Vector(1,-1).angle())

# n = 80
# for i in range(n+1):
#     v = Vector(2*math.pi * i / n)
#     if abs(2*math.pi * i / n - v.angle()) > .000001:
#         print('ERROR')
#         print(2*math.pi * i / n, v.angle())
#         print(v)



