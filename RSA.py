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

# generate prime number that is greater than specified int input
def prime(greater_than):
    prime = greater_than
    i = 2
    while i < prime:
        if prime % i == 0:
            prime = prime + 1
            i = 2
        else:
            i = i + 1
    return prime

# generate list of values that are coprime to input value
def coprime(value):
    coprime = 2
    coprime_list = []
    i = 2
    while coprime < value:
        for i in range(i,coprime-1):
            if coprime % i == 0 and value % i == 0:
                i = 2
                coprime = coprime + 1
        if value % coprime != 0:
            coprime_list.append(coprime)
        i = 2
        coprime = coprime + 1
    return coprime_list

# generate private key based on minimum values for P and Q, initial primes, using coprime function
def keygeneration(a,b):
    P = prime(a)
    Q = prime(b)
    n = P*Q
    psi = (P-1)*(Q-1)
    coprimelist = coprime(psi)
    coprimecounter = 1
    d = 0
    e = 0
    while coprimecounter < len(coprimelist):
        e = coprimelist[coprimecounter]
        for k in range(10):
            if (((k*psi)+1) % e) == 0:
                d = (int) (((k*psi)+1)/e)
                print('P = ' + str(P) + ', Q = ' + str(Q) + ', n = ' + str(n) + ', Psi = ' + str(psi) + ', e = ' + str(e) + ', d = ' + str(d))
                coprimecounter = len(coprimelist)
                break
        coprimecounter = coprimecounter + 1
    return P,Q,n,psi,e,d

P,Q,n,psi,e,d = keygeneration(32,43)