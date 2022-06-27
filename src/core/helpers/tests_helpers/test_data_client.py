from unittest import mock

from django.test import TestCase

from core.helpers.data_client import DataClient


class DataClientTest(TestCase):

    def test_predict_attending(self):
        input_data = {
            'test': 'test'
        }
        post_response = {
            'attending': True
        }
        data_client = DataClient()
        with mock.patch(
            'core.helpers.data_client.requests.post'
        ) as mock_post:
            response = mock.MagicMock()
            response.json.return_value = post_response
            mock_post.return_value = response
            self.assertTrue(data_client.predict_attending(input_data=input_data))
