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

import requests
from typing import Any
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
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


class TestGetJson(unittest.TestCase):
    @parameterized.expand([  # type:ignore
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: Any, test_payload: Any):
        with patch('__main__.requests.get') as mock_requests_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_requests_get.return_value = mock_response

            result = get_json(test_url)

            mock_requests_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
            
        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            instance = TestClass()
            
            result1 = instance.a_property
            result2 = instance.a_property
            
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
