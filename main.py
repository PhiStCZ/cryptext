#!/usr/bin/env python3

''' Just a scratchpad for ideas & stuff. '''

from cryptext.cicada import liberprimus as lp, gematriaprimus as gp, futhorc
from cryptext.dmath import mul_inverse
from cryptext import ciphers
from cryptext.alphabet import latin
from cryptext.ciphers import vigenere, multi_vigenere, autokey, caesar, atbash
from cryptext.analytics import *
from cryptext.dmath import is_prime
import matplotlib.pyplot as plt

print(gp.decode(lp.load_before_unsolved_decrypted().content()))

# TODO: create a function for also enumerating the repeated ngrams and their distance (use some other class?)
