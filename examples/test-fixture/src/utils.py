"""Utility functions with no type hints or docstrings."""


def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def deduplicate(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def safe_get(dictionary, key, default=None):
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return default


def format_name(first, last, middle=None):
    if middle:
        return f"{first} {middle} {last}"
    return f"{first} {last}"
