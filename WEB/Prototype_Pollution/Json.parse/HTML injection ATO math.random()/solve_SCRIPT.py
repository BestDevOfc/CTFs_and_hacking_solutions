import os, struct
from z3 import *
from decimal import Decimal

# set_option("verbose", 10)
set_option("parallel.enable", True)
set_option("parallel.threads.max", os.cpu_count() - 2)

# https://github.com/d0nutptr/v8_rand_buster/blob/master/xs128p.py
def to_double(value):
    """
    https://github.com/v8/v8/blob/master/src/base/utils/random-number-generator.h#L111
    """
    double_bits = (value >> 12) | 0x3FF0000000000000
    return struct.unpack('d', struct.pack('<Q', double_bits))[0] - 1

# https://github.com/d0nutptr/v8_rand_buster/blob/master/xs128p.py
def from_double(dbl):
    """
    https://github.com/v8/v8/blob/master/src/base/utils/random-number-generator.h#L111

    This function acts as the inverse to @to_double. The main difference is that we
    use 0x7fffffffffffffff as our mask as this ensures the result _must_ be not-negative
    but makes no other assumptions about the underlying value.

    That being said, it should be safe to change the flag to 0x3ff...
    """
    return struct.unpack('<Q', struct.pack('d', dbl + 1))[0] & 0x7FFFFFFFFFFFFFFF

def reverse17(val):
    return val ^ (val >> 17) ^ (val >> 34) ^ (val >> 51)

def reverse23(val):
    return (val ^ (val << 23) ^ (val << 46)) & 0xFFFFFFFFFFFFFFFF

class XorShift128PlusSolver:
    def __init__(self):
        self.s0 = BitVec('s0', 64)
        self.s1 = BitVec('s1', 64)
        self.solver = SolverFor("QF_BV")
        
        self._store = [self.s0, self.s1]
    
    # https://github.com/v8/v8/blob/79f76b5e82defaab5cd3ab7e2dcdbdb87f8bc310/src/base/utils/random-number-generator.h#L119
    @staticmethod
    def get_next_state(state_s0, state_s1):
        o = state_s0
        
        s1 = state_s0
        s0 = state_s1
        
        state_s0 = s0
        
        s1 ^= (s1 << 23) & 0xFFFFFFFFFFFFFFFF
        s1 ^= (s1 >> 17) & 0xFFFFFFFFFFFFFFFF
        s1 ^= (s0      ) & 0xFFFFFFFFFFFFFFFF
        s1 ^= (s0 >> 26) & 0xFFFFFFFFFFFFFFFF
        
        state_s1 = s1
        
        return state_s0, state_s1, to_double(o)
    
    # https://github.com/TACIXAT/XorShift128Plus/blob/29ce8b02ca36b799e11c1a674613072edafa859a/xs128p.py#L57
    @staticmethod
    def get_prev_state(state_s0, state_s1):
        
        prev_s1 = state_s0
        prev_s0 = state_s1 ^ (state_s0 >> 26)
        prev_s0 = prev_s0 ^ state_s0
        prev_s0 = reverse17(prev_s0)
        prev_s0 = reverse23(prev_s0)
        
        return prev_s0, prev_s1, to_double(prev_s0)

    # https://github.com/v8/v8/blob/79f76b5e82defaab5cd3ab7e2dcdbdb87f8bc310/src/base/utils/random-number-generator.h#L119
    # https://github.com/d0nutptr/v8_rand_buster/blob/master/xs128p.py
    @staticmethod
    def sym_xorshiftplus(s0, s1):
        # swap s0 and s1
        sym_s1, sym_s0 = s0, s1
        
        sym_s1 ^= sym_s1 << 23
        sym_s1 ^= LShR(sym_s1, 17)
        sym_s1 ^= sym_s0
        sym_s1 ^= LShR(sym_s0, 26)
        
        return s1, sym_s1

    def _sym_next_state(self):
        self.s0, self.s1 = XorShift128PlusSolver.sym_xorshiftplus(self.s0, self.s1)

    def _sym_next_state_floor(self, expected, multiple):
        self._sym_next_state()
        
        # https://github.com/d0nutptr/v8_rand_buster/blob/fc2903989788a925dbfad98b43b3e824255a0894/xs128p.py#L47
        # Fancy double to -> int and take known bits from floor
        calc = LShR(self.s0, 12)
        
        lower = from_double(Decimal(expected) / Decimal(multiple))
        upper = from_double((Decimal(expected) + 1) / Decimal(multiple))

        lower_mantissa = (lower & 0x000FFFFFFFFFFFFF)
        upper_mantissa = (upper & 0x000FFFFFFFFFFFFF)
        upper_expr     = (upper >> 52) & 0x7FF

        self.solver.add(
            And(
                lower_mantissa <= calc, 
                Or(
                    upper_mantissa >= calc,
                    upper_expr == 1024
                )
            )
        )
    
    def get_solved_state(self):
        if self.solver.check() == sat:
            m = self.solver.model()

            s0 = m[self._store[0]].as_long()
            s1 = m[self._store[1]].as_long()

            return s0, s1
        else:
            return None

if __name__ == "__main__":
    x = XorShift128PlusSolver()
    
    modulo = 0xffff
    
    nums = 'efefbf58c2e7e1f3f23d17b2c0a24098e0d9d58d75634a7bb2fbd4f667c7bbb2dcdafc4fc018b6ffe9bccf94c3fb99e34b40a12469c07ecd42801fd7ff7e312bcf7b315a9d6e40cf14bdb32334fbafcd391ee3755420155c04d389afcc03221e69fcfed643c0d1ebfa758adb8f91cf6290412d0813a8396c7730f341331e2782'
    
    # split every 2 characters
    nums = [nums[i:i+4] for i in range(0, len(nums), 4)]
    nums = [int(i, 16) for i in nums]
    
    print(nums)

    # for every chunk of 64 characters, reverse it
    nums = [nums[i:i+64] for i in range(0, len(nums), 64)]
    nums = [nums[i][::-1] for i in range(len(nums))]
    nums = [item for sublist in nums for item in sublist]
    
    print(nums)
    
    x._sym_next_state()
    for n in nums:
        x._sym_next_state_floor(n, modulo)
    
    if x.solver.check() == sat:
        m = x.solver.model()
        s0, s1 = x.get_solved_state()
        
        print(f"0x{s0:016x}, 0x{s1:016x}, {s0 % modulo}")

        for i in range(3):
            s0, s1, o = XorShift128PlusSolver.get_next_state(s0, s1)
            print(f"0x{s0:016x}, 0x{s1:016x}, {math.floor(o * modulo)}")
        
        print('hashes going forward:')
        for _ in range(10):
            buff = []
            for i in range(64):
                n_next = hex(math.floor(o * modulo))[2:].rjust(4, '0')
                buff.append(n_next)
                s0, s1, o = XorShift128PlusSolver.get_next_state(s0, s1)
                # print(f"0x{s0:016x}, 0x{s1:016x}, {math.floor(o * modulo)}")

            print(''.join(buff[::-1]))
        
    else:
        print("unsat")