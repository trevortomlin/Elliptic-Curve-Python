from ellipticcurve import Curve, Point

CURVE_COEFFICIENTS = [3, -1, 0, 1]
P = 127

def main():

	#Define Curve
	ec_curve = Curve(CURVE_COEFFICIENTS, P)

	# Generator Point
	G = Point(ec_curve)
	G.from_xy(16, 107)

	# Private Keys
	alice_d = 2001
	bob_d = 596

	# Public Keys
	alice_Q = alice_d * G
	bob_Q = bob_d * G

	# Swapping and mixture of Pub Keys
	alice_s = alice_d * bob_Q
	bob_s = bob_d * alice_Q

	print(alice_s)
	print(bob_s)

	assert(alice_s == bob_s)

if __name__ == "__main__":
	main()