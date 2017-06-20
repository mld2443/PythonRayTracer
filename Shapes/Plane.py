from .Shape import *

class Plane(Shape):
    def __init__(self, material, position, normal):
        self.material = material
        self.position = position
        self.normal = normal.unit()
        # Constant value so we don't calculate it every time
        self.n_dot_p = dot(self.nor, self.pos)

    def intersect_ray(self, ray, frustum):
        denominator = dot(self.normal, ray.direction)

        if denominator is 0.0:
            return None

        distance = (self.n_dot_p - dot(self.normal, ray.origin)) / denominator

        if distance < frustum[0] and distance > frustum[1]:
            return None

        return Intersection(distance, ray.traverse(distance), self.normal, self.material)
