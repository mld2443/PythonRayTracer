from random import gauss
from operator import mul,sub

class Vector:
	def __init__(self, xyz):
		self.xyz = xyz

	def __repr__(self):
		return self.xyz.__repr__()

	def __str__(self):
		return self.xyz.__str__()

	def __getitem__(self, index):
		return self.xyz[index]

	def mag(self):
		"""sqrt(x*x + y*y + z*z)"""
		return sum(x**2 for x in self.xyz) ** 0.5

	def unit(self):
		"""Normalization, divide all elements by magnitude of Vector"""
		return Vector([x/self.mag() for x in self.xyz])

	def __add__(self, rhs):
		if isinstance(rhs, Vector):
			return Vector(list(map(sum, zip(self.xyz, rhs.xyz))))
		else:
			return NotImplemented

	def __sub__(self, rhs):
		if isinstance(rhs, Vector):
			return Vector(list(map(sub, self.xyz, rhs.xyz)))
		else:
			return NotImplemented

	def __mul__(self, rhs):
		"""Dot-product and integer product"""
		if isinstance(rhs, Vector):
			return sum(map(mul, self.xyz, rhs.xyz))
		elif isinstance(rhs, (int, float)):
			return Vector([x * rhs for x in self.xyz])
		else:
			return NotImplemented

	def __matmul__(self, rhs):
		"""Cross-product"""
		if isinstance(rhs, Vector):
			return Vector([self[1]*rhs[2] - self[2]*rhs[1],
        	 self.xyz[2]*rhs[0] - self[0]*rhs[2],
        	 self.xyz[0]*rhs[1] - self[1]*rhs[0]])

def rand_unit_vector():
	return Vector([gauss(0, 1) for i in range(3)]).unit()

#MARK: Linear algebra functions

def reflect(dir, normal):
    """Reflect a vector across a surface,
    assumes dir and normal are unit vectors"""
    return (dir - normal * (2 * (dir * normal))).unit()

def refract(dir, normal):
	"""refract a vector on surface with normal
	and eta of refraction index ratio"""
	#TODO Implement this function
	return dir
