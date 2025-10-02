import time
import secrets
class Random:
    TYPE_0 = 0
    BREAK_0 = 8
    DEG_0 = 0
    SEP_0 = 0

    TYPE_1 = 1
    BREAK_1 = 32
    DEG_1 = 7
    SEP_1 = 3

    TYPE_2 = 2
    BREAK_2 = 64
    DEG_2 = 15
    SEP_2 = 1

    TYPE_3 = 3
    BREAK_3 = 128
    DEG_3 = 31
    SEP_3 = 3

    TYPE_4 = 4
    BREAK_4 = 256
    DEG_4 = 63
    SEP_4 = 1

    MAX_TYPES = 5

    _degrees = [DEG_0, DEG_1, DEG_2, DEG_3, DEG_4]
    _seps = [SEP_0, SEP_1, SEP_2, SEP_3, SEP_4]

    def __init__(self, seed=None):
        self.initstate(128, seed)

    def initstate(self, n_bytes, seed):
        if n_bytes < self.BREAK_0:
            raise ValueError("State size must be at least 8 bytes.")

        if n_bytes < self.BREAK_1:
            self._rand_type = self.TYPE_0
        elif n_bytes < self.BREAK_2:
            self._rand_type = self.TYPE_1
        elif n_bytes < self.BREAK_3:
            self._rand_type = self.TYPE_2
        elif n_bytes < self.BREAK_4:
            self._rand_type = self.TYPE_3
        else:
            self._rand_type = self.TYPE_4

        self._rand_deg = self._degrees[self._rand_type]
        self._rand_sep = self._seps[self._rand_type]

        state_size = 1 if self._rand_type == self.TYPE_0 else self._rand_deg
        self._state = [0] * state_size

        self._fptr = 0
        self._rptr = 0

        self.seed(seed)

    def seed(self, a=None):
        if a is None:
            a = secrets.randbits(1024)
        
        self._state[0] = a

        if self._rand_type == self.TYPE_3:
            return

        modulus = 2147483647
        multiplier = 16807

        for i in range(1, self._rand_deg):
            hi = self._state[i-1] // 127773
            lo = self._state[i-1] % 127773
            test = multiplier * lo - 2836 * hi
            self._state[i] = test + (test < 0) * modulus

        self._fptr = self._rand_sep
        self._rptr = 0

        for _ in range(10 * self._rand_deg):
            self._get_random_int()

    def _get_random_int(self):
        if self._rand_type == self.TYPE_3:
            self._state[0] = ((self._state[0] * 132047653857099716108)+961808399608617582016) % 4079919672758639624917
            return self._state[0]
        
        val = (self._state[self._fptr] + self._state[self._rptr]) & 0xFFFFFFFF
        self._state[self._fptr] = val

        result = (val >> 1) & 0x7FFFFFFF

        self._fptr = (self._fptr + 1) % self._rand_deg
        self._rptr = (self._rptr + 1) % self._rand_deg

        return result

    def random(self):
        return self._get_random_int() / 2147483647.0

    def getstate(self):
        if self._rand_type == self.TYPE_3:
            return (self._rand_type, tuple(self._state), None, None)
        else:
            return (self._rand_type, tuple(self._state), self._rptr, self._fptr)

    def setstate(self, state):
        rand_type, state_tuple, rptr, fptr = state

        if rand_type < self.TYPE_0 or rand_type >= self.MAX_TYPES:
            raise ValueError("Invalid state object")

        self._rand_type = rand_type
        self._rand_deg = self._degrees[rand_type]
        self._rand_sep = self._seps[rand_type]
        self._state = list(state_tuple)
        self._rptr = rptr
        self._fptr = fptr

    def __int__(self):
        return self._get_random_int()

    def __index__(self):
        return int(self)

    def __mod__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return int(self) % other

    def __rmod__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return other % int(self)
    
    def randint(self, n):
        if n <= 0:
            raise ValueError("n must be positive")
        return self._get_random_int() % n