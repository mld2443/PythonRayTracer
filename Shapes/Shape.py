from abc import ABCMeta, abstractmethod

class Shape:
    """A shape is an object that can be intersected by a ray"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def intersect_ray(self, ray, frustum):
        # Must include a way for the shape to calculate ray intersection
        pass
