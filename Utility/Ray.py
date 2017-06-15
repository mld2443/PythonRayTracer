from .Vector import *

class Ray:
    def __init__(self, origin, direction):
        self.ori = origin
        self.dir = direction.unit()
        self.inv = [1 / d for d in self.dir.xyz]

    def __repr__(self):
        return "Origin: %s, Direction: %s" % (self.ori, self.dir)

    def __str__(self):
        return "o: %s, d: %s" % (self.ori, self.dir)

    def traverse(self, dist):
        return self.ori + self.dir * dist

    def reflect(self, across, tolerance=0.000001):
        return Ray(across.origin, reflect()) * tolerance

    #def refract(self, across, eta, tolerance=0.000001):
        #refract = Vector.refract()

        #if refract is Vector.zero():
        #    return None

        #return Ray(across.origin, refract.unit) *

    def __mul__(self, dist):
        if isinstance(dist, (int, float)):
            return Ray(self.ori + self.dir * dist, self.dir)
        else:
            return NotImplemented
