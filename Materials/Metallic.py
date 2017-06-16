from .Material import *

class Metallic(Material)
    def __init__(color, fuzz):
        self.color = color
        self.fuzz = fuzz

	def scatter(incoming, intersect, scene, color, bounce):
        reflected = reflect(incoming.dir, intersect.normal)

        bounce = Ray(intersect.point, reflected + fuzz * rand_unit_vector())
        color = self.color

        return (bounce.dir.dot(intersect.normal)) > 0, color, bounce
