"""
* Key Resources: (code adapted from)
# https://stackoverflow.com/questions/8751653/how-to-convert-a-binary-string-into-a-float-value
# https://stackoverflow.com/questions/25099626/convert-scientific-notation-to-float
# https://stackoverflow.com/questions/30971079/how-to-convert-an-integer-to-a-list-of-bits
"""

from codecs import decode
import struct

def int_to_bin(num: int) -> str:
    """ Convert integer to binary string representation. """
    list_of_bits = [1 if num & (1 << (31-n)) else 0 for n in range(32)]
    string_version = ''.join([str(bit) for bit in list_of_bits])
    return string_version

def bin_to_float(byte_string: str) -> str:
    """ Convert binary string to a float. """
    float_bytes = int(byte_string, 2).to_bytes(4, 'big')  
    # see https://docs.python.org/3/library/struct.html for manipulation of params
    float_string =  format(struct.unpack('>f', float_bytes)[0], 'f')
    return float(float_string)

def int_to_float(num: int) -> float:
    bits = int_to_bin(num)
    return abs(bin_to_float(bits))

# Test example
num = 4140206672
print(f'For the output: {num}, we have the float: {int_to_float(num)}')
