from .Quadric import Qaudric

class Sphere(Quadric):
    def __init__(self, material, position, radius):
        super().__init__(material, position, [1,1,1,0,0,0,0,0,0,-(radius**2)])

    def _get_normal(self, point):
        # Override Quadric's normal function
        return (point - self.pos).unit()
