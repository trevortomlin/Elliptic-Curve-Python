import math
import copy

#Curve25519 = y^2 = x^3 + 48662x^2 + x
#Coefficients are stored [b, x, x^2, ..., x^n]
#CURVE_COEFFICIENTS = [0, 1, 48662, 1]
CURVE_COEFFICIENTS = [1, -1, 0, 1]
#P = 2^255-19
P = 97

class Point:

	def __init__(self, x, y, curve):

		self.x, self.y = x, y
		self.curve = curve

	def __mul__(self, n: int):
		
		bits = bin(n)[2:][::-1]

		r = copy.copy(self)

		for bit in bits:
			if bit == "1" and bits.index(bit) != 0:
				r += r
			r = self.double()

		return r

	def __rmul__(self, n):
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

		if b == 0:
			return self

		if self.x == b.x: 
			if self.y == -b.y:
				return 0
			elif self.y == b.y:
				return 0

		s = Curve.secant(self, b)
		x = s**2 - self.x - b.x
		y = -1 * self.y + s * (self.x - x)
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

	def evaluate(self, x, sign: int) -> float:

		y2 = 0

		for index in range(len(self.coefficients)):

			y2 += self.coefficients[index] * x ** index

		return math.sqrt((y2 % self.p)) * sign

	def tangent(self, a: Point) -> float:

		t = (3 * a.x**2 + self.coefficients[1]) / (2 * a.y)
		return t

	@staticmethod
	def secant(a: Point, b: Point) -> float:
		try:
			s = (b.y - a.y) / (b.x - a.x)
			return s
		except ZeroDivisionError as e:
			print("Points cannot be the same.", e)
			return 0.0

def main():

	ec_curve = Curve(CURVE_COEFFICIENTS, P)
	
	x = 1
	y = ec_curve.evaluate(x, 1)

	p = Point(x, y, ec_curve)

	x1 = 2
	y1 = ec_curve.evaluate(x1, -1)

	q = Point(x1, y1, ec_curve)

	print(Curve.secant(p, q))

	r = p + q

	print(p, q, r)

	print(Point.double(p))
	
if __name__ == "__main__":
	main()