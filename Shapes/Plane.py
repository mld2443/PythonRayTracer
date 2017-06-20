from .Shape import *

class Plane(Shape):
    def __init__(self, material, position, normal):
        self.mat = material
        self.pos = position
        self.nor = normal.unit()
        # Constant value so we don't calculate it every time
        self.n_p = dot(self.nor, self.pos)

    def intersect_ray(self, ray, frustum):
        denominator = dot(self.nor, ray.dir)

        if denominator == 0.0
            return None

        dist = (self.n_p - dot(self.nor, ray.ori)) / denominator

        if dist < frustum[0] and dist > frustum[1]:
            return None

        intersect = ray.traverse(dist)

        return Intersection(dist, intersect, self.nor, self.mat)
