from .Material import *
import random

class Dielectric(Material)
    def __init__(color, refrIndex):
        self.color = color
        self.refrIndex = refrIndex

    def scatter(incoming, intersect, scene, color, bounce):
        reflect_prob = 1.0
        cosine = 1.0
        eta = 1.0
        #outward_normal = Vector([0,0,0])

        reflected = reflect(incoming.dir, intersect.normal)

        # Are we entering the object?
        entering = dot(incoming.dir, intersect.normal)

        if entering < 0:
            outward_normal = -intersect.normal
            eta = refrIndex / scene.refrIndex
            cosine = refrIndex * entering
        else:
            outward_normal = intersect.norm
            eta = scene.refrIndex / refrIndex
            cosine = -entering

        refracted = refract(incoming.dir, outward_normal, eta)

        if refracted is not Vector([0,0,0]):
            reflect_prob = schlick(cosine, refrIndex)
        else:
            bounce = Ray(intersect.point, reflected)

        if random.uniform(0,1) < reflect_prob:
            bounce = Ray(intersect.point, reflected)
        else:
			bounce = Ray(intersect.point, refracted)

		return True, self.color, bounce
