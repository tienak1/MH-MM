import random

class Module:
    @staticmethod
    def Mulmod(x, y, n): #(x * y) % n
        x = x % n
        P = 0
        if y & 1 == 1:
             P = x
        y >>= 1
        while y > 0:
            x = (x << 1) % n
            if y & 1 == 1:
                P += x
                if P >= n:
                    P -= n
            y >>= 1
        return P

    @staticmethod
    def Powermod(x, p, n): #(x ^ p) % n
        y = 1
        if p == 0:
            return y
        A = x
        if p & 1 == 1:
            y = x
        p >>= 1
        while p > 0:
            A = Module.Mulmod(A, A, n)
            if p & 1 == 1:
                y = Module.Mulmod(A, y, n)
            p >>= 1
        return y

class Prime:
    @staticmethod
    def rm(n): # n - 1 = (2 ^ r) * m
        m = n - 1
        r = 0
        while m & 1 == 0:
            r += 1
            m >>= 1
        return r, m

    @staticmethod
    def PrimeTestF(n): # fermat nho
        b = random.choice([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])
        r, m = Prime.rm(n)
        for i in range(1, r):
            if Module.Powermod(b, m << i, n) != 1 and Module.Powermod(b, m << i, n) != n - 1:
                return False
        return True

    @staticmethod
    def miillerTest(d, n): # miller robbin

        a = random.randrange(2, n - 1)
        x = Module.Powermod(a, d, n)
        if x == 1  or x == n-1:
           return True

        while (d != n-1):
            x = Module.Mulmod(x, x, n)
            d <<= 1
            if x == 1:
                return False
            if x == n - 1:
                return True

        return False

    @staticmethod
    def isPrime(n, k): # kiem tra so nguyen to
        primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
        if n in primes:
            return True
        if n <= 1 or not(all(n % i != 0 for i in primes)):
            return False

        d = n - 1
        while d % 2 == 0:
            d >>= 1
        if not(Prime.PrimeTestF(n)):
            return False
            
        return True


def PrimeGen(x): # sinh so nguyen to
    while(1):
        n = 1
        for i in range(x):
            n <<= 1
            j = random.choice([0,1])
            n += j
        n = (n << 1) + 1 # sinh 1 so le
        if Prime.isPrime(n, 1): #kiem tra nguyen to
            return n


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def gcd_extends(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

class RSA:
    def __init__(self):
        pass

    def encrypt(self, m, E, N):
        c = []
        for i in m:
            elem = []
            for j in i:
                elem.append(Module.Powermod(j, E, N))
            c.append(elem)
        return c
    def decrypt(self,c, D, N):
        m = []
        for i in c:
            elem = []
            for j in i:
                elem.append(Module.Powermod(j, D, N))
            m.append(elem)
        return m

def CreateKey():
    P = PrimeGen(10)

    Q = PrimeGen(10)

    N = P*Q

    eulerTotient = (P - 1) * (Q - 1)

    E = PrimeGen(4)
    while gcd(E, eulerTotient) != 1:
        E = PrimeGen(4)

    D = gcd_extends(E, eulerTotient)
    return E, D, N


# i = RSA(E, D, N)

# m = [[0, 2, 3], [2, 3, 1], [7, 6, 2]]

# c = i.encrypt(m)
# print(c)

# m1 = i.decrypt(c)
# print(m1)
