"""Simple calculator module with an intentional division-by-zero bug."""


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    # BUG: No check for division by zero
    return a / b


def average(numbers: list[float]) -> float:
    # BUG: No check for empty list
    return sum(numbers) / len(numbers)
