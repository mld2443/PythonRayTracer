from collections import namedtuple
from operator import mul
from random import gauss

class Vector(namedtuple('Point', 'x y z')):
    """A math vector capable of indication direction and magnitude"""

    def unit(self):
        # Normalization
        return self/abs(self)

    # These could be more pythonic, but I'm worried about speed and simplicity more
    def __add__(self, rhs):
        if isinstance(rhs, Vector):
            return Vector(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)
        return NotImplemented

    def __sub__(self, rhs):
        if isinstance(rhs, Vector):
            return Vector(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)
        return NotImplemented

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __abs__(self):
        return sum(x**2 for x in self) ** 0.5

    def __truediv__(self, rhs):
        if isinstance(rhs, (int, float)):
            return Vector(self.x/rhs, self.y/rhs, self.z/rhs)
        return NotImplemented

    def __mul__(self, rhs):
        if isinstance(rhs, Vector):
            # Elementwise product
            return Vector(self.x * rhs.x, self.y * rhs.y, self.z * rhs.z)
        elif isinstance(rhs, (int, float)):
            # Scaling
            return Vector(self.x*rhs, self.y*rhs, self.z*rhs)
        return NotImplemented

    def __str__(self):
        return "<{:2f}, {:2f}, {:2f}>".format(self.x, self.y, self.z)

def rand_unit_vector():
    return Vector._make([gauss(0, 1) for i in range(3)]).unit()

def dot(lhs, rhs):
    # Dot-product
    if isinstance(lhs, Vector) and isinstance(rhs, Vector):
        return sum(map(mul, lhs, rhs))
    return NotImplemented

def cross(lhs, rhs):
    # Cross-product
    if isinstance(lhs, Vector) and isinstance(rhs, Vector):
        return Vector(lhs.y * rhs.z - lhs.z * rhs.y, lhs.z * rhs.x - lhs.x * rhs.z, lhs.x * rhs.y - lhs.y * rhs.x)
    return NotImplemented

def reflect(direction, normal):
    # Reflect a vector across a surface, assumes dir and normal are unit vectors
    return (direction - normal * (2 * dot(direction, normal))).unit()

def refract(direction, normal, eta):
    # Refract a vector on surface with normal and eta of refraction index ratio
    direction = direction.unit()
    dt = dot(direction, normal)
    discriminant = 1.0 - eta ** 2 * (1.0 - dt ** 2)
    return (direction - normal * dt) * eta - normal * discriminant**0.5 if discriminant > 0 else None


#MARK: rays

class Ray(object):
    """A class that holds all our rays with which we trace"""
    def __init__(self, origin, direction):
        self.origin = Vector._make(origin)
        self.direction = Vector._make(direction).unit()

    def traverse(self, distance):
        # Returns a point 'distance' units away from origin in direction
        return self.origin + self.direction * distance
