#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient.org method."""

    @parameterized.expand([  # type:ignore
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: PropertyMock):
        """Test that GithubOrgClient.org returns correct value.

        Verifies:
        1. get_json is called exactly once with correct URL
        2. The return value matches the mock payload
        3. No actual HTTP calls are made

        Args:
            org_name: Organization name to test
            mock_get_json: Mock object for get_json function
        """
        test_payload = {"login": org_name, "id": 123456}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"

        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
