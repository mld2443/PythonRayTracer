from math import radians, atan
from collections import namedtuple

Dimensions = namedtuple('Dimensions', 'w h')

def capture(camera, scene, dimensions, sampling, depth = 5):
    # calculate the screen dimensions given the FOV
    screen_width = atan(radians(FOV / 2.0))
    screen_height = (float(dimensions.h) / float(dimensions.w)) * screen_width

    # calculate the coordinate frame for screenspace
    X₀ = cross(lookDirection, upDirection).unit
    Y₀ = cross(lookDirection, X₀).unit

    # compute the average width of a pixel represented in screenspace
    ∆X = (2.0 * screen_width * X₀) / float(dimensions.w)
    ∆Y = (2.0 * screen_height * Y₀) / float(dimensions.h)

    # grab the top left of the screenspace as the starting point for our image
    top_left = position + look_direction - (X₀ * screen_width) - (Y₀ * screen_height)

    # create the empty pixel array to convert to an image
    pixels = []

    for y in range(dimensions.h)
        for x in range(dimensions.w)
            pixel_position = top_left + x * ∆X + y * ∆Y
            pixels[y][x] = get_pixel(scene, pixel_position, sampling, (∆X, ∆Y), depth)

    return image_from_pixels(pixels, dimensions)

def get_pixel(scene, position, sampling, dims, depth):
    return Color(1.0,1.0,1.0)

def image_from_pixels(pixels, dimensions):
