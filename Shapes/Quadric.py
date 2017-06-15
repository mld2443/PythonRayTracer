from .Shape import *
from Utility.Ray import *

class Quadric(Shape):
    """
    A Quadric is a shape described by a 2nd degree polynomial of the form:
        Ax² + By² + Cz² + 2Dyz + 2Exz + 2Fxy + 2Gx + 2Hy + 2Iz + J = 0
    """

    def __init__(self, material, position, equation):
        self.mat = material
        self.pos = position
        self.equ = equation

    def _get_normal(self, point):
        relative = point - self.pos
        # Compute the generic derivative of the equation at given point
        x = 2 * self.equ[0] * relative[0] + self.equ[4] * relative[2] + self.equ[5] * relative[1] + self.equ[6]
        y = 2 * self.equ[1] * relative[1] + self.equ[3] * relative[2] + self.equ[5] * relative[0] + self.equ[7]
        z = 2 * self.equ[2] * relative[2] + self.equ[3] * relative[1] + self.equ[4] * relative[0] + self.equ[8]
        return Vector([x,y,z]).unit()

    def __calculate_intersection(self, ray, frustum):
        # Calculate the positions of the camera and the ray relative to the quadric
        rCam = ray.ori - self.pos
        rRay = ray.dir

        # Precalculate these values for our quadratic equation
        ABC = Vector(self.equ[0:2])
        DEF = Vector(self.equ[3:5])
        GHJ = Vector(self.equ[6:8])

        V1 = rRay * rRay
        V2 = Vector([rRay[0] * rRay[1], rRay[1] * rRay[2], rRay[2] * rRay[0]]) * 2
        V3 = rCam * rRay
        V4 = Vector([rRay[0] * rCam[1] + rCam[0] * rRay[1], rCam[1] * rRay[2] + rRay[1] * rCam[2], rCam[0] * rRay[2] + rRay[0] * rCam[2]])
        V5 = rRay
        V6 = rCam * rCam
        V7 = Vector([rCam[0] * rCam[1], rCam[1] * rCam[2], rCam[0] * rCam[2]]) * 2
        V8 = rCam * 2

        # Calculate the quadratic coefficients
        A = ABC.dot(V1) + DEF.dot(V2)
        B = ABC.dot(V3) + DEF.dot(V4) + GHI.dot(V5)
        C = ABC.dot(V6) + DEF.dot(V7) + GHI.dot(V8) + self.equ[9]

        # Calculate the squared value for our quadratic formula
        square = B**2 - A * C

        # No collision if the root is imaginary
        if square < 0:
            return None

        # Take its squareroot if it's real
        root = square**0.5

        # Calculate both intersections
        D1 = (-B - root)/A
        D2 = (-B + root)/A

        # Return closest intersection thats in the frustum
        if frustum[0] <= D1 <= frustum[1]:
            return D1
        elif frustum[0] <= D2 <= frustum[1]:
            return D2
        return None

    def intersect_ray(self, ray, frustum):
        dist = self.__calculate_intersection(ray, frustum)

        if dist is None:
            return None

        intersect = ray.traverse(dist)
        normal = self._get_normal(intersect)

        return (dist, intersect, normal, self.mat)
