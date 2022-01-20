import math

def dotproduct(v1, v2):
  return v1.x*v2.x + v1.y*v2.y

def length(v):
  return dotproduct(v, v)**.5

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

class Vector:
    def __init__(self, x, y=None):
        if y is None:
            self.x = math.cos(x)
            self.y = -math.sin(x)
        else:
            self.x = x
            self.y = y

    def __repr__(self):
        return "(%f, %f)"%(self.x, self.y)

    def __sub__(self, other):
        if type(other) != Vector:
            raise TypeError
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        if type(other) != Vector:
            raise TypeError
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x*other, self.y*other)

    def __divmod__(self, other):
        return Vector(self.x/other, self.y/other)

    def angle(self):
        facing = angle(self, Vector(1, 0))
        if self.x == 0:
            return facing if self.y > 0 else facing + math.pi
        if self.y < 0 < self.x:
            facing += 3*math.pi / 2
        elif self.x < 0 and self.y < 0:
            facing += math.pi / 2
        return facing % (2 * math.pi)


# print(Vector(1,0).angle())
# print(Vector(1,1).angle())
# print(Vector(0,1).angle())
# print(Vector(-1,1).angle())
# print(Vector(-1,0).angle())
# print(Vector(-1,-1).angle())
# print(Vector(0,-1).angle())
# print(Vector(1,-1).angle())


