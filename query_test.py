import pytest
from query import run_query


def test_select_w_limit_extra_items():
    data = [
        {"title": "a", "genres": "cartoon"},
        {"title": "b", "genres": "cartoon"},
        {"title": "c", "genres": "cartoon"},
    ]
    query = [
        ["SCAN", ["movies"]],
        ["LIMIT", [2]],
    ]

    returned_items = run_query(query, data)

    assert returned_items == [
        {"title": "a", "genres": "cartoon"},
        {"title": "b", "genres": "cartoon"},
    ]


def test_select_w_limit_less_items():
    data = [
        {"title": "a", "genres": "cartoon"},
    ]
    query = [
        ["SCAN", ["movies"]],
        ["LIMIT", [2]],
    ]

    returned_items = run_query(query, data)

    assert returned_items == [
        {"title": "a", "genres": "cartoon"},
    ]


def test_select_w_filter():
    data = [
        {"title": "a", "ratings": 5},
        {"title": "c", "ratings": 1},
        {"title": "b", "ratings": 2},
    ]
    query = [
        ["SCAN", ["movies"]],
        ["FILTER", ["ratings", "GT", "1"]],
    ]

    returned_items = run_query(query, data)

    assert returned_items == [
        {"title": "a", "ratings": 5},
        {"title": "b", "ratings": 2},
    ]


def test_select_w_filter_w_limit():
    data = [
        {"title": "a", "ratings": 5},
        {"title": "c", "ratings": 1},
        {"title": "b", "ratings": 2},
    ]
    query = [["SCAN", ["movies"]], ["FILTER", ["ratings", "GT", "1"]], ["LIMIT", [1]]]

    returned_items = run_query(query, data)

    assert returned_items == [
        {"title": "a", "ratings": 5},
    ]


def test_projection():
    data = [
        {"title": "a", "ratings": 5},
        {"title": "c", "ratings": 1},
        {"title": "b", "ratings": 2},
    ]
    query = [
        ["SCAN", ["movies"]],
        ["FILTER", ["ratings", "GT", "1"]],
        ["PROJECTION", ["title"]],
    ]

    returned_items = run_query(query, data)

    assert returned_items == [
        {"title": "a"},
        {"title": "b"},
    ]


def test_projection_w_float():
    data = [
        {"title": "a", "ratings": 5},
        {"title": "c", "ratings": 1},
        {"title": "b", "ratings": 2.5},
    ]
    query = [
        ["SCAN", ["movies"]],
        ["FILTER", ["ratings", "GT", "1.4"]],
        ["PROJECTION", ["title"]],
    ]

    returned_items = run_query(query, data)

    assert returned_items == [
        {"title": "a"},
        {"title": "b"},
    ]


def test_sort():
    data = [
        {"title": "c", "ratings": 1},
        {"title": "b", "ratings": 2},
        {"title": "a", "ratings": 5},
    ]
    query = [
        ["SCAN", ["movies"]],
        ["SORT", [["ratings", "DESC"]]],
        ["PROJECTION", ["title"]],
    ]

    returned_items = run_query(query, data)

    assert returned_items == [{"title": "a"}, {"title": "b"}, {"title": "c"}]
