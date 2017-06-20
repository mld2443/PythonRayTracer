from .Material import *
import random

class Dielectric(Material)
    def __init__(color, refr_index):
        self.color = color
        self.refr_index = refr_index

    def scatter(incoming, intersect, scene, color, bounce):
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
