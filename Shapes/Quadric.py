from .Shape import *
from Utility.Ray import *

class Quadric(Shape):
    """
    A Quadric is a shape described by a 2nd degree polynomial of the form:
        Ax² + By² + Cz² + 2Dyz + 2Exz + 2Fxy + 2Gx + 2Hy + 2Iz + J = 0
    """

    def __init__(self, material, position, equation):
        self.material = material
        self.position = position
        self.equation = equation
        # Prepare ABC, DEF, and GHI vectors per the equation
        self.ABC = Vector(self.equation[0:2])
        self.DEF = Vector(self.equation[3:5])
        self.GHI = Vector(self.equation[6:8])

    def _get_normal(self, point):
        relative = point - self.position
        # Compute the generic derivative of the equation at given point
        x = 2 * self.equation[0] * relative[0] + self.equation[4] * relative[2] + self.equation[5] * relative[1] + self.equation[6]
        y = 2 * self.equation[1] * relative[1] + self.equation[3] * relative[2] + self.equation[5] * relative[0] + self.equation[7]
        z = 2 * self.equation[2] * relative[2] + self.equation[3] * relative[1] + self.equation[4] * relative[0] + self.equation[8]
        return Vector([x,y,z]).unit()

    def __calculate_intersection(self, ray, frustum):
        # Calculate the positions of the camera and the ray relative to the quadric
        rCam = ray.origin - self.position
        rRay = ray.dirgin

        # Precalculate these values for our quadratic equation
        V1 = rRay * rRay
        V2 = Vector([rRay[0] * rRay[1], rRay[1] * rRay[2], rRay[2] * rRay[0]]) * 2
        V3 = rCam * rRay
        V4 = Vector([rRay[0] * rCam[1] + rCam[0] * rRay[1], rCam[1] * rRay[2] + rRay[1] * rCam[2], rCam[0] * rRay[2] + rRay[0] * rCam[2]])
        V5 = rRay
        V6 = rCam * rCam
        V7 = Vector([rCam[0] * rCam[1], rCam[1] * rCam[2], rCam[0] * rCam[2]]) * 2
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
        if frustum[0] <= D1 <= frustum[1]:
            return D1
        elif frustum[0] <= D2 <= frustum[1]:
            return D2
        return None

    def intersect_ray(self, ray, frustum):
        distance = self.__calculate_intersection(ray, frustum)

        if distance is None:
            return None

        intersect = ray.traverse(distance)
        normal = self._get_normal(intersect)

        return Intersection(distance, intersect, normal, self.material)
