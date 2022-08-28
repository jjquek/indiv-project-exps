from random import Random
import random as r
from math import ldexp

# this code in this file is ADAPTED from the following source:

"""
* Author(s) name : Python Software Foundation
* Date Accessed: 22 August 2022
* Title : 'Recipes' in "random-Generate pseudo-random numbers"
* Code Version: as in https://github.com/python/cpython/blob/3.10/Lib/random.py
* Type: source code
* Web address: https://docs.python.org/3/library/random.html

To quote from the documentation, using an instance of the FullRandom class,

"The mantissa comes from a uniform distribution of integers in the range 2⁵² ≤ mantissa < 2⁵³. The exponent comes from a geometric distribution where exponents smaller than -53 occur half as often as the next larger exponent"

We adapt the code to generate randoms where the mantissa comes from the same uniform distribution as stated in the quote, but modify the geoemtric distribution the exponents come from to be significantly less so we raise the chances of a large D value.

The code forms the bulk of the `random` method defined below. 

"""

manitssa_bit_size = 52 # value in documentation example: 52
exponent_size = [i for i in range(-40, -25)] # value in documentation example: -53. We set it for initial runs to -35.
                                            # Selecting randomly from this range varies the generated D values more greatly.

# -35 exponent_size works. Generates randoms in the vicinity of 100000s

class SharedPRNG(Random):

    def __init__(self, shared_seed: int) -> None:
        super().__init__()
        self.seed_PRNG(shared_seed)
        self.seed_internal_PRNG(shared_seed)
    
    def seed_PRNG(self, shared_seed) -> None:
        self.seed(shared_seed)
    
    def seed_internal_PRNG(self, shared_seed) -> None:
        self.internal_PRNG = r.seed(shared_seed)

    def random(self):
        mantissa = 0x10_0000_0000_0000 | self.getrandbits(manitssa_bit_size)
        exponent = r.choice(exponent_size)
        x = 0
        while not x:
            x = self.getrandbits(32)
            exponent += x.bit_length() - 32
        return ldexp(mantissa, exponent)
        
