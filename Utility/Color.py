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
        return Color(self.r*rhs, self.g*rhs, self.b*rhs) if isinstance(rhs, (int, float)) else NotImplemented

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

#MARK: PIL implementation

def image_from_pixels(pixels, dimensions):
    # Start with a blank image
    image = Image.new('RGB', dimensions, black.quantize())

    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            image.putpixel((x, y), pixels[y][x])

    # This would be a good place to do any post-processing on our image
    # PIL in python 3 uses the Pillow library
    return image
