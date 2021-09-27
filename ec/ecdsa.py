from ellipticcurve import Curve, Point
import hashlib
import random

#############################
#   	   					#
#	Made by Trevor Tomlin	#
#	Date: 9/27/21			#
#	ecdsa.py				#
#							#
#############################	

# Hardcoded values are from https://www.youtube.com/watch?v=6TI5YOpnrgI for testing.

CURVE_COEFFICIENTS = [15, -2, 0, 1]
P = 23
random.seed(42)

def main():

	# Define Curve
	ec_curve = Curve(CURVE_COEFFICIENTS, P)

	# Generator Point
	G = Point(ec_curve)
	G.from_xy(4, 5)

	# Private Key
	priv = 3

	# Public Key
	pub = priv * G

	# Message
	msg = "Hello, World!"

	# Sign and Verify
	r,s = sign(msg, priv, G)
	print(verify(msg, r, s, pub, G))


def sign(msg, priv, G):
	# Message Hash
	#h = int(hashlib.sha256(msg.encode()).hexdigest(), 16)
	h = 10

	# Generate random number less than P
	#k = random.randrange(1, P-1)
	k = 19

	# Calc Random point and take its x value
	R = k * G
	r = R.x % P

	# Modular Inverse of K
	ki = pow(k, P-2, P)

	# Create Sig
	s = (ki * (h + r * priv)) % P

	return(r, s)


def verify(msg, r, s, pub, G):
	# Message Hash
	#h = int(hashlib.sha256(msg.encode()).hexdigest(), 16)
	h = 10

	# Modular Inverse of S
	si = pow(s, P-2, P)

	# Verify Sig
	u1 = (h * si) % P
	u2 = (r * si) % P
	R1 = u1 * G + u2 * pub
	r1 = R1.x

	return r1 == r

if __name__ == "__main__":
	main()