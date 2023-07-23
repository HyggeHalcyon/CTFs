# a = bq + remain, with some number q
def gcd(a,b):
    if( b > a):
        a,b = b,a

    r = a % b

    if( r != 0):
        commondivisor = gcd(b,r)
    elif( r == 0):
        commondivisor = b

    return commondivisor

a = 12
b = 8
print( gcd(a,b) )

a = 66528
b = 52920
print("Flag: " + str(gcd(a,b)) )