from Materials import *
from Camera import *

# define constants
up = Vector(0,0,1)

def default_scene():
    # Invent matter
    matte_white = Lambertian(white)
    #mirror = Metallic(Color(0.64, 1.0, 1.0), 0.03)
    #glass = Dielectric(Color(0.73, 1.0, 0.82), 1.2)
    #shiny_red = Metallic(red, 0.0)
    matte_green = Lambertian(green)

    # Make a scene
    floor = Shapes.Plane(matte_white, Vector(0,0,0), up)
    sphere1 = Shapes.Sphere(matte_green, Vector(0,25,3), 3)
    sphere2 = Shapes.Sphere(matte_white, Vector(-4,35,4), 4)
    #sphere3 = Sphere(matte_white, Vector([-10,2,6]), 6)
    sphere4 = Shapes.Sphere(matte_white, Vector(19,34,18), 18)

    return [floor, sphere1, sphere2, sphere4]

def random_scene(seed, num_spheres):

    return []

def build_and_draw(options):
    # Build a camera obscura
    camera = Camera(Vector(0,0,8), Vector(0,1,0), up, options.resolution[0],options.resolution[1], 95.0)

    return capture(camera, options.samples, options.depth)
