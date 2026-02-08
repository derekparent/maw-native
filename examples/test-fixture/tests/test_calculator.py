"""Calculator tests — full coverage including edge cases."""

import math

import pytest

from src.calculator import add, average, divide, multiply, subtract


# --- add ---

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_add_floats():
    result = add(0.1, 0.2)
    assert abs(result - 0.3) < 1e-9


def test_add_type_error():
    with pytest.raises(TypeError, match="Arguments must be numbers"):
        add("a", "b")


# --- subtract ---

def test_subtract():
    assert subtract(5, 3) == 2


def test_subtract_type_error():
    with pytest.raises(TypeError, match="Arguments must be numbers"):
        subtract(None, 1)


# --- multiply ---

def test_multiply():
    assert multiply(3, 4) == 12


def test_multiply_by_zero():
    assert multiply(100, 0) == 0
    assert multiply(0, 100) == 0


def test_multiply_type_error():
    with pytest.raises(TypeError, match="Arguments must be numbers"):
        multiply([1], 2)


# --- divide ---

def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5
    assert divide(-6, 3) == -2.0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)


# --- average ---

def test_average():
    assert average([1, 2, 3]) == 2.0
    assert average([10]) == 10.0
    assert average([1.5, 2.5]) == 2.0


def test_average_empty_list():
    with pytest.raises(ValueError, match="Cannot compute average of empty list"):
        average([])


# --- edge cases ---

def test_add_infinity():
    assert add(float('inf'), 1) == float('inf')


def test_subtract_infinity():
    result = subtract(float('inf'), float('inf'))
    assert math.isnan(result)


def test_multiply_infinity():
    result = multiply(float('inf'), 0)
    assert math.isnan(result)


def test_divide_large_numbers():
    assert divide(1e308, 0.1) == float('inf')


def test_average_single_negative():
    assert average([-5]) == -5.0


def test_average_mixed_signs():
    assert average([-10, 10]) == 0.0
