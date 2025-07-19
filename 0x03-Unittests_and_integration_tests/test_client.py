#!/usr/bin/env python3
"""
Comprehensive Testing Framework for GithubOrgClient

This module includes thorough unit and integration tests for the GithubOrgClient
class, ensuring all specified functionalities while adhering to:
- Proper test isolation using mocking
- Fully parameterized test cases
- Detailed documentation
- Compliance with pycodestyle standards
"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit Test Suite for the GithubOrgClient Class

    Tests individual methods using mocked dependencies to confirm
    internal logic without making actual HTTP requests.
    """

    @parameterized.expand([
        ("google", {"login": "google"}, "https://api.github.com/orgs/google"),
        ("abc", {"login": "abc"}, "https://api.github.com/orgs/abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, expected_url, mock_get_json):
        """
        Verify that GithubOrgClient.org returns the correct organization data.

        Args:
            org_name: The name of the organization being tested
            expected_response: The anticipated organization data
            expected_url: The URL that should be requested
            mock_get_json: Mock for the get_json function

        Ensures:
            - get_json is called exactly once with the correct URL
            - The expected organization data is returned
            - No real HTTP requests are made
        """
        mock_get_json.return_value = expected_response

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_response)
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Verify that the _public_repos_url property returns the correct URL.

        Ensures:
            - Retrieves the correct repos URL from the organization payload
            - Utilizes the memoized org property
            - Properly manages property access
        """
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch('client.GithubOrgClient.org',
                  new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                test_payload["repos_url"]
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Verify that public_repos returns the correct list of repositories.

        Args:
            mock_get_json: Mock for the get_json function

        Ensures:
            - Returns the correct list of repository names
            - Utilizes the _public_repos_url property
            - Calls get_json exactly once
            - Properly processes the repository data
        """
        test_repos = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_repos

        with patch('client.GithubOrgClient._public_repos_url',
                  new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({}, "my_license", False),
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Verify that has_license correctly identifies the presence of a license.

        Args:
            repo: The repository dictionary to test
            license_key: The license key to check
            expected: The anticipated boolean outcome

        Ensures:
            - Correctly handles the absence of a license key
            - Accurately matches license keys
            - Returns the expected boolean outcome
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration Test Suite for GithubOrgClient

    Tests the entire functionality with mocked HTTP responses using
    fixtures from fixtures.py to simulate real API responses.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup method for the class - runs once before any tests

        Configures the requests.get mock to return appropriate
        fixtures based on requested URLs.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Determine which fixture to return based on the URL"""
            if url.endswith("/orgs/google"):
                return Mock(json=lambda: cls.org_payload)
            if url.endswith("/orgs/google/repos"):
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Teardown method for the class - runs after all tests complete

        Stops the patcher to restore original functionality.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Verify that public_repos returns the expected repositories.

        Ensures:
            - Returns the complete list of anticipated repositories
            - Correctly handles the integration between methods
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Verify public_repos with license filtering.

        Ensures:
            - Correctly filters repositories by license
            - Returns only repositories licensed under Apache 2.0
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()#!/usr/bin/env python3
"""
Comprehensive Testing Framework for GithubOrgClient

This module includes thorough unit and integration tests for the GithubOrgClient
class, ensuring all specified functionalities while adhering to:
- Proper test isolation using mocking
- Fully parameterized test cases
- Detailed documentation
- Compliance with pycodestyle standards
"""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit Test Suite for the GithubOrgClient Class

    Tests individual methods using mocked dependencies to confirm
    internal logic without making actual HTTP requests.
    """

    @parameterized.expand([
        ("google", {"login": "google"}, "https://api.github.com/orgs/google"),
        ("abc", {"login": "abc"}, "https://api.github.com/orgs/abc"),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, expected_url, mock_get_json):
        """
        Verify that GithubOrgClient.org returns the correct organization data.

        Args:
            org_name: The name of the organization being tested
            expected_response: The anticipated organization data
            expected_url: The URL that should be requested
            mock_get_json: Mock for the get_json function

        Ensures:
            - get_json is called exactly once with the correct URL
            - The expected organization data is returned
            - No real HTTP requests are made
        """
        mock_get_json.return_value = expected_response

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_response)
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Verify that the _public_repos_url property returns the correct URL.

        Ensures:
            - Retrieves the correct repos URL from the organization payload
            - Utilizes the memoized org property
            - Properly manages property access
        """
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}

        with patch('client.GithubOrgClient.org',
                  new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                test_payload["repos_url"]
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Verify that public_repos returns the correct list of repositories.

        Args:
            mock_get_json: Mock for the get_json function

        Ensures:
            - Returns the correct list of repository names
            - Utilizes the _public_repos_url property
            - Calls get_json exactly once
            - Properly processes the repository data
        """
        test_repos = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_repos

        with patch('client.GithubOrgClient._public_repos_url',
                  new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({}, "my_license", False),
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Verify that has_license correctly identifies the presence of a license.

        Args:
            repo: The repository dictionary to test
            license_key: The license key to check
            expected: The anticipated boolean outcome

        Ensures:
            - Correctly handles the absence of a license key
            - Accurately matches license keys
            - Returns the expected boolean outcome
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration Test Suite for GithubOrgClient

    Tests the entire functionality with mocked HTTP responses using
    fixtures from fixtures.py to simulate real API responses.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup method for the class - runs once before any tests

        Configures the requests.get mock to return appropriate
        fixtures based on requested URLs.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Determine which fixture to return based on the URL"""
            if url.endswith("/orgs/google"):
                return Mock(json=lambda: cls.org_payload)
            if url.endswith("/orgs/google/repos"):
                return Mock(json=lambda: cls.repos_payload)
            return Mock(json=lambda: {})

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Teardown method for the class - runs after all tests complete

        Stops the patcher to restore original functionality.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Verify that public_repos returns the expected repositories.

        Ensures:
            - Returns the complete list of anticipated repositories
            - Correctly handles the integration between methods
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Verify public_repos with license filtering.

        Ensures:
            - Correctly filters repositories by license
            - Returns only repositories licensed under Apache 2.0
        """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == '__main__':
    unittest.main()
