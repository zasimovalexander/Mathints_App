"""
Use only as a dev helper.
"""


from random import randint as random__randint

from modules.calcs_math import primality


def prev_prime(n: int) -> int:
    """
    Return the largest prime <= N (2 for N < 3).
    """
    n = int(n)  # explicit coercion
    if n < 3:
        return 2
    if n % 2 == 0:
        n -= 1
    while n > 7:
        if primality(n):
            break
        n -= 2
    return n


def set_primes(
        pwr: int,
        qty: int =6
) -> list[int]:
    """
    Return a consecutive set of prime numbers < 10**P.
    """
    res = [prev_prime(10 ** pwr), ]
    for _ in range(qty - 1):
        res.append(prev_prime(res[-1] - 2))
    res.reverse()
    return res


def _test__prev_prime__boundary_values():
    for num in range(-1, 22):
        print(f"{num}:{prev_prime(num)}  ", end="")
    print()
    for num in set_primes(8, 10):
        lim = num + random__randint(1, 11)
        num = prev_prime(lim)
        print(f"{lim}:{num}  ", end="")


if __name__ == "__main__":
    _test__prev_prime__boundary_values()
