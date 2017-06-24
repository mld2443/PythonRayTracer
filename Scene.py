from Materials import *
from Camera import *

# define constants
up = Vector(0,0,1)

# Invent matter
matte_white = Lambertian(white)
#mirror = Metallic(Color(0.64, 1.0, 1.0), 0.03)
#glass = Dielectric(Color(0.73, 1.0, 0.82), 1.2)
#shiny_red = Metallic(red, 0.0)
matte_green = Lambertian(green)

# Make a scene
floor = Shapes.Plane(matte_white, Vector(0,0,0), up)
sphere1 = Shapes.Sphere(matte_green, Vector(0,10,3), 3)
sphere2 = Shapes.Sphere(matte_white, Vector(-4,20,4), 4)
#sphere3 = Sphere(matte_white, Vector([-10,2,6]), 6)
sphere4 = Shapes.Sphere(matte_white, Vector(19,19,18), 18)

scene = [floor, sphere1, sphere2, sphere4]

# Build a camera obscura
camera = Camera(Vector(0,-15,8), Vector(0,-14,8), up, 320, 240, 95.0)
