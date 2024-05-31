import unittest
from common.github_extraction_mapper import map_github_to_freshdesk


class TestMappers(unittest.TestCase):

    def test_get_github_to_freshdesk_mapping(self):
        mocked_user_info = {'name': 'Borislav', 'email': 'bobi@proba.com', 'bio': 'Coding programmer'}

        # Calling the method
        result = map_github_to_freshdesk(mocked_user_info)

        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Borislav')
        self.assertEqual(result['email'], 'bobi@proba.com')
        self.assertEqual(result['description'], 'Coding programmer')
