from .Vector import *

class Ray:
    """A class that holds all our rays with which we trace"""
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.unit()

    def traverse(self, dist):
        # Returns a point 'dist' units away from origin in direction
        return self.origin + self.direction * dist

    def __mul__(self, dist):
        # Used in part to move past intersections with surfaces
        # to prevent them from intersecting again
        if isinstance(dist, (int, float)):
            return Ray(self.origin + self.direction * dist, self.direction)
        return NotImplemented

    def __repr__(self):
        return "Origin: %s, Direction: %s" % (self.origin, self.direction)

    def __str__(self):
        return "o: %s, d: %s" % (self.origin, self.direction)
