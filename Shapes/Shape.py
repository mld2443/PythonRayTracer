from abc import ABCMeta, abstractmethod

class Shape:
    """A shape is an object that can be intersected by a ray"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def intersect_ray(self, ray, frustum):
        # Must include a way for the shape to calculate ray intersection
        pass

class Intersection(object):
    def __init__(self, distance, point, normal, material):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.material = material
