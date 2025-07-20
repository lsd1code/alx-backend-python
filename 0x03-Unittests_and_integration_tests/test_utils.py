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
from utils import access_nested_map, get_json
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


if __name__ == "__main__":
    unittest.main()
