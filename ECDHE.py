import collections
import random
import matplotlib.pyplot as pyplot
import numpy as np
import math

# This creates a tuple called 'EllipticCurve' with fields 'name','p','a','b','g','n','h'
# fields are accessible by name reference (rather than integer reference to position in tuple)
EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

# An elliptic curve is defined by parameters obtained from OpenSSL secp256k1
curve = EllipticCurve(
    'secp256k1',
    # Field characteristic.
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    # Base point.
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    # Subgroup order.
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    # Subgroup cofactor.
    h=1,
)

# Check if co-ordinates (point) are on the Elliptic Curve defined above. 
# If it is, return true. If point is at infinity, return false. If it is not, return false
def is_on_curve(point):
    # point at infinity
    if point is None:
        return True
    x,y = point
    return (y*y - x*x*x - curve.a*x - curve.b) % curve.p == 0

# Generate inverse point of point on Elliptic Curve
def point_inverse(point):
    # checks that point satisfies curve relation, throws error if not
    assert is_on_curve(point)
    x, y = point
    # inverse calculated as y reflection in x axis, modulo p
    result = (x, -y % curve.p)
    # checks that new point is also on curve, throws error if not
    assert is_on_curve(result)
    # return new inverse point
    return result

# Generate 3rd point from addition of two separate points
def point_add(point1, point2):
    # Check that point1, point2 are on the Elliptic Curve, throw error if not
    assert is_on_curve(point1)
    assert is_on_curve(point2)
    # if point1 is zero, point2 = point2
    if point1 is None:
        # 0 + point2 = point2
        return point2
    # if point2 is zero, point1 = point1
    if point2 is None:
        # point1 + 0 = point1
        return point1
    
    x1, y1 = point1
    x2, y2 = point2
    # if point1 is inverse of point2 (same x, inverse y), return null
    if x1 == x2 and y1 != y2:
        return None
    # if point1 is the same as point2, special case of points on tangent
    if x1 == x2:
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        # if point1 and point2 are unique, gradient calculated
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

    # new point co-ordinates calculated from linear curve equations
    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p, -y3 % curve.p)
    # check if new point is on curve, throw error if not
    assert is_on_curve(result)
    return result

# Generate new point from scalar multiplication of point with integer k
def scalar_multiply(k, point):
    # check that point is on curve, throw error if not
    assert is_on_curve(point)
    # check if k is order of subgroup, return false
    if k % curve.n == 0:
        return None
    # if k is negative, scalar multiply the inverse point
    if k < 0:
        return scalar_multiply(-k, point_inverse(point))
    # configure loop variables
    result = None
    i = 0
    point_operation = point
    # convert scalar value to binary base 2
    k_binary = bin(k)[2:]
    # loop over each bit of base 2 representation of scalar k
    while i < len(k_binary):
        # if bit = 1, add point*2^i to running total
        if k_binary[i]:
            result = point_add(result,point_operation)
        # iterate 2^i*point
        point_operation = point_add(point_operation,point_operation)
        # iterate scalar to next bit
        i = i + 1
    # check value is still within group
    assert is_on_curve(result)
    return result

# Calculate inverse modulus of k and p
def inverse_mod(k, p):
    # calculate x such that (x * k) % p == 1 where k is non-zero and p is a prime
    # inverse of k modulo p
    if k == 0:
        raise ZeroDivisionError('division by zero')
    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # Extended Euclidean algorithm.
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p

# generate keypair (private key is random between 1 and parameter n, 
# public key is scalar multiple of private key and parameter G)
def make_keypair():
    """Generates a random private-public key pair."""
    private_key = random.randrange(1, curve.n)
    public_key = scalar_multiply(private_key, curve.g)

    return private_key, public_key

# Alice generates her own keypair.
alice_private_key, alice_public_key = make_keypair()
print("Alice's private key:", hex(alice_private_key))
print("Alice's public key: (0x{:x}, 0x{:x})".format(*alice_public_key))

# Bob generates his own key pair.
bob_private_key, bob_public_key = make_keypair()
print("Bob's private key:", hex(bob_private_key))
print("Bob's public key: (0x{:x}, 0x{:x})".format(*bob_public_key))

# Alice and Bob exchange their public keys and calculate the shared secret.
s1 = scalar_multiply(alice_private_key, bob_public_key)
s2 = scalar_multiply(bob_private_key, alice_public_key)
assert s1 == s2

print('Shared secret: (0x{:x}, 0x{:x})'.format(*s1))