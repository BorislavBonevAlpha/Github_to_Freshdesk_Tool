import unittest
from unittest.mock import patch, MagicMock, Mock
from requests import HTTPError
from client_models.freshdesk import FreshdeskAPI


class TestFreshdeskAPI(unittest.TestCase):

    def setUp(self):
        self.freshdesk_api = FreshdeskAPI("dummy_api_key")

    @patch('requests.get')
    def test_get_freshdesk_contact_success(self, mock_get):
        # Making a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': 123, 'name': 'Borislav', 'email': 'bobi@proba.com'}]
        mock_get.return_value = mock_response

        # Calling the method
        result = self.freshdesk_api.get_freshdesk_contact("proba", "bobi@proba.com")

        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 123)
        self.assertEqual(result['name'], 'Borislav')
        self.assertEqual(result['email'], 'bobi@proba.com')

    @patch('requests.get')
    def test_get_freshdesk_contact_timeout(self, mock_get):
        # Testing if timeout works
        mock_get.side_effect = TimeoutError

        # Calling the method
        result = self.freshdesk_api.get_freshdesk_contact("proba", "bobi@proba.com", timeout=5, retries=2)

        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_freshdesk_contact_http_error(self, mock_get):
        # Testing the response to raise an HTTPError
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError(response=Mock(status_code=404))
        mock_get.return_value = mock_response

        # Calling the method
        result = self.freshdesk_api.get_freshdesk_contact("proba", "bobi@proba.com")

        self.assertFalse(result)

    @patch('requests.post')
    @patch('requests.put')
    def test_create_or_update_contact_create(self, mock_put, mock_post):
        # Testing a response for creation
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 123}
        mock_post.return_value = mock_response

        # Calling the method
        result = self.freshdesk_api.create_or_update_contact("proba", {'name': 'Borislav', 'email': 'bobi@proba.com'})

        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 123)
        mock_put.assert_not_called()

    @patch('requests.post')
    @patch('requests.put')
    def test_create_or_update_contact_update(self, mock_put, mock_post):
        # Testing a response for update
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 123}
        mock_post.return_value = mock_response

        # Calling the method
        result = self.freshdesk_api.create_or_update_contact("proba",
                                                             {'id': 123, 'name': 'Borislav', 'email': 'bobi@proba.com'})

        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 123)
        mock_put.assert_not_called()

    @patch('requests.delete')
    def test_soft_delete_contact_success(self, mock_delete):
        # Testing a response for successful soft deletion
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        # Calling the method
        result = self.freshdesk_api.soft_delete_contact("proba", 123)

        self.assertTrue(result)

    @patch('requests.delete')
    def test_permanently_delete_contact_success(self, mock_delete):
        # Testing a response for successful hard deletion
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        # Calling the method
        result = self.freshdesk_api.permanently_delete_contact("proba", {'id': 123, 'name': 'Borislav',
                                                                         'email': 'bobi@proba.com'})

        self.assertFalse(result)
