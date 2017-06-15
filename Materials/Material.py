class Material(object):
    """Class to contain all the properties
        of how light interacts with a material
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def scatter():
        # Must define how to scatter incoming rays
        pass

def schlick(cosine, index):
    # The Schlick approximation of the Fresnel equation
    r0 = (1 - index) / (1 + index)
    r0 = r0 ** 2
    return r0 + (1 - r0) * ((1 - cosine) ** 5)
