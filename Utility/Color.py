from PIL import Image
from collections import namedtuple

class Color(namedtuple('Color', 'r g b')):
    """A class that holds RGB values with floating point precision"""

    def apply_transform(self, func):
        return Color._make(map(func, self))

    def quantize(self):
        # Convert from floating point to 8-bit values for each color channel
        return self.apply_transform(lambda x: min(max(int(255*x),0),255))

    def __add__(self, rhs):
        return Color(self.r+rhs.r, self.g+rhs.g, self.b+rhs.b) if isinstance(rhs, Color) else NotImplemented

    def __mul__(self, rhs):
        if isinstance(rhs, (int, float)):
            return Color(self.r*rhs, self.g*rhs, self.b*rhs)
        elif isinstance(rhs, Color):
            return Color(self.r*rhs.r, self.g*rhs.g, self.b*rhs.b)
        return NotImplemented

    def __truediv__(self, rhs):
        if isinstance(rhs, (int, float)):
            return Color(self.r/rhs, self.g/rhs, self.b/rhs)
        elif isinstance(rhs, Color):
            return Color(self.r/rhs.r, self.g/rhs.g, self.b/rhs.b)
        return NotImplemented

    def __str__(self):
        return '{:02X}{:02X}{:02X}'.format(int(255*self.r), int(255*self.g), int(255*self.b))

#MARK: Named color defenitions

black = Color(0.0,0.0,0.0)
darkgrey = Color(0.3,0.3,0.3)
lightgrey = Color(0.7,0.7,0.7)
white = Color(1.0,1.0,1.0)
red = Color(1.0,0.0,0.0)
green = Color(0.0,1.0,0.0)
blue = Color(0.0,0.0,1.0)
yellow = Color(1.0,1.0,0.0)
magenta = Color(1.0,0.0,1.0)
cyan = Color(0.0,1.0,1.0)

################
# Sky gradient #
################
# It's important this be bright, as it's the
# source of much of the light of the scene.
def sky_gradient(angle):
    #TODO: Check how this looks with curve correction
    interpolate = (0.5 * (angle + 1)) #**0.5
    return white * (1 - interpolate) + Color(0.5, 0.7, 1.0) * interpolate

def heat_gradient(value):
    curve = 1.0/3.0
    red = min(max(int(255 * (value)**(curve)), 0), 255)
    cyan = min(max(int(255 * (1 - value)**(curve)), 0), 255)
    return (red,cyan,cyan)

def normalize(data):
    lo = hi = data[0][0]

    for row in data:
        for element in row:
            if element > hi:
                hi = element
            elif element < lo:
                lo = element

    span = hi - lo
    return [[(e - lo)/span for e in row] for row in data]

#MARK: PIL implementation

def heatmap_from_data(data, dimensions):
    # Start with a black image
    image = Image.new('RGB', dimensions, (0,0,0))

    data = normalize(data)

    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            image.putpixel((x, y), heat_gradient(data[y][x]))

    return image

def image_from_pixels(pixels, dimensions):
    # Start with a black image
    image = Image.new('RGB', dimensions, (0,0,0))

    # Quantize will convert a pixel from floating point to 8bit
    # colorspace. I do this by clipping any value greater than the
    # max. Another way to do this is to normalize all values with
    # the largest all at once after calculating all the pixels.
    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            image.putpixel((x, y), pixels[y][x].quantize())

    # This would be a good place to do any post-processing on the image
    # For reference, PIL in python 3 uses the Pillow library

    return image
