import unittest
from unittest.mock import Mock, patch
from requests import HTTPError
from client_models.github import GitHubClient


class TestGitHubClient(unittest.TestCase):

    def setUp(self):
        self.github_client = GitHubClient("dummy_token")

    @patch('requests.get')
    def test_get_github_user_information_success(self, mock_get):
        # Making a successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'name': 'Borislav', 'email': 'bobi@proba.com', 'bio': 'Coding programmer'}
        mock_get.side_effect = [mock_response]

        # Calling the method
        result = self.github_client.get_github_user_information("borislav")

        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Borislav')
        self.assertEqual(result['email'], 'bobi@proba.com')
        self.assertEqual(result['bio'], 'Coding programmer')

    @patch('requests.get')
    def test_get_github_user_information_timeout(self, mock_get):
        # Testing if timeout works
        mock_get.side_effect = [TimeoutError]

        # Calling the method
        result = self.github_client.get_github_user_information("borislav", timeout=5, retries=2)

        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_github_user_information_http_error(self, mock_get):
        # Testing the response to raise an HTTPError
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError(response=Mock(status_code=404))
        mock_get.return_value = mock_response

        # Calling the method
        result = self.github_client.get_github_user_information("borislav")

        self.assertFalse(result)

