from modules import calcs_math

import pytest


def test__gen_rand__type():
    num = calcs_math.gen_rand(1)
    assert isinstance(num, int)
    assert num > 0

def test__gen_rand__length():
    pwr = 8
    assert len(str(calcs_math.gen_rand(pwr))) == pwr

@pytest.mark.parametrize("delta, max_expect", [(2, 8), (7, 3)])
def test__gen_rand__clipped_1d_num(delta, max_expect):
    assert 1 <= calcs_math.gen_rand(1, delta) <= max_expect

def test__gen_rand__not_same_num():
    nums = {calcs_math.gen_rand(1) for _ in range(10)}
    assert len(nums) > 1

def test__gen_rand__stable_type_and_length():
    pwr = 5
    for _ in range(10):
        num = calcs_math.gen_rand(pwr)
        assert isinstance(num, int)
        assert len(str(num)) == pwr


def test__primality__type():
    prime = calcs_math.primality(9)
    assert isinstance(prime, bool)

def test__primality__is_prime():
    assert calcs_math.primality(11)

def test__primality__not_prime():
    assert not calcs_math.primality(998)

def test__primality__num_1():
    assert not calcs_math.primality(1)

@pytest.mark.parametrize("num", [2, 3, 5, 7])
def test__primality__prime_1d_num(num):
    assert calcs_math.primality(num)

@pytest.mark.parametrize("num", [99999931, 99999941, 99999959, 99999971, 99999989])
def test__primality__prime_8d_num(num):
    assert calcs_math.primality(num)

@pytest.mark.parametrize("num", [4, 10, 100, 10000, 99999998])
def test__primality__even_num(num):
    assert not calcs_math.primality(num)
