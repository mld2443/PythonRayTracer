#############
# Shapes.py #
#############
# Here I define the mathematical defenitions of a Shape
# For an exercise, you might try defining your
# own shape, like a triangle.
# For those looking to tinker, try messing with
# shape normals for different effects.

from abc import ABCMeta, abstractmethod
from Utility.Vector import *

class Shape(object):
    """A shape is an object that can be intersected by a ray"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def intersect_ray(self, ray, frustum):
        # Must include a way for the shape to calculate ray intersection
        pass

Intersection = namedtuple('Intersection', 'distance point normal material')

class Plane(Shape):
    """Simple flat infinite plane defined by the plane equation"""

    def __init__(self, material, position, normal):
        self._material = material
        self._position = Vector._make(position)
        self._normal = Vector._make(normal).unit()
        # Constant value so we don't calculate it every time
        self._n_dot_p = dot(self._normal, self._position)

    def intersect_ray(self, ray, frustum):
        denominator = dot(self._normal, ray.direction)

        if denominator is 0.0:
            return None

        distance = (self._n_dot_p - dot(self._normal, ray.origin)) / denominator

        if frustum.near <= distance <= frustum.far:
            return Intersection(distance,
                                ray.project(distance),
                                self._normal,
                                self._material)
        return None

Equation = namedtuple('Equation', 'A B C D E F G H I J')

class Quadric(Shape):
    """A Quadric is a shape described by a 2nd degree polynomial of the form:
        Ax² + By² + Cz² + 2Dyz + 2Exz + 2Fxy + 2Gx + 2Hy + 2Iz + J = 0"""

    def __init__(self, material, position, equation):
        self._material = material
        self._position = Vector._make(position)
        self._equation = Equation._make(equation)
        # Prepare ABC, DEF, and GHI vectors per the equation
        self._ABC = Vector._make(self._equation[0:3])
        self._DEF = Vector._make(self._equation[3:6])
        self._GHI = Vector._make(self._equation[6:9])

    def _get_normal(self, point):
        relative = point - self._position
        # Compute the generic derivative of the equation at given point
        x = (2 * self._equation.A * relative.x
             + self._equation.E * relative.z
             + self._equation.F * relative.y
             + self._equation.G)
        y = (2 * self._equation.B * relative.y
             + self._equation.D * relative.z
             + self._equation.F * relative.x
             + self._equation.H)
        z = (2 * self._equation.C * relative.z
             + self._equation.D * relative.y
             + self._equation.E * relative.x
             + self._equation.I)
        return Vector(x,y,z).unit()

    def _calculate_intersection(self, ray, frustum):
        # Calculate the positions of the camera and the ray relative to the quadric
        rCam = ray.origin - self._position
        rRay = ray.direction

        # Precalculate these values for our quadratic equation
        V1 = rRay * rRay
        V2 = Vector(rRay.x * rRay.y, rRay.y * rRay.z, rRay.z * rRay.x) * 2
        V3 = rCam * rRay
        V4 = Vector(rRay.x * rCam.y + rCam.x * rRay.y,
                    rCam.y * rRay.z + rRay.y * rCam.z,
                    rCam.x * rRay.z + rRay.x * rCam.z)
        V5 = rRay
        V6 = rCam * rCam
        V7 = Vector(rCam.x * rCam.y, rCam.y * rCam.z, rCam.z * rCam.x) * 2
        V8 = rCam * 2

        # Calculate the quadratic coefficients
        A = dot(self._ABC, V1) + dot(self._DEF, V2)
        B = dot(self._ABC, V3) + dot(self._DEF, V4) + dot(self._GHI, V5)
        C = dot(self._ABC, V6) + dot(self._DEF, V7) + dot(self._GHI, V8) + self._equation[9]

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
        distance = self._calculate_intersection(ray, frustum)

        if distance is None:
            return None

        intersect = ray.project(distance)
        normal = self._get_normal(intersect)

        return Intersection(distance, intersect, normal, self._material)

class Sphere(Quadric):
    """Redefinition of spheres to override the normal function for a simpler one"""

    def __init__(self, material, position, radius):
        super().__init__(material, position, (1,1,1,0,0,0,0,0,0,-(radius**2)))

    def _get_normal(self, point):
        # Override Quadric's normal function with this faster calculation
        return (point - self._position).unit()
