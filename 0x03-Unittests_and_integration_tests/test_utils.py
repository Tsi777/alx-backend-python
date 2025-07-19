#!/usr/bin/env python3
"""
Comprehensive Unit Tests for the Utilities Module

This module includes detailed test cases for utility functions, featuring:
- Fully parameterized test decorators
- Extensive documentation for each test case
- Proper mocking of external dependencies
- Code formatting compliant with pycodestyle
- Clear validation of all requirements
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test Suite for the access_nested_map Function

    Validates both successful access patterns and correct error handling
    when navigating nested dictionary structures using key paths.
    """

    @parameterized.expand([
        # Test Case 1: Accessing the top-level key in a flat dictionary
        (
            {"a": 1},        # Input dictionary
            ("a",),          # Path tuple for top-level access
            1                # Expected return value
        ),
        # Test Case 2: Accessing a nested dictionary
        (
            {"a": {"b": 2}}, # Input with two levels of nesting
            ("a",),          # Path for first-level access
            {"b": 2}         # Expected nested dictionary
        ),
        # Test Case 3: Accessing a leaf node in a nested structure
        (
            {"a": {"b": 2}}, # Input with two levels of nesting
            ("a", "b"),      # Full path to the leaf node
            2                # Expected leaf value
        )
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Validate Successful Dictionary Access Patterns

        Tests that access_nested_map retrieves values correctly when:
        - Accessing top-level keys
        - Navigating nested dictionaries
        - Retrieving leaf node values

        Asserts:
        - The returned value matches the expected result
        - No exceptions raised for valid paths
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        # Test Case 1: Accessing a missing top-level key
        (
            {},              # Empty dictionary
            ("a",),          # Non-existent key access attempt
            "Key 'a' not found"  # Expected error message
        ),
        # Test Case 2: Accessing a missing nested key
        (
            {"a": 1},        # Flat dictionary
            ("a", "b"),      # Invalid nested access attempt
            "Key 'b' not found"  # Expected error message
        )
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """
        Validate Error Handling for Invalid Paths

        Tests that access_nested_map:
        - Raises KeyError for invalid paths
        - Provides accurate error messages
        - Correctly identifies missing keys

        Asserts:
        - KeyError exception is raised
        - Exception message matches the expected format
        - Correct key is identified in the error message
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_msg)


class TestGetJson(unittest.TestCase):
    """
    Test Suite for the get_json Function

    Verifies the functionality of HTTP JSON retrieval while:
    - Preventing actual network calls through mocking
    - Validating request construction and response handling
    """

    @parameterized.expand([
        # Test Case 1: Standard JSON response
        (
            "http://example.com",   # Test endpoint URL
            {"payload": True}       # Expected response payload
        ),
        # Test Case 2: Alternative endpoint
        (
            "http://holberton.io",  # Different test URL
            {"payload": False}     # Alternative response payload
        )
    ])
    @patch('utils.requests.get')  # Mocking requests.get
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Validate JSON Retrieval from HTTP Endpoints

        Tests that get_json:
        - Makes correct HTTP GET requests
        - Properly processes JSON responses
        - Returns expected payloads

        Mock Configuration:
        - Creates a mock response with a json() method
        - Configures mock to return the test payload
        - Verifies a single call to requests.get

        Asserts:
        - Correct URL was requested
        - Return value matches the test payload
        """
        # Configure the mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Execute the function under test
        result = get_json(test_url)

        # Verify mock interactions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
    Test Suite for the memoize Decorator

    Validates the correct implementation of method result caching:
    - Single execution of the underlying method
    - Consistent return values
    - Proper cache behavior
    """

    def test_memoize(self):
        """
        Validate Caching Behavior of Method Results

        Tests that the @memoize decorator:
        - Calls the underlying method only once
        - Returns the cached result on subsequent calls
        - Maintains consistency in return values

        Test Structure:
        1. Creates a test class with a memoized property
        2. Mocks the underlying method
        3. Verifies call count and return values
        """
        class TestClass:
            """Test class with a memoized property"""

            def a_method(self):
                """Method to be memoized"""
                return 42

            @memoize
            def a_property(self):
                """Memoized property using a_method"""
                return self.a_method()

        # Patch and test memoization behavior
        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            instance = TestClass()

            # First access - should call the underlying method
            self.assertEqual(instance.a_property, 42)
            
            # Second access - should use the cached result
            self.assertEqual(instance.a_property, 42)

            # Verify single call to the underlying method
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
