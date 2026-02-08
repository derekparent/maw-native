"""Utility functions for common data transformations."""

from collections.abc import Generator, Hashable, Sequence
from typing import Any


def flatten(nested: list[Any]) -> list[Any]:
    """Recursively flatten a nested list structure into a single flat list.

    Args:
        nested: A list that may contain other lists at any depth.

    Returns:
        A flat list with all nested elements in order.
    """
    result: list[Any] = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(items: Sequence[Any], size: int) -> Generator[Sequence[Any], None, None]:
    """Split a sequence into fixed-size chunks.

    Args:
        items: The sequence to split.
        size: Maximum number of elements per chunk.

    Yields:
        Subsequences of up to `size` elements.

    Raises:
        ValueError: If size is not a positive integer.
    """
    if not isinstance(size, int) or size <= 0:
        raise ValueError("Chunk size must be a positive integer")
    for i in range(0, len(items), size):
        yield items[i:i + size]


def deduplicate(items: list[Hashable]) -> list[Hashable]:
    """Remove duplicate elements while preserving insertion order.

    Args:
        items: A list of hashable elements.

    Returns:
        A new list with duplicates removed, first occurrence kept.
    """
    seen: set[Hashable] = set()
    result: list[Hashable] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def safe_get(dictionary: dict[str, Any] | None, key: str, default: Any = None) -> Any:
    """Safely retrieve a value from a dictionary.

    Handles missing keys and None dictionaries without raising exceptions.

    Args:
        dictionary: The dictionary to look up (may be None).
        key: The key to retrieve.
        default: Value to return if key is missing or dictionary is None.

    Returns:
        The value for key, or default if not found.
    """
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return default


def format_name(first: str, last: str, middle: str | None = None) -> str:
    """Format a person's name as a single string.

    Args:
        first: First name.
        last: Last name.
        middle: Optional middle name or initial.

    Returns:
        Formatted full name string.
    """
    if middle:
        return f"{first} {middle} {last}"
    return f"{first} {last}"
