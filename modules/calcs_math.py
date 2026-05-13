"""
Common functions for math calculations.
"""


from random import randint as random__randint


def gen_rand(
        power: int,
        delta_max: int =1
) -> int:
    """
    Generate a random integer with the given digit length.

    Args:
        power: Number of digits.
        delta_max: Range modifier that reduces the upper bound.
    """
    return random__randint(10 ** (power - 1), 10 ** power - delta_max)


def primality(n: int) -> bool:
    """
    Check a number for a primality.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def div_detailed(number: int) -> tuple[list[tuple[int, int]], dict[int, int]]:
    """
    Factor a number into prime factors while keeping track of division steps.

    Notes:
        Produce a list of (dividend, divisor) pairs for each prime factorization step, and record prime divisors with
        multiplicity in a separate rank map.
    """
    pairs = []
    ranks = {}
    while number % 2 == 0:
        pairs.append((number, 2))
        number //= 2
        ranks[2] = ranks.get(2, 0) + 1
    prm = 3
    while prm * prm <= number:
        while number % prm == 0:
            pairs.append((number, prm))
            number //= prm
            ranks[prm] = ranks.get(prm, 0) + 1
        prm += 2
    if number > 1:
        pairs.append((number, number))
        ranks[number] = 1
    pairs.append((1, 1))
    return pairs, ranks


def gcd_or_lcm(
        suites_factors: list[dict[int, int]],
        clue: str
) -> tuple[dict[int, int], int]:
    """
    Select the relevant prime factors and compute the Greatest Common Divisor or the Least Common Multiple.

    Notes:
        Additionally, return a separate rank map based on the computed math function.
    """
    branching = {
        "GCD": (set.intersection, min, lambda d, k: d[k]),
        "LCM": (set.union, max, lambda d, k: d.get(k, 0))
    }
    func_set, func_pick, func_val = branching[clue]
    picked = {}
    for ftr in func_set(*(set(suite.keys()) for suite in suites_factors)):
        picked[ftr] = func_pick(func_val(suite, ftr) for suite in suites_factors)
    value = 1
    for p, r in picked.items():
        value *= p ** r
    return picked, value
