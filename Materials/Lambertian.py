from .Material import *

class Lambertian(Material):
    def __init__(color, shininess):
        self.color = color
        self.shininess = shininess

    def scatter(incoming, intersect, scene, color, bounce) -> Bool {
        target = intersect.point + intersect.normal + rand_unit_vector()

        bounce = Ray(intersect.point, target - intersect.point)
        #FIXME
        #color = scene.phongShading(self.color, position: intersect.point, normal: intersect.norm, from: incoming.d, diffuse: true, specular: self.shininess)

        return True, color, bounce
