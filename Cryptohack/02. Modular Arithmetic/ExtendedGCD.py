# Extended Euclidian Algorithm writes a GCD between two numbers as a Linear Combination
# Linear Combination can be written as a * u + b * v = gcd(a,b)
# http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html
# https://captainmich.github.io/programming_language/CTF/Challenge/CryptoHack/general.html#math-extended-gcd

def extendedGCD(a, b):
    if(a == 0):
        return (0, 1)
    else:
        u, v = extendedGCD(b % a, a)
        return (v - (b // a) * u, u)

p = 26513
q = 32321

u, v = extendedGCD(p, q)
print(f'Flag: {u}') if u < v else print(f'Flag: {v}')