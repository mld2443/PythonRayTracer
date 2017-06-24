from collections import namedtuple
from math import radians, atan, sqrt
from Utility.Vector import *
from Utility.Color import *

Camera = namedtuple('Camera', 'position direction width height FOV')

def capture(camera, scene, sampling, depth, up = Vector(0,0,1)):
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
    return pixel
