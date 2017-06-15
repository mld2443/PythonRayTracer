from .Shape import Shape
from Utility.Ray import Ray

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
		rRay = ray.d

		# Precalculate these values for our quadratic equation
        ABC = Vector(self.equ[0:2])
        DEF = Vector(self.equ[3:5])
        GHJ = Vector(self.equ[6:8])

		V1 = rRay * rRay
		V2 = Vector([rRay.x * rRay.y, rRay.y * rRay.z, rRay.x * rRay.z]) * 2
		V3 = rCam * rRay
		V4 = Vector([rRay.x * rCam.y + rCam.x * rRay.y, rCam.y * rRay.z + rRay.y * rCam.z, rCam.x * rRay.z + rRay.x * rCam.z])
		V5 = rRay
		V6 = rCam * rCam
		V7 = Vector([rCam.x * rCam.y, rCam.y * rCam.z, rCam.x * rCam.z]) * 2
		V8 = rCam * 2

		# Calculate the quadratic coefficients
		A = ABC * V1 + DEF * V2
		B = ABC * V3 + DEF * V4 + GHI * V5
		C = ABC * V6 + DEF * V7 + GHI * V8 + self.equ[9]

		# Calculate the squared value for our quadratic formula
		square = B**2 - A * C

		# No collision if the root is imaginary
		if square < 0:
			return None

		# Take its squareroot if it's real
		root = sqrt(square)

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

        intersect = (ray * dist).ori
        normal = self.__get_normal(intersect)

        return (dist, intersect, normal, self.mat)
