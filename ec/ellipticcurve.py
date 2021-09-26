import math
import copy
import matplotlib.pyplot as plt

#https://stackoverflow.com/questions/31074172/elliptic-curve-point-addition-over-a-finite-field-in-python
def inv_mod_p(x, p):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % p == 0:
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p-2, p)

class Point:
	"""
	Description:
		Describes a point on a finite curve.

	Functions:
		from_xy()
		from_hex()
		point_to_hex() -> str
		point_to_hex_compressed() -> str
		hex_to_coords() -> (x, y)
		hex_to_coords_compressed() -> (x, y)
		double() -> Point

	Variables:
		curve
		x
		y

	"""

	def __init__(self, curve):
		self.curve = curve

	def from_xy(self, x, y):
		"""
		Creates a point from x and y values.
		"""
		self.x, self.y = x, y

	def from_hex(self, hex_pt):
		"""
		Creates point from uncompressed or compressed hex value.
		"""
		print(len(hex_pt))
		print((self.curve.keysize // 4) + 4)

		# Uncompressed Point
		if len(hex_pt) == (self.curve.keysize // 2) + 4:
			self.x, self.y = self.hex_to_coords(hex_pt)
		# Compressed Point
		elif len(hex_pt) == (self.curve.keysize // 4) + 4:
			self.x, self.y = self.hex_to_coords_compressed(hex_pt)
		else:
			raise Exception("Not valid hex point.")

	def point_to_hex(self):
		"""
		Returns the representation of self as an uncompressed point.
		"""
		return "0x04" + hex(self.x)[2:].zfill(self.curve.keysize // 4) + hex(self.y)[2:].zfill(self.curve.keysize // 4)

	def point_to_hex_compressed(self):
		"""
		Returns the representation of self as a compressed point.
		"""
		lsb = self.y & 1

		if lsb == 1:
			return "0x02" + hex(self.x)[2:].zfill(self.curve.keysize // 4)
		elif lsb == 0:
			return "0x03" + hex(self.x)[2:].zfill(self.curve.keysize // 4)

	def hex_to_coords(self, hex_pt):
		"""
		Converts uncompressed hex value to xy points.
		"""
		x = int(hex_pt[4:68], 16)
		y = int(hex_pt[68:], 16)
		return x,y

	def hex_to_coords_compressed(self, hex_pt):
		"""
		Converts compressed hex value to xy points.
		"""
		byte = hex_pt[:4]
		lsb = 0 
		if byte == "0x02":
			lsb = 1
		elif byte == "0x03":
			lsb = 0

		x = int(hex_pt[4:], 16)
		y = self.curve.evaluate(int(hex_pt[4:], 16), lsb)
		return x,y

	def __eq__(self, n):
		if isinstance(n, Point):
			return self.x == n.x and self.y == n.y
			
	def __truediv__(self, n):
		raise Exception("Points cannot be divided.")

	def __floordiv__(self, n):
		raise Exception("Points cannot be floor divided.")

	def __mul__(self, n: int):
		if type(n) is Point:
			raise Exception("Points cannot be multiplied.")

		bits = bin(n)[2:][::-1]

		Q = 0
		N = copy.copy(self)

		for bit in bits:
			if bit == "1":
				Q = N + Q
			N = N.double()

		return Q

	def __rmul__(self, n):
		if type(n) is Point:
			raise Exception("Points cannot be multiplied.")

		return self * n

	def double(self):
		"""
		Returns point that is double self.
		"""
		l = self.curve.tangent(self)
		x = (l**2 - 2 * self.x) % self.curve.p 
		y = (l * (self.x - x) - self.y) % self.curve.p  
		r = Point(self.curve)
		r.from_xy(x, y)
		return r

	def __neg__(self):
		n = Point(self.curve)
		n.from_xy(self.x, -self.y % self.curve.p)
		return n

	def __add__(self, b):
		#P+O=P
		if b == 0:
			return self

		#P+-P=O
		if self.x == b.x: 
			if self.y == -b.y:
				return 0
			#P+P=2P
			elif self.y == b.y:
				return self.double()

		s = self.curve.secant(self, b)
		x = (s**2 - self.x - b.x) % self.curve.p 
		y = (s * (self.x - x) - self.y) % self.curve.p  
		r = Point(self.curve)
		r.from_xy(x, y)

		return r

	def __sub__(self, b):
		return self + -b

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class Curve:
	"""
	Description:
		Describes a Curve over Finite Field P with the coefficients stored as [b, x, 0, x^3]
	
	Functions:
		valid() -> bool
		calcValidPoint() -> list of points
		graphPoints() -> float
		evaluate(x, sign) -> float
		tangent(a) -> float
		secant(a, b) -> float

	Variables:
		coefficients
		p
		discriminant
		keysize
		numPoints
	"""

	def __init__(self, coefficients, p, keysize=256):
		self.coefficients = coefficients
		self.p = p
		self.keysize = keysize

		# Can be used later to check for validity of curve.
		self.discriminant = 4 * self.coefficients[1]**3 + 27 * self.coefficients[0]**2

	def valid(self, a: Point):
		"""
		Determines whether a given point is valid on this curve.
		"""

		try:
			return a.y**2 % self.p == (pow(a.x, 3, self.p) + self.coefficients[1] * a.x + self.coefficients[0]) % self.p
		except TypeError:
			return False

	def calcValidPoints(self):
		"""
		Calculates the number of points on the curve and stores each point in a list.
		"""

		# Use baby step method here to improve speed
		validPoints = []
		
		for x in range(self.p):
			for y in range(self.p):
				if (y ** 2) % self.p == ((x ** 3) + self.coefficients[1] * x + self.coefficients[0]) % self.p:
					validPoints.append((x,y))

		self.numPoints = len(validPoints)

		return validPoints

	def graphPoints(self):
		"""
		Graphs the points on the curve using Matplotlib.
		"""

		points = self.calcValidPoints()
		print(points)
		xs = [i[0] for i in points]
		ys = [i[1] for i in points]
		fig, ax = plt.subplots()
		ax.scatter(xs, ys)
		plt.axline((0, self.p/2), (self.p, self.p/2))
		plt.show()

	def evaluate(self, x, sign: int) -> float:
		"""
		Gets the y value from a given x value from the curve.
		"""

		y2 = 0

		for index in range(len(self.coefficients)):

			y2 += self.coefficients[index] * x ** index

			#https://crypto.stackexchange.com/questions/20667/modulo-square-roots
			y = pow(y2, ((self.p+1)//4), self.p)

		if sign == 0:
			y = self.p - y

		return y

	def tangent(self, a: Point) -> float:
		"""
		Returns the tangent of a point.
		"""

		t = (3 * a.x**2 + self.coefficients[1]) * inv_mod_p((2 * a.y), self.p)
		return t

	def secant(self, a: Point, b: Point):
		"""
		Returns the secant of a point.
		"""
		try:
			s = (b.y - a.y) * inv_mod_p((b.x - a.x), self.p)
			return s
		except ZeroDivisionError as e:
			print("Points cannot be the same.", e)
			return 0

	def __str__(self):
		return "Elliptic Curve defined by y^2 = " + str(self.coefficients[3]) + "x^3 + " + str(self.coefficients[1]) + "x + " + str(self.coefficients[0]) + " in 𝔽" + str(self.p)