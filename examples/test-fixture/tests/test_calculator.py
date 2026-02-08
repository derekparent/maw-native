"""Calculator tests — intentionally missing edge case coverage."""

from src.calculator import add, subtract, multiply, divide


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(3, 4) == 12


# Missing tests:
# - test_divide (happy path)
# - test_divide_by_zero (should raise or handle gracefully)
# - test_average (happy path)
# - test_average_empty_list (should raise or handle gracefully)
# - test_add_floats (precision)
# - test_multiply_by_zero
