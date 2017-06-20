from abc import ABCMeta, abstractmethod
from Utility.Vector import *
import random

class Material(object):
    """Abstract Class to contain all the properties of how light interacts with a material"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def scatter(self, incoming, intersect, scene, color, bounce):
        # Must define how to scatter incoming rays
        pass

def schlick(cosine, index):
    # The Schlick approximation of the Fresnel equation
    r0 = (1 - index) / (1 + index)
    r0 = r0 ** 2
    return r0 + (1 - r0) * ((1 - cosine) ** 5)

class Dielectric(Material):
    def __init__(color, refr_index):
        self.color = color
        self.refr_index = refr_index

    def scatter(self, incoming, intersect, scene, color, bounce):
        reflect_prob = 1.0
        cosine = 1.0
        eta = 1.0
        #outward_normal = Vector([0,0,0])

        reflected = reflect(incoming.direction, intersect.normal)

        entering = dot(incoming.direction, intersect.normal)

        # Are we entering or exiting the object?
        if entering < 0:
            outward_normal = -intersect.normal
            eta = refr_index / scene.refr_index
            cosine = refr_index * entering
        else:
            outward_normal = intersect.normal
            eta = scene.refr_index / refr_index
            cosine = -entering

        refracted = refract(incoming.direction, outward_normal, eta)

        if refracted is None:
            bounce = Ray(intersect.point, reflected)
        else:
            reflect_prob = schlick(cosine, refr_index)

        if random.uniform(0,1) < reflect_prob:
            bounce = Ray(intersect.point, reflected)
        else:
            bounce = Ray(intersect.point, refracted)

        return True, self.color, bounce

class Lambertian(Material):
    def __init__(self, color):
        self.color = color

    def scatter(self, incoming, intersect, scene, color, bounce):
        target = intersect.point + intersect.normal + rand_unit_vector()

        bounce = Ray(intersect.point, target - intersect.point)

        return True, self.color, bounce

class Metallic(Material):
    def __init__(color, fuzz):
        self.color = color
        self.fuzz = fuzz

    def scatter(self, incoming, intersect, scene, color, bounce):
        reflected = reflect(incoming.direction, intersect.normal)

        bounce = Ray(intersect.point, reflected + fuzz * rand_unit_vector())
        color = self.color

        return dot(bounce.direction, intersect.normal) > 0, self.color, bounce
