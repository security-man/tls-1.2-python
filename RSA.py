# This little script aims to provide a working, albeit highly-inefficient, implementation of TLS 1.2 for learning / demonstration purposes.
# Algorithm outline:
# 1) generate two primes, P and Q
# 2) generate PUBLIC key n, n=P*Q
# 3) generate psi(n), psi(n)=(P-1)*(Q-1)
# 4) generate exponent e, 1 < e < psi(n), e is an integer
# 5) generate PRIVATE key d, d=(k*psi(n) +1)/e, k is an integer
# 6) encrypted data = <character byte as int>^(e mod n)
# 7) decrypted data = <character byte(s) as int>^(d mod n)

# 1) Generate two primes, P and Q

# generate prime number that is greater than specified int input
def generate_prime(greater_than):
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
P = generate_prime(50)
print('')
print('Prime Q generation ...')
print('')
Q = generate_prime(60)
print('')

# 2) generate PUBLIC key n, n=P*Q

n=P*Q
print('PUBLIC key n = ' + str(P) + ' * ' + str(Q) + ' = ' + str(n))