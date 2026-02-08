"""Simple calculator module with safe division and averaging."""


def _validate_numeric(a: float, b: float) -> None:
    """Validate that both arguments are numeric types.

    Args:
        a: First argument to validate.
        b: Second argument to validate.

    Raises:
        TypeError: If either argument is not a number.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")


def add(a: float, b: float) -> float:
    _validate_numeric(a, b)
    return a + b


def subtract(a: float, b: float) -> float:
    _validate_numeric(a, b)
    return a - b


def multiply(a: float, b: float) -> float:
    _validate_numeric(a, b)
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def average(numbers: list[float]) -> float:
    """Compute the arithmetic mean of a list of numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot compute average of empty list")
    return sum(numbers) / len(numbers)
