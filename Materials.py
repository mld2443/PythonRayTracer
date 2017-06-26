from abc import ABCMeta, abstractmethod
from Utility.Vector import *
import random

class Material(object):
    """Abstract Class to contain all the properties of how light interacts with a material"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def scatter(self, incoming, intersect, refr_index):
        # Must define how to scatter incoming rays
        pass

def schlick(cosine, eta):
    # The Schlick approximation of the Fresnel equation
    r0 = (1 - eta) / (1 + eta)
    r0 = r0 ** 2
    return r0 + (1 - r0) * ((1 - cosine) ** 5)

class Dielectric(Material):
    """Glossy, transparent material"""

    def __init__(self, color, refr_index):
        self.color = color
        self.refr_index = refr_index

    def scatter(self, incoming, intersect, refr_index):
        entering = dot(incoming.direction, intersect.normal)

        # Are we entering or exiting the object?
        if entering < 0:
            outward_normal = -intersect.normal
            eta = self.refr_index / refr_index
            cosine = self.refr_index * entering
        else:
            outward_normal = intersect.normal
            eta = refr_index / self.refr_index
            cosine = -entering

        reflected = reflect(incoming.direction, intersect.normal)
        refracted = refract(incoming.direction, outward_normal, eta)

        if refracted is None:
            return self.color, Ray(intersect.point, reflected)

        if random.uniform(0,1) < schlick(cosine, self.refr_index):
            return self.color, Ray(intersect.point, reflected)
        return self.color, Ray(intersect.point, refracted)

class Lambertian(Material):
    """Matte, diffuse material"""
    def __init__(self, color):
        self.color = color

    def scatter(self, incoming, intersect, refr_index):
        target = intersect.point + intersect.normal + rand_unit_vector()

        return self.color, Ray(intersect.point, target - intersect.point)

class Metallic(Material):
    """Shiny, specular material"""
    def __init__(self, color, fuzz):
        self.color = color
        self.fuzz = fuzz

    def scatter(self, incoming, intersect, refr_index):
        reflected = reflect(incoming.direction, intersect.normal)

        bounce = Ray(intersect.point, reflected + fuzz * rand_unit_vector())

        return self.color, bounce if dot(bounce.direction, intersect.normal) > 0 else None
