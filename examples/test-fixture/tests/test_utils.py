"""Tests for src/utils.py — covers all 5 utility functions."""

import pytest

from src.utils import chunk, deduplicate, flatten, format_name, safe_get


# --- flatten ---

def test_flatten_simple():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_flatten_deeply_nested():
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]


def test_flatten_already_flat():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_flatten_empty():
    assert flatten([]) == []


def test_flatten_single_item():
    assert flatten([[1]]) == [1]


def test_flatten_mixed_types():
    assert flatten([1, ["a", 2], [True]]) == [1, "a", 2, True]


# --- chunk ---

def test_chunk_even_split():
    assert list(chunk([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]


def test_chunk_uneven_split():
    assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_chunk_size_larger_than_list():
    assert list(chunk([1, 2], 10)) == [[1, 2]]


def test_chunk_single_elements():
    assert list(chunk([1, 2, 3], 1)) == [[1], [2], [3]]


def test_chunk_empty():
    assert list(chunk([], 3)) == []


def test_chunk_string():
    assert list(chunk("abcde", 2)) == ["ab", "cd", "e"]


def test_chunk_zero_size():
    with pytest.raises(ValueError, match="Chunk size must be a positive integer"):
        list(chunk([1, 2, 3], 0))


def test_chunk_negative_size():
    with pytest.raises(ValueError, match="Chunk size must be a positive integer"):
        list(chunk([1, 2, 3], -1))


# --- deduplicate ---

def test_deduplicate_basic():
    assert deduplicate([1, 2, 2, 3, 1]) == [1, 2, 3]


def test_deduplicate_no_dupes():
    assert deduplicate([1, 2, 3]) == [1, 2, 3]


def test_deduplicate_all_same():
    assert deduplicate([5, 5, 5]) == [5]


def test_deduplicate_empty():
    assert deduplicate([]) == []


def test_deduplicate_preserves_order():
    assert deduplicate([3, 1, 2, 1, 3]) == [3, 1, 2]


def test_deduplicate_strings():
    assert deduplicate(["a", "b", "a", "c"]) == ["a", "b", "c"]


# --- safe_get ---

def test_safe_get_existing_key():
    assert safe_get({"a": 1}, "a") == 1


def test_safe_get_missing_key():
    assert safe_get({"a": 1}, "b") is None


def test_safe_get_missing_key_with_default():
    assert safe_get({"a": 1}, "b", default=42) == 42


def test_safe_get_none_dict():
    assert safe_get(None, "a") is None


def test_safe_get_none_dict_with_default():
    assert safe_get(None, "a", default="fallback") == "fallback"


def test_safe_get_nested():
    d = {"outer": {"inner": 1}}
    assert safe_get(d, "outer") == {"inner": 1}


# --- format_name ---

def test_format_name_first_last():
    assert format_name("John", "Doe") == "John Doe"


def test_format_name_with_middle():
    assert format_name("John", "Doe", middle="Q") == "John Q Doe"


def test_format_name_middle_none():
    assert format_name("Jane", "Smith", middle=None) == "Jane Smith"


def test_format_name_empty_middle():
    # Empty string is falsy, so treated as no middle name
    assert format_name("Jane", "Smith", middle="") == "Jane Smith"


# --- edge cases ---

def test_deduplicate_with_none():
    assert deduplicate([None, 1, None, 2]) == [None, 1, 2]


def test_safe_get_empty_dict():
    assert safe_get({}, "a") is None


def test_format_name_unicode():
    assert format_name("José", "García") == "José García"


def test_flatten_empty_nested():
    assert flatten([[], [[]], []]) == []
