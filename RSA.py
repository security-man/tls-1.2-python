# This little script aims to provide a working, albeit highly-inefficient, implementation of TLS 1.2 for learning / demonstration purposes.
# Algorithm outline:
# 1) generate two primes, P and Q
# 2) generate n, n=P*Q
# 3) generate totient psi(n), psi(n)=(P-1)*(Q-1)
# 4) generate exponent e, 1 < e < psi(n), e is an integer and coprime to psi(n)
# 5) generate d, d=(k*psi(n) +1)/e, k is an integer
# 6) C= P^(e) mod n
# 7) P = C^(d) mod n
# PUBLIC key = (n,e), PRIVATE key = (n,d)

import math

# 1) Generate two primes, P and Q

# generate prime number that is greater than specified int input
def prime(greater_than):
    prime = greater_than
    i = 2
    while i < prime:
        print(str(prime) + ' mod ' + str(i) + ' = ' + str(prime % i))
        if prime % i == 0:
            print(str(prime) + " is not prime, divisible by " + str(i))
            prime = prime + 1
            i = 2
        else:
            i = i + 1
    print(str(prime) + " is prime!")
    return prime

print('Prime P generation ...')
print('')
P = prime(3)
print('')
print('Prime Q generation ...')
print('')
Q = prime(11)


# 2) generate PUBLIC key n, n=P*Q

print('')
n=P*Q
print('PUBLIC key n = ' + str(P) + ' * ' + str(Q) + ' = ' + str(n))

# 3) generate psi(n) = (P-1)*(Q-1)

print('')
psi=(P-1)*(Q-1)
print('psi(n) = ' + str(psi))

# 4) generate e, 1 < e < psi(n), e is an integer and coprime to psi(n)

def coprime(value):
    coprime = 3
    i = 3
    print('Coprime e generation ...')
    while coprime < value:
        if coprime % i != 0 or value % i != 0:
            print(str(coprime) + ' mod ' + str(i) + ' = ' + str(coprime % i) + ', ' + str(value) + ' mod ' + str(i) + ' = ' + str(value % i))
            i = i + 1
            if i > coprime:
                i = 3
                coprime = coprime + 1
        else :
            print(str(coprime) + ' and ' + str(value) + ' are coprime, common factor = ' + str(i))
            break
    return coprime

print('')
e = coprime(psi)

e = 7

# 5) generate d, (d*e) mod psi = 1, d is integer (iterate until d satisfies equation)

def privatekey(psi,e):
    d = 1
    k = ((e*d) % psi)
    while k != 1:
        d = d + 1
        k = ((e*d) % psi)
    return d

print('psi = ' + str(psi) + ' e = ' + str(e))

d = privatekey(psi,e)

print('')
print('d = ' + str(d))

# 6) C= P^(e) mod n
# 7) P = C^(d) mod n
# PUBLIC key = (n,e), PRIVATE key = (n,d)