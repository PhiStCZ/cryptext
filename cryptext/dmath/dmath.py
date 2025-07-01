import math


def is_prime(n: int) -> bool:
    ''' Tests whether a given positive integer is prime. '''
    if n < 2: return False
    if n % 2 == 0: return n == 2
    if n % 3 == 0: return n == 3

    limit = int(math.sqrt(n))
    for i in range(5, limit + 1, 6):
        if n % i == 0: return False
        if n % (i + 2) == 0: return False

    return True

def primes(excl_upper_limit: int) -> list[int]:
    ''' Generates a list of primes, up to a given upper limit. '''
    if excl_upper_limit <= 2: return []
    output = [2]

    # places cover a range(3, excl_upper_limit, 2)
    # len = math.upper((excl_upper_limit - 3) / 2)
    # the roundup is only needed when upper limit is even,
    # so just add 1 to the excl_upper_limit and it works with int div
    places = [True] * ((excl_upper_limit - 2) // 2)
    for i in range(len(places)):
        if not places[i]: continue
        n = i * 2 + 3
        output.append(n)
        for nn in range(n*n, excl_upper_limit, 2*n):
            places[(nn - 3) // 2] = False

    return output

def mul_inverse(a: int, b: int) -> int:
    ''' Calculates and returns the multiplicative inverse of a number *a* given a base *b*. '''
    a = a % b
    for c in range(1, b):
        if (a * c) % b == 1: return c
    raise Exception('Multiplicative inverse cannot be found')
