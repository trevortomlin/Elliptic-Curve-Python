import math

#Curve25519 = y^2 = x^3 + 48662x^2 + x
#Coefficients are stored [x, x^2, ..., x^n]
CURVE_COEFFICIENTS = [1, 48662, 1]


class Point:

	def __init__(self, x, y):

		self.x, self.y = x, y

	def __add__(self, b):
		s = Curve.secant(self, b)
		x = s**2 - 2.0 * self.x
		y = self.x + s * (x - self.x)
		r = Point(x, y)
		return r

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

class Curve:

	def __init__(self, coefficients, p):
		self.coefficients = coefficients
		self.p = p

	def evaluate(self, x, sign: int) -> float:

		y2 = 0

		for index in range(len(self.coefficients)):

			y2 += self.coefficients[index] * x ^ index+1

		return math.sqrt((y2 % self.p)) * sign

	@staticmethod
	def secant(a: Point, b: Point) -> float:
		try:
			s = (b.y - a.y) / (b.x - a.x)
			return s
		except ZeroDivisionError as e:
			print("Points cannot be the same.", e)
			return 0.0

def main():

	ec_curve = Curve(CURVE_COEFFICIENTS, 2^255-19)
	
	x = 1
	y = ec_curve.evaluate(x, 1)

	p = Point(x, y)

	x1 = 2
	y1 = ec_curve.evaluate(x1, -1)

	q = Point(x1, y1)	

	#print(y, y1)
	#print(Curve.secant(p, q))

	r = p + q

	print(p, q, r)
	#print(p + q + r)

	

if __name__ == "__main__":
	main()