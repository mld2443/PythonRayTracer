class Color:
    """A class that holds RGB values with floating point precision"""

    def __init__(self, red, green, blue):
        self.rgb = [red, green, blue]

    def __getitem__(self, key):
        return self.rgb[key]

    def __eq__(self, rhs):
        if isinstance(rhs, Color):
            return self.rgb == rhs.rgb
        else:
            return NotImplemented

    def __str__(self):
        return '{:02X}{:02X}{:02X}'.format(int(255*self[0]), int(255*self[1]), int(255*self[2]))

    def __repr__(self):
        return "0x" + self.__str__()

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
