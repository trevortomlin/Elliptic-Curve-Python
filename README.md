# Elliptic-Curve-Python

![Bower](https://img.shields.io/bower/l/a?style=plastic)\
\
Implements Elliptic Curves and example uses in Python.

## Description

This project recreates Elliptic Curves over Finite Fields in Python. It supports all elliptic curve operations such as addition and multiplication over a Finite Field. There are also example implementations of Elliptic Curve Diffie Hellman Exchange and Elliptic Curve Digital Signature Algorithm.

## Installation

`
git clone https://github.com/trevortomlin/Elliptic-Curve-Python.git
`

### If you want to use the module in your own project:
`
cp ellipticcurve.py ~/location_of_your_project/
`

## Usage

| :exclamation:  Do not use this in production code!   |
|------------------------------------------------------|

```python
from ellipticcurve import Curve, Point

# Coefficients are store [b, x, 0, x^3].
# P is the field that the curve is defined over.
CURVE_COEFFICIENTS = [15, -2, 0, 1]
P = 23

ec_curve = Curve(CURVE_COEFFICIENTS, P)

Q = Point(ec_curve)
Q.from_xy(4, 5)

L = Point(ec_curve)
L.from_xy(9, 17)

print(Q + L)

print(3 * Q)

```

Output:
`
(13, 1)
(13, 22)
`

## Technologies Used

Python, hashlib, matplotlib

## Improvements

- Add @dataclasses to Point class.
- Implement more efficient Point counting algorithm.
- Add more checks for incorrect usage.
- Rename variable and function names to fit PEP-8 standard.

## References

[Wikipedia](https://en.wikipedia.org/wiki/Elliptic_curve)\
[Andrea Corbellini ECC](https://andrea.corbellini.name/ecc/interactive/modk-add.html)\
[Bitcoin Book](https://github.com/bitcoinbook/bitcoinbook/blob/develop/ch04.asciidoc)\
[Crypto Book](https://cryptobook.nakov.com/digital-signatures/ecdsa-sign-verify-messages)

## License

This project is licensed under the  MIT License - see the LICENSE file for details.
