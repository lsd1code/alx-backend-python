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
        result = client.org()

        expected_url = f"https://api.github.com/orgs/{org_name}"

        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct value from org payload.

        Verifies:
        1. The property returns the expected 'repos_url' value
        2. Uses mocked org payload instead of real API call
        3. Properly accesses nested data in payload
        """

        test_payload = {
            "login": "test_org",
            "id": 123456,
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("test_org")

            result = client._public_repos_url

            self.assertEqual(
                result, "https://api.github.com/orgs/test_org/repos")

            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
