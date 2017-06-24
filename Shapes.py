#############
# Shapes.py #
#############
# Here I define the mathematical defenitions of a Shape
# For an exercise, you might try defining your
# own shape, like a triangle.
# For those looking to tinker, try messing with
# shape normals for different effects.

from abc import ABCMeta, abstractmethod
from collections import namedtuple
from Utility.Vector import *

class Shape(object):
    """A shape is an object that can be intersected by a ray"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def intersect_ray(self, ray, frustum):
        # Must include a way for the shape to calculate ray intersection
        pass

Frustum = namedtuple('Frustum', 'near far')
Intersection = namedtuple('Intersection', 'distance point normal material')

class Plane(Shape):
    """Simple flat infinite plane defined by the plane equation"""

    def __init__(self, material, position, normal):
        self.material = material
        self.position = Vector._make(position)
        self.normal = Vector._make(normal).unit()
        # Constant value so we don't calculate it every time
        self.n_dot_p = dot(self.normal, self.position)

    def intersect_ray(self, ray, frustum):
        denominator = dot(self.normal, ray.direction)

        if denominator is 0.0:
            return None

        distance = (self.n_dot_p - dot(self.normal, ray.origin)) / denominator

        if frustum.near <= distance <= frustum.far:
            return Intersection(distance, ray.traverse(distance), self.normal, self.material)
        return None

Equation = namedtuple('Equation', 'A B C D E F G H I J')

class Quadric(Shape):
    """A Quadric is a shape described by a 2nd degree polynomial of the form:
        Ax² + By² + Cz² + 2Dyz + 2Exz + 2Fxy + 2Gx + 2Hy + 2Iz + J = 0"""

    def __init__(self, material, position, equation):
        self.material = material
        self.position = Vector._make(position)
        self.equation = Equation._make(equation)
        # Prepare ABC, DEF, and GHI vectors per the equation
        self.ABC = Vector._make(self.equation[0:3])
        self.DEF = Vector._make(self.equation[3:6])
        self.GHI = Vector._make(self.equation[6:9])

    def _get_normal(self, point):
        relative = point - self.position
        # Compute the generic derivative of the equation at given point
        x = 2 * self.equation.A * relative.x + self.equation.E * relative.z + self.equation.F * relative.y + self.equation.G
        y = 2 * self.equation.B * relative.y + self.equation.D * relative.z + self.equation.F * relative.x + self.equation.H
        z = 2 * self.equation.C * relative.z + self.equation.D * relative.y + self.equation.E * relative.x + self.equation.I
        return Vector(x,y,z).unit()

    def __calculate_intersection(self, ray, frustum):
        # Calculate the positions of the camera and the ray relative to the quadric
        rCam = ray.origin - self.position
        rRay = ray.direction

        # Precalculate these values for our quadratic equation
        V1 = rRay * rRay
        V2 = Vector(rRay.x * rRay.y, rRay.y * rRay.z, rRay.z * rRay.x) * 2
        V3 = rCam * rRay
        V4 = Vector(rRay.x * rCam.y + rCam.x * rRay.y, rCam.y * rRay.z + rRay.y * rCam.z, rCam.x * rRay.z + rRay.x * rCam.z)
        V5 = rRay
        V6 = rCam * rCam
        V7 = Vector(rCam.x * rCam.y, rCam.y * rCam.z, rCam.z * rCam.x) * 2
        V8 = rCam * 2

        # Calculate the quadratic coefficients
        A = dot(self.ABC, V1) + dot(self.DEF, V2)
        B = dot(self.ABC, V3) + dot(self.DEF, V4) + dot(self.GHI, V5)
        C = dot(self.ABC, V6) + dot(self.DEF, V7) + dot(self.GHI, V8) + self.equation[9]

        # Calculate the squared value for our quadratic formula
        square = B ** 2 - A * C

        # No collision if the root is imaginary
        if square < 0:
            return None

        # Take its squareroot if it's real
        root = square ** 0.5

        # Calculate both intersections
        D1 = (-B - root) / A
        D2 = (-B + root) / A

        # Return closest intersection thats in the frustum
        if frustum.near <= D1 <= frustum.far:
            return D1
        elif frustum.near <= D2 <= frustum.far:
            return D2
        return None

    def intersect_ray(self, ray, frustum):
        distance = self.__calculate_intersection(ray, frustum)

        if distance is None:
            return None

        intersect = ray.traverse(distance)
        normal = self._get_normal(intersect)

        return Intersection(distance, intersect, normal, self.material)

class Sphere(Quadric):
    """Redefinition of spheres to override the normal function for a simpler one"""

    def __init__(self, material, position, radius):
        super().__init__(material, position, (1,1,1,0,0,0,0,0,0,-(radius**2)))

    def _get_normal(self, point):
        # Override Quadric's normal function with this faster calculation
        return (point - self.position).unit()
