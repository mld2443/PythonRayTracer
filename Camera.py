#############
# Camera.py #
#############
# This is the proverbial sausage factory.
# There are lots of things to play with in here
# and I've tried to mark areas of interest

from collections import namedtuple
from math import radians, tan, sqrt
from random import uniform
from time import time
from Utility.Vector import cross, Ray
import Utility.Color as Color

# Global settings
scene_refraction_index = 1.0
total_rays = 0

# A frustum is a conical shape with the top chopped off
Frustum = namedtuple('Frustum', 'near far')

class Camera(object):
    """Holds the camera's parameters and calculates the screenspace coordinate frame"""

    def __init__(self, position, direction, up, resolution, FOV, samples, depth, frustum):
        direction = direction.unit()

        self.position = position
        self.width = resolution[0]
        self.height = resolution[1]
        self.samples = samples
        self.depth = depth
        self.frustum = Frustum._make(frustum)

        # Calculate the screen dimensions given the FOV
        screen_width = tan(radians(FOV / 2.0))
        screen_height = (float(self.height) / float(self.width)) * screen_width

        # Calculate the coordinate frame for screenspace
        i_star = cross(direction, up).unit()
        j_star = cross(i_star, direction).unit()

        # Compute the dimensions of a pixel represented in screenspace
        self.i_hat = i_star * (2 * screen_width / self.width)
        self.j_hat = j_star * (2 * screen_height / self.height)

        # The top left of the screenspace is the origin of our image
        self.origin = (direction
                       - (i_star * screen_width)
                       + (j_star * screen_height))

    def __str__(self):
        return "Camera (p: {}, w:{}, h: {}, ih: {}, jh: {})".format(self.position, self.width, self.height, abs(self.i_hat), abs(self.j_hat))

def capture(scene, camera, verbose, draw_heatmap):
    global total_rays
    total_rays = 0

    # Create the empty pixel array to convert to an image
    pixels = []
    metadata = []

    begin = time()

    # Build the image one pixel at a time
    for y in range(camera.height):
        pixels.append([])
        metadata.append([])
        for x in range(camera.width):
            pixel, data = get_pixel(scene, camera, x, y)
            pixels[y].append(pixel)
            metadata[y].append(data)

    print("Total tracing time: {:.2f}s".format(time() - begin))

    if verbose:
        per_pixel = float(total_rays)/float(camera.width * camera.height)
        print("Total number of rays traced: {}, Average per pixel: {}".format(total_rays, per_pixel))
        print("Mean time per pixel: [], Median: [], Max: []")
        begin = time()

    # Convert our array from what is essentially a bitmap to an image
    image = Color.image_from_pixels(pixels, (camera.width, camera.height))
    heatmap = None

    if draw_heatmap:
        heatmap = Color.heatmap_from_data(metadata, (camera.width, camera.height))

    if verbose:
        print("Image processing time: {:.2f}s".format(time() - begin))

    return image, heatmap

def get_pixel(scene, camera, x, y):
    pixel = Color.black

    begin = time()

    # Collect samples of the scene for this current pixel
    for _ in range(camera.samples):
        # Randomly generate offsets for the current subsample
        x_n = x + uniform(0, 1)
        y_n = y + uniform(0, 1)

        # Get the subsample position and construct a ray from it
        screen_coordinate = camera.origin + camera.i_hat * x_n - camera.j_hat * y_n
        sample = Ray(camera.position, screen_coordinate)

        pixel = pixel + trace(scene, sample, camera.depth, camera.frustum)

    # Color correction
    pixel = pixel / camera.samples
    #TODO: check how this looks with transform
    #pixel = pixel.apply_transform(sqrt)

    endtime = time()

    return pixel, endtime - begin

def trace(scene, ray, depth, frustum):
    # Base case; try changing the color and seeing what you get!
    if depth <= 0:
        return Color.black

    # Check to see if our ray hits an object, or just shoots into space
    intersect = cast_ray(scene, ray, frustum)
    if intersect:
        #return Color.black
        # Get the color of that object and the bounce vector for recursion if there is recursion
        sample, bounce = intersect.material.scatter(ray, intersect, scene_refraction_index)

        #TODO: check how this looks with color
        # Here is the actual color blending; it's very simple
        return sample * trace(scene, bounce, depth - 1, frustum) if bounce else Color.black
    else:
        #return Color.white
        return Color.sky_gradient(ray.direction.z)

def cast_ray(scene, ray, frustum):
    global total_rays
    total_rays += 1

    closest = None

    for shape in scene:
        intersect = shape.intersect_ray(ray, Frustum(frustum.near, (closest.distance if closest else frustum.far)))
        if intersect:
            closest = intersect

    return closest
