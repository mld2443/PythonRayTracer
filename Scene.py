from Utility.Vector import Vector
import Materials
import Shapes
from Camera import *

# define constants
up = Vector(0,0,1)

def prepared_scene(params):
    # Invent matter
    matte_white = Materials.Lambertian(Color.white)
    matte_green = Materials.Lambertian(Color.green)
    glass = Materials.Dielectric(Color.Color(0.73, 1.0, 0.82), 1.33)
    mirror = Materials.Metallic(Color.Color(0.64, 1.0, 1.0), 0.0)
    gunmetal = Materials.Metallic(Color.darkgrey, 0.03)

    # Make a scene
    scene = []
    scene.append(Shapes.Plane(matte_white, Vector(0,0,0), up))
    scene.append(Shapes.Sphere(matte_green, Vector(-3,250,3), 3))
    scene.append(Shapes.Sphere(glass, Vector(4,260,5), 5))
    scene.append(Shapes.Sphere(mirror, Vector(-5,270,7), 7))
    scene.append(Shapes.Sphere(gunmetal, Vector(13,285,20), 20))

    # Build a camera obscura
    camera = Camera(Vector(0,0,3),
                    Vector(0,1,0),
                    up,
                    params.resolution,
                    5.0,
                    params.samples,
                    params.depth,
                    params.frustum)

    return scene, camera

def random_scene(params):
    camera = Camera(Vector(0,0,8),
                    Vector(0,1,0),
                    up,
                    params.resolution,
                    params.fov,
                    params.samples,
                    params.depth,
                    params.frustum)

    return [], camera

def build_and_draw(params):
    if params.verbose:
        begin = time()

    scene, camera = prepared_scene(params) if params.prepared else random_scene(params)

    if params.debug:
        print(params)
        print(camera)
        print(scene)

    if params.verbose:
        print("Scene built, Number of shapes: {}".format(len(scene)))
        print("Time to build scene: {:.2f}s".format(time() - begin))

    return capture(scene, camera, params.verbose, params.heatmap)
