from .Material import *

class Metallic(Material):
    def __init__(color, fuzz):
        self.color = color
        self.fuzz = fuzz

    def scatter(self, incoming, intersect, scene, color, bounce):
        reflected = reflect(incoming.direction, intersect.normal)

        bounce = Ray(intersect.point, reflected + fuzz * rand_unit_vector())
        color = self.color

        return dot(bounce.direction, intersect.normal) > 0, self.color, bounce
