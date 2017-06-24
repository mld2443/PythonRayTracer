from collections import namedtuple
from math import radians, atan, sqrt
from random import uniform
from Utility.Vector import *
from Utility.Color import *
import Shapes

Camera = namedtuple('Camera', 'position direction width height FOV')

# Global settings
scene_refraction_index = 1.0
up = Vector(0,0,1)

def capture(camera, scene, sampling, depth):
    # calculate the screen dimensions given the FOV
    screen_width = atan(radians(camera.FOV / 2.0))
    screen_height = (float(camera.height) / float(camera.width)) * screen_width

    # calculate the coordinate frame for screenspace
    i_hat = cross(camera.direction, up).unit()
    j_hat = cross(i_hat, camera.direction).unit()

    # compute the dimensions of a pixel represented in screenspace
    deltaX = i_hat * (2 * screen_width / camera.width)
    deltaY = j_hat * (2 * screen_height / camera.height)

    # grab the top left of the screenspace as the starting point for our image
    top_left = camera.position + camera.direction - (i_hat * screen_width) + (j_hat * screen_height)

    # create the empty pixel array to convert to an image
    pixels = []

    for y in range(camera.height)
        for x in range(camera.width)
            pixel_position = top_left + x * deltaX - y * deltaY
            pixels[y][x] = get_pixel(scene, pixel_position, (deltaY, deltaY), depth)

    return image_from_pixels(pixels, (camera.width, camera.height))

def get_pixel(scene, position, samples, pixel_size, depth):
    pixel = black

    # collect samples of the scene for this current pixel
    for _ in range(samples):
        # randomly generate offsets for the current subsample
        random_offset = pixel_size[0] * uniform(0,1) - pixel_size[1] * uniform(0,1)

        # get the subsample position and construct a ray from it
        subsample = position + random_offset
        ray = Ray(position, subsample - position)

        pixel = pixel + trace(ray, scene, depth)

    # Color correction
    pixel = pixel / samples
    #pixel = pixel.apply_transform(sqrt)

    return pixel.quantize()

def trace(ray, scene, depth):
    return black if depth <= 0

    intersect = cast_ray(scene, ray, frustrum)
    if intersect:
        color, bounce = intersect.material.scatter(ray, intersect, scene_refraction_index)

        return color * trace(bounce, scene, depth - 1) if bounce else black
    else:
def sky_gradient(direction):
    interpolate = (0.5 * (direction.y + 1)) #**0.5
    return white * (1 - interpolate) + Color(0.5, 0.7, 1.0) * interpolate

def cast_ray(ray, scene, frustum):
    closest = None

    for shape in scene:
        intersect = shape.intersect_ray(ray, (frustrum.near, (closest.dist if closest else frustum.far)))
        if intersect:
            closest = intersect

    return closest
