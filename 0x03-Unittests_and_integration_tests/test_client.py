#!/usr/bin/env python3

from typing import Any, Dict
import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
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

        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("test_org")

            result = client._public_repos_url

            self.assertEqual(
                result, "https://api.github.com/orgs/test_org/repos")

            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Any):
        """Test public_repos returns correct repository list.

        Verifies:
        1. Correct repository names are returned
        2. _public_repos_url property is accessed once
        3. get_json is called once with correct URL
        4. Payload structure is properly processed
        """

        test_repos_url = "https://api.github.com/orgs/test_org/repos"
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value=test_repos_url
        ) as mock_public_repos_url:
            mock_get_json.return_value = test_payload

            client = GithubOrgClient("test_org")

            repos = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)

            mock_public_repos_url.assert_called_once()

            mock_get_json.assert_called_once_with(test_repos_url)

    @parameterized.expand([  # type:ignore
        (
            {"license": {"key": "my_license"}}, 
            "my_license",                        
            True                                  
        ),
        (
            {"license": {"key": "other_license"}},  
            "my_license",                           
            False                                   
        ),
        (
            {"license": {}},  
            "my_license",     
            False             
        ),
        (
            {},               
            "my_license",     
            False             
        ),
    ])
    def test_has_license(self, repo: Dict[str, Any], license_key: str, expected: bool):
        """Test license detection in repository data.

        Verifies that has_license correctly identifies:
        - When a repo has the specified license
        - When a repo has a different license
        - Edge cases (missing license data)

        Args:
            repo: Repository data structure
            license_key: License identifier to check
            expected: Expected boolean result
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


org_payload = {
    "login": "test_org",
    "id": 123456,
    "repos_url": "https://api.github.com/orgs/test_org/repos"
}

repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}}
]

expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient with mocked HTTP requests."""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide test environment.

        Mocks requests.get to return fixture data based on requested URL.
        """
        # Define URL patterns
        cls.org_url = "https://api.github.com/orgs/{org}"
        cls.repos_url = org_payload["repos_url"]

        # Define side effect function for requests.get
        def get_side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url == cls.org_url.format(org="test_org"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.repos_url:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.get_patcher = patch('client.requests.get',
                                side_effect=get_side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests have run."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test repository listing without license filtering."""
        client = GithubOrgClient("test_org")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

        self.assertEqual(self.mock_get.call_count, 2)
        self.mock_get.assert_any_call(self.org_url.format(org="test_org"))
        self.mock_get.assert_any_call(self.repos_url)

    def test_public_repos_with_license(self):
        """Test repository listing with Apache 2.0 license filtering."""
        client = GithubOrgClient("test_org")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

        self.assertEqual(self.mock_get.call_count, 2)
        self.mock_get.assert_any_call(self.org_url.format(org="test_org"))
        self.mock_get.assert_any_call(self.repos_url)


if __name__ == "__main__":
    unittest.main()
