
import struct

S11 = 7
S12 = 12
S13 = 17
S14 = 22
S21 = 5
S22 = 9
S23 = 14
S24 = 20
S31 = 4
S32 = 11
S33 = 16
S34 = 23
S41 = 6
S42 = 10
S43 = 15
S44 = 21

PADDING = b"\x80" + b"\0" * 63

def F(x, y, z): return ((x & y) | (~x & z))
def G(x, y, z): return ((x & z) | (y & ~z))
def H(x, y, z): return (x ^ y ^ z)
def I(x, y, z): return (y ^ (x | ~z))

def ROTATE_LEFT(x, n):
    x &= 0xffffffff  
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def FF(a, b, c, d, x, s, ac):
    a = (a + F(b, c, d) + x + ac) & 0xffffffff
    a = ROTATE_LEFT(a, s)
    a = (a + b) & 0xffffffff
    return a

def GG(a, b, c, d, x, s, ac):
    a = (a + G(b, c, d) + x + ac) & 0xffffffff
    a = ROTATE_LEFT(a, s)
    a = (a + b) & 0xffffffff
    return a

def HH(a, b, c, d, x, s, ac):
    a = (a + H(b, c, d) + x + ac) & 0xffffffff
    a = ROTATE_LEFT(a, s)
    a = (a + b) & 0xffffffff
    return a

def II(a, b, c, d, x, s, ac):
    a = (a + I(b, c, d) + x + ac) & 0xffffffff
    a = ROTATE_LEFT(a, s)
    a = (a + b) & 0xffffffff
    return a

class md5(object):
    digest_size = 16
    block_size = 64

    def __init__(self, string=b"", state=None, count=0):
        self.count = 0
        self.buffer = b""

        if state is None:
            self.state = (
                0x67452301,
                0xefcdab89,
                0x98badcfe,
                0x10325476,
            )
        else:
            self.state = _decode(state, md5.digest_size)

        if count is not None:
            self.count = count
        if string:
            self.update(string)

    def update(self, input_bytes):
        inputLen = len(input_bytes)
        index = (self.count >> 3) & 0x3F
        self.count += (inputLen << 3)
        partLen = md5.block_size - index

        if inputLen >= partLen:
            self.buffer = self.buffer[:index] + input_bytes[:partLen]
            self.state = hash(self.state, self.buffer)
            i = partLen
            while i + 63 < inputLen:
                self.state = hash(self.state, input_bytes[i:i + md5.block_size])
                i += md5.block_size
            index = 0
        else:
            i = 0

        self.buffer = self.buffer[:index] + input_bytes[i:inputLen]

    def digest(self):
        _buffer, _count, _state = self.buffer, self.count, self.state
        self.update(padding(self.count))
        result = self.state
        self.buffer, self.count, self.state = _buffer, _count, _state
        return _encode(result, md5.digest_size)

    def hexdigest(self):
        return self.digest().hex()


def padding(msg_bits):
    index = (msg_bits >> 3) & 0x3f
    if index < 56:
        padLen = (56 - index)
    else:
        padLen = (120 - index)

    return PADDING[:padLen] + _encode(((msg_bits & 0xffffffff), msg_bits >> 32), 8)


