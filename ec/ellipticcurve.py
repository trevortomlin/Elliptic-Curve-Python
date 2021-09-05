import math

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
		pass

	def double(self):
		l = self.curve.tangent()
		x = s**2 - self.x - b.x
		y = -1 * self.y + s * (self.x - x)
		r = Point(x, y, self.curve)

	def __neg__(self):
		n = Point(x, -y)
		return n

	def __add__(self, b):

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

			y2 += self.coefficients[index] * x ^ index

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

if __name__ == "__main__":
	main()