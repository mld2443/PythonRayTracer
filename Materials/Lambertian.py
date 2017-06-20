from .Material import *

class Lambertian(Material):
    def __init__(self, color):
        self.color = color

    def scatter(self, incoming, intersect, scene, color, bounce):
        target = intersect.point + intersect.normal + rand_unit_vector()

        bounce = Ray(intersect.point, target - intersect.point)

        return True, self.color, bounce