def hash(msg):
    state = (0x67452301,
             0xefcdab89,
             0x98badcfe,
             0x10325476,)
    a, b, c, d = state
    block = msg + padding(len(msg) * 8)
    x = _decode(block, 64)

    a = FF (a, b, c, d, x[ 0], S11, 0xd76aa478)  
    d = FF (d, a, b, c, x[ 1], S12, 0xe8c7b756)  
    c = FF (c, d, a, b, x[ 2], S13, 0x242070db)  
    b = FF (b, c, d, a, x[ 3], S14, 0xc1bdceee)  
    a = FF (a, b, c, d, x[ 4], S11, 0xf57c0faf)  
    d = FF (d, a, b, c, x[ 5], S12, 0x4787c62a)  
    c = FF (c, d, a, b, x[ 6], S13, 0xa8304613)  
    b = FF (b, c, d, a, x[ 7], S14, 0xfd469501)  
    a = FF (a, b, c, d, x[ 8], S11, 0x698098d8)  
    d = FF (d, a, b, c, x[ 9], S12, 0x8b44f7af)  
    c = FF (c, d, a, b, x[10], S13, 0xffff5bb1)  
    b = FF (b, c, d, a, x[11], S14, 0x895cd7be)  
    a = FF (a, b, c, d, x[12], S11, 0x6b901122)  
    d = FF (d, a, b, c, x[13], S12, 0xfd987193)  
    c = FF (c, d, a, b, x[14], S13, 0xa679438e)  
    b = FF (b, c, d, a, x[15], S14, 0x49b40821)  
    d = GG (d, a, b, c, x[ 6], S22, 0xc040b340)  
    c = GG (c, d, a, b, x[11], S23, 0x265e5a51)  
    a = GG (a, b, c, d, x[ 5], S21, 0xd62f105d)  
    d = GG (d, a, b, c, x[10], S22,  0x2441453)  
    c = GG (c, d, a, b, x[15], S23, 0xd8a1e681)  
    b = GG (b, c, d, a, x[ 4], S24, 0xe7d3fbc8)  
    a = GG (a, b, c, d, x[ 9], S21, 0x21e1cde6)  
    d = GG (d, a, b, c, x[14], S22, 0xc33707d6)  
    b = GG (b, c, d, a, x[ 8], S24, 0x455a14ed)  
    a = GG (a, b, c, d, x[13], S21, 0xa9e3e905)  
    c = GG (c, d, a, b, x[ 7], S23, 0x676f02d9)  
    b = GG (b, c, d, a, x[12], S24, 0x8d2a4c8a)  
    a = HH (a, b, c, d, x[ 5], S31, 0xfffa3942)  
    d = HH (d, a, b, c, x[ 8], S32, 0x8771f681)  
    c = HH (c, d, a, b, x[11], S33, 0x6d9d6122)  
    b = HH (b, c, d, a, x[14], S34, 0xfde5380c)  
    d = HH (d, a, b, c, x[ 4], S32, 0x4bdecfa9)  
    c = HH (c, d, a, b, x[ 7], S33, 0xf6bb4b60)  
    b = HH (b, c, d, a, x[10], S34, 0xbebfbc70)  
    a = HH (a, b, c, d, x[13], S31, 0x289b7ec6)  
    b = HH (b, c, d, a, x[ 6], S34,  0x4881d05)  
    a = HH (a, b, c, d, x[ 9], S31, 0xd9d4d039)  
    d = HH (d, a, b, c, x[12], S32, 0xe6db99e5) 
    c = HH (c, d, a, b, x[15], S33, 0x1fa27cf8) 
    d = II (d, a, b, c, x[ 7], S42, 0x432aff97) 
    c = II (c, d, a, b, x[14], S43, 0xab9423a7) 
    b = II (b, c, d, a, x[ 5], S44, 0xfc93a039) 
    a = II (a, b, c, d, x[12], S41, 0x655b59c3) 
    c = II (c, d, a, b, x[10], S43, 0xffeff47d) 
    a = II (a, b, c, d, x[ 8], S41, 0x6fa87e4f) 
    d = II (d, a, b, c, x[15], S42, 0xfe2ce6e0) 
    c = II (c, d, a, b, x[ 6], S43, 0xa3014314) 
    b = II (b, c, d, a, x[13], S44, 0x4e0811a1) 
    a = II (a, b, c, d, x[ 4], S41, 0xf7537e82) 
    d = II (d, a, b, c, x[11], S42, 0xbd3af235) 
    b = II (b, c, d, a, x[ 9], S44, 0xeb86d391) 

    state = (0xffffffff & (state[0] + a),
             0xffffffff & (state[1] + b),
             0xffffffff & (state[2] + c),
             0xffffffff & (state[3] + d),)
    return _encode(state, 16)

def _encode(input_tuple, length):
    k = length >> 2
    return struct.pack("%iI" % k, *input_tuple[:k])


def _decode(input_bytes, length):
    k = length >> 2
    return list(struct.unpack("%iI" % k, input_bytes[:length]))