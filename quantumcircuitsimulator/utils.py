import math

def log2(number):
    """Calculate the logarithm in base-2 for a given number.

    Args:
        number: the number whose logarithm we wish to find

    Returns:
        logarithm of given number to base 2

        For 256  it returns: 3
    """
    return math.frexp(number)[1] - 1
