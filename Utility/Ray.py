from .Vector import *

class Ray:
    """A class that holds all our rays with which we trace"""
    def __init__(self, origin, direction):
        self.ori = origin
        self.dir = direction.unit()
        self.inv = [1 / d for d in self.dir.xyz]

    def traverse(self, dist):
        # Returns a point 'dist' units away from origin in direction
        return self.ori + self.dir * dist

    def reflect(self, across, tolerance=0.000001):
        return Ray(across.origin, reflect()) * tolerance

    #def refract(self, across, eta, tolerance=0.000001):
        #refract = Vector.refract()

        #if refract is Vector.zero():
        #    return None

        #return Ray(across.origin, refract.unit) *

    def __mul__(self, dist):
        # Used in part to move past intersections with surfaces
        # to prevent them from intersecting again
        if isinstance(dist, (int, float)):
            return Ray(self.ori + self.dir * dist, self.dir)
        else:
            return NotImplemented

    def __repr__(self):
        return "Origin: %s, Direction: %s" % (self.ori, self.dir)

    def __str__(self):
        return "o: %s, d: %s" % (self.ori, self.dir)
