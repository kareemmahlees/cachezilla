import time

import pytest  # pylint: disable=import-error

from cachezilla import CacheZilla


def test_set_increases_size(cachezilla_object: CacheZilla):
    cachezilla_object.set("first", "first")
    cachezilla_object.set("second", "second")
    cachezilla_object.set("third", "third")
    cachezilla_object.set("fourth", "fourth")

    assert cachezilla_object.size == 4


def test_set_adds_item_to_list(cachezilla_object: CacheZilla):
    result = cachezilla_object.set("name", "kareem")

    assert result == 1
    assert cachezilla_object.get("name") == "kareem"


def test_get_nonexisting_item_return_none(cachezilla_object: CacheZilla):
    assert cachezilla_object.get("foo") is None


def test_exceeding_maxsize_removes_items_all_none():
    cachezilla_object = CacheZilla(max_size=3)
    cachezilla_object.set("first", "first")
    cachezilla_object.set("second", "second")
    cachezilla_object.set("third", "third")
    cachezilla_object.set("fourth", "fourth")

    assert cachezilla_object.get("first") is None


@pytest.mark.parametrize(
    "a, b, c, expected",
    [
        ("third", "first", "second", "third"),
        ("second", "third", "first", "second"),
        ("first", "third", "second", "first"),
    ],
)
def test_exceeding_maxsize_removes_items_all_used(
    a, b, c, expected
):  # pylint: disable=invalid-name
    cachezilla_object = CacheZilla(max_size=3)
    cachezilla_object.set("first", "first")
    cachezilla_object.set("second", "second")
    cachezilla_object.set("third", "third")

    cachezilla_object.get(a)
    time.sleep(0.5)
    cachezilla_object.get(b)
    time.sleep(0.5)
    cachezilla_object.get(c)

    cachezilla_object.set("fourth", "fourth")

    assert cachezilla_object.get(expected) is None


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("first", "second", "third"),
        ("second", "third", "first"),
        ("first", "third", "second"),
    ],
)
def test_exceeding_maxsize_removes_items(
    a, b, expected
):  # pylint: disable=invalid-name
    cachezilla_object = CacheZilla(max_size=3)
    cachezilla_object.set("first", "first")
    cachezilla_object.set("second", "second")
    cachezilla_object.set("third", "third")

    cachezilla_object.get(a)
    cachezilla_object.get(b)
    cachezilla_object.set("fourth", "fourth")

    assert cachezilla_object.get(expected) is None


def test_tail_head_are_set_right(cachezilla_object: CacheZilla):
    cachezilla_object.set("first", "first")
    cachezilla_object.set("second", "second")
    cachezilla_object.set("third", "third")

    assert cachezilla_object.tail.value == "first"
    assert cachezilla_object.head.value == "third"
