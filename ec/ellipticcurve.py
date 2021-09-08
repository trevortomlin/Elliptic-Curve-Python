import math
import copy
import matplotlib.pyplot as plt

#Curve25519 = y^2 = x^3 + 48662x^2 + x
#Coefficients are stored [b, x, x^2, ..., x^n]
#CURVE_COEFFICIENTS = [0, 1, 48662, 1]
CURVE_COEFFICIENTS = [1, -1, 0, 1]
#P = 2^255-19
P = 97

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

	def __init__(self, x, y, curve):

		self.x, self.y = x, y
		self.curve = curve

	def __truediv__(self, n):
		raise Exception("Points cannot be divided.")

	def __floordiv__(self, n):
		raise Exception("Points cannot be floor divided.")

	def __mul__(self, n: int):
		
		if type(n) is Point:
			raise Exception("Points cannot be multiplied.")

		bits = bin(n)[2:][::-1]

		r = copy.copy(self)

		for bit in bits:
			if bit == "1" and bits.index(bit) != 0:
				r += r
			r = self.double()

		return r

	def __rmul__(self, n):

		if type(n) is Point:
			raise Exception("Points cannot be multiplied.")

		return self * n

	def double(self):
		l = self.curve.tangent(self)
		x = l**2 - 2 * self.x
		y = l * (self.x - x) - self.y
		r = Point(x, y, self.curve)
		return r

	def __neg__(self):
		n = Point(x, -y)
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
				return self.double(b)

		s = self.curve.secant(self, b)
		x = (s**2 - self.x - b.x) % self.curve.p 
		y = (-1 * self.y + s * (self.x - x)) % self.curve.p  
		r = Point(x, y, self.curve)
		return r

	def __sub__(self, b):
		return self + -b

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class Curve:

	def __init__(self, coefficients, p):
		self.coefficients = coefficients
		self.p = p

	def valid(self, a: Point):
		try:
			return a.y**2 % self.p == (pow(a.x, 3, self.p) + self.coefficients[1] * a.x + self.coefficients[0]) % self.p
		except TypeError:
			return False

	def calcValidPoints(self):

		validPoints = []
		
		for x in range(self.p):
			for y in range(self.p):
				if (y ** 2) % self.p == ((x ** 3) + self.coefficients[1] * x + self.coefficients[0]) % self.p:
					validPoints.append((x,y))

		return validPoints

	def graphPoints(self):
		points = self.calcValidPoints()
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

		return math.sqrt(y2) * sign

	def tangent(self, a: Point) -> float:

		t = (3 * a.x**2 + self.coefficients[1]) / inv_mod_p((2 * a.y), self.p)
		return t

	def secant(self, a: Point, b: Point):
		try:
			s = (b.y - a.y) / inv_mod_p((b.x - a.x), self.p)
			return s
		except ZeroDivisionError as e:
			print("Points cannot be the same.", e)
			return 0

def main():

	ec_curve = Curve(CURVE_COEFFICIENTS, P)
	
	x = 1
	y = ec_curve.evaluate(x, 1)

	p = Point(x, y, ec_curve)

	print(p)
	print(ec_curve.valid(p))

	x1 = 3
	y1 = ec_curve.evaluate(x1, -1)

	q = Point(x1, y1, ec_curve)

	print(q)
	print(ec_curve.valid(q))

	r = p + q
	print(r)
	print(ec_curve.valid(r))

	#print(ec_curve.calcValidPoints())
	ec_curve.graphPoints()

	# print(ec_curve.secant(p, q))

	# r = p + q

	# print(p, q, r)

	# print(Point.double(p))

if __name__ == "__main__":
	main()