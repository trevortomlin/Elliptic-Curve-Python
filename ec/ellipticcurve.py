import math
import copy
import matplotlib.pyplot as plt

#Curve25519 = y^2 = x^3 + 48662x^2 + x
#Coefficients are stored [b, x, x^2, ..., x^n]
#CURVE_COEFFICIENTS = [0, 1, 48662, 1]
#CURVE_COEFFICIENTS = [1, -1, 0, 1]

#CURVE_COEFFICIENTS = [10, -7, 0, 1]
CURVE_COEFFICIENTS = [3, -1, 0, 1]

#CURVE_COEFFICIENTS = [7, 0, 0, 1]
#P = 2^255-19

#P = 487
P = 127

#P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1

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

	def __init__(self, curve):

		self.curve = curve

		# if x is not None and y is not None:
		# 	self.x, self.y = x, y

		# if hex_pt is not None:
		# 	hex_to_point(hex_pt)

	def from_xy(self, x, y):
		self.x, self.y = x, y

	def from_x_sign(self, x, sign):
		pass

	def from_hex(self, hex_pt):

		# Uncompressed Point
		if len(hex_pt) == (self.curve.keysize // 2) + 2:
			self.x, self.y = self.hex_to_coords(hex_pt)
		# Compressed Point
		elif len(hex_pt) == (self.curve.keysize // 4) + 2:
			pass

	def point_to_hex(self):
		#return hex(self.x)[2:].zfill(self.curve.keysize // 2) + hex(self.y)[2:].zfill(self.curve.keysize // 2)
		return "04" + hex(self.x)[2:].zfill(self.curve.keysize // 4) + hex(self.y)[2:].zfill(self.curve.keysize // 4)

	def point_to_hex_compressed(self):
		pass

	def hex_to_coords(self, hex_pt):
		x = int(hex_pt[2:66], 16)
		y = int(hex_pt[66:], 16)
		return x,y


	def hex_to_coords_compressed(self, hex_pt):
		pass

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
		l = self.curve.tangent(self)
		#x = l**2 - 2 * self.x
		#y = l * (self.x - x) - self.y
		x = (l**2 - 2 * self.x) % self.curve.p 
		y = (l * (self.x - x) - self.y) % self.curve.p  
		r = Point(x, y, self.curve)
		return r

	def __neg__(self):
		n = Point(self.x, -self.y % self.curve.p, self.curve)
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
		#print(self.x - b.x)
		x = (s**2 - self.x - b.x) % self.curve.p 
		y = (s * (self.x - x) - self.y) % self.curve.p  
		r = Point(x, y, self.curve)

		return r

	def __sub__(self, b):
		return self + -b

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class Curve:

	def __init__(self, coefficients, p, keysize=256):
		self.coefficients = coefficients
		self.p = p
		self.discriminant = 4 * self.coefficients[1]**3 + 27 * self.coefficients[0]**2
		self.keysize = keysize

	def valid(self, a: Point):
		try:
			return a.y**2 % self.p == (pow(a.x, 3, self.p) + self.coefficients[1] * a.x + self.coefficients[0]) % self.p
		except TypeError:
			return False

	def calcValidPoints(self):

		# Use baby step method here to improve speed

		validPoints = []
		
		for x in range(self.p):
			for y in range(self.p):
				if (y ** 2) % self.p == ((x ** 3) + self.coefficients[1] * x + self.coefficients[0]) % self.p:
					validPoints.append((x,y))


		self.numPoints = len(validPoints)

		return validPoints

	def graphPoints(self):
		points = self.calcValidPoints()
		print(points)
		xs = [i[0] for i in points]
		ys = [i[1] for i in points]
		fig, ax = plt.subplots()
		ax.scatter(xs, ys)
		plt.axline((0, self.p/2), (self.p, self.p/2))
		plt.show()

	def evaluate(self, x, sign: int) -> float:

		y2 = 0

		for index in range(len(self.coefficients)):

			y2 += self.coefficients[index] * x ** index

			#https://crypto.stackexchange.com/questions/20667/modulo-square-roots
			y = pow(y2, ((self.p+1)//4), self.p)

		if sign == -1:
			y = self.p - y
		#y = min(y, self.p-y)

		return y

	def tangent(self, a: Point) -> float:

		t = (3 * a.x**2 + self.coefficients[1]) * inv_mod_p((2 * a.y), self.p)
		return t

	def secant(self, a: Point, b: Point):
		try:
			s = (b.y - a.y) * inv_mod_p((b.x - a.x), self.p)
			#print(s)
			return s
		except ZeroDivisionError as e:
			print("Points cannot be the same.", e)
			return 0

	def __str__(self):
		return "Elliptic Curve defined by y^2 = " + str(self.coefficients[3]) + "x^3 + " + str(self.coefficients[1]) + "x + " + str(self.coefficients[0]) + " in 𝔽" + str(self.p)

def main():

	ec_curve = Curve(CURVE_COEFFICIENTS, P)

	# print(ec_curve)
	
	# x = 16
	# y = ec_curve.evaluate(x, -1)

	# p = Point(x, y, ec_curve)

	# print(p)
	# print(ec_curve.valid(p))

	# x1 = 41
	# y1 = ec_curve.evaluate(x1, 1)

	# q = Point(x1, y1, ec_curve)

	# print(q)
	# print(ec_curve.valid(q))

	# r = p + q
	# print(r)
	# print(ec_curve.valid(r))

	# l = p + p
	# print(l)
	# print(ec_curve.valid(l))
 
	# m = p * 4
	# print(m)
	# print(ec_curve.valid(m))

	# ec_curve.calcValidPoints()
	# print(p.point_to_hex())

	x2 = 100000000000000000000000000025
	y2 = ec_curve.evaluate(x2, 1)

	v = Point(ec_curve)
	v.from_xy(x2, y2)
	print(v)
	print(ec_curve.valid(v))
	print(v.point_to_hex())

	l = Point(ec_curve)
	l.from_hex(v.point_to_hex())
	print(l)

	#o = Point("040000000000000000000000000000000000000001431e0fae6d7217caa00000190000000000000000000000000000000000000000000000000000000000000057", ec_curve)
	#print(len(v.point_to_hex()))

	#print(len("0479BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8"))

	#print(int("0x0000000000000000000000000000000000000000000000000000000000000010", 16))


	#print(ec_curve.calcValidPoints())
	#ec_curve.graphPoints()

	#print(ec_curve.secant(p, q))

	# r = p + q

	# print(p, q, r)

	# print(Point.double(p))

if __name__ == "__main__":
	main()