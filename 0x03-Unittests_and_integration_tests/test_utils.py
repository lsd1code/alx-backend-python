#!/usr/bin/env python3


"""
#! Parameterize a unit test

#? Create a TestAccessNestedMap class that inherits from unittest.TestCase
#? Implement the TestAccessNestedMap.test_access_nested_map() method to test that the method returns what is supposed to.
#? Decorate the method with @parameterized.expand to test the function for following inputs:
    >>> nested_map, path = ({'a': 1}, ['a'])
    >>> nested_map, path = ({'a': {'b': 2}}, ['a',])
    >>> nested_map, path = ({'a': {'b': 2}}, ['a', 'b'])
"""

from typing import Any
import unittest
from utils import access_nested_map
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([  # type:ignore
        ({'a': 1}, ['a'], 1),
        ({'a': {'b': 2}}, ['a',], {'b': 2}),
        ({'a': {'b': 2}}, ['a', 'b'], 2)
    ])
    def test_access_nested_map(self, nested_map: dict[str, Any], path: list[str], expected: int):
        self.assertEqual(access_nested_map(nested_map, path), expected)


    @parameterized.expand([  # type:ignore
        ({}, ['a'], KeyError),
        ({'a': 1}, ['a', 'b'], KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map: dict[str, Any], path: list[str], expected: Any):
        if expected == KeyError:
            with self.assertRaises(KeyError):
                access_nested_map(nested_map=nested_map, path=path)

        # self.assertRaises(access_nested_map(nested_map=nested_map, path=path), expected)


if __name__ == "__main__":
    unittest.main()


