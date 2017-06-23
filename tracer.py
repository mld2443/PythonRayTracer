from PIL import Image
from collections import namedtuple
import os

def convert(rgb):
    return tuple(int(255 * value) for value in rgb)

Size = namedtuple('Size', 'w h')

s = Size(16, 16)

data = [[(x + y)/sum(s) for x in range(s.w)] for y in range(s.h)]

im = Image.new('RGB', s, convert((0.1,0.8,0.7)))

for y in range(s.h):
    for x in range(s.w):
        im.putpixel((x,y),convert((0.1,data[y][x],data[y][x])))

path = os.path.join(os.getcwd(), "picture2.png")
try:
    file = open(path, 'wb')
    im.save(file, "PNG")
except FileNotFoundError:
    print("Something went wrong?")
