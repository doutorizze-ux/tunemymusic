import unittest
from unittest.mock import MagicMock, patch
from clients.deezer_client import DeezerClient

class TestDeezerClient(unittest.TestCase):
    def setUp(self):
        self.access_token = "fake_token"
        self.client = DeezerClient(self.access_token)
    
    @patch('clients.deezer_client.requests.Session')
    def test_get_user_info(self, mock_session):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "name": "Test User"}
        mock_response.status_code = 200
        
        # Setup session mock
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response
        
        # Re-init client to use mocked session
        self.client = DeezerClient(self.access_token)
        self.client.session = mock_session_instance
        
        # Call method
        user_info = self.client.get_user_info()
        
        # Assertions
        self.assertEqual(user_info["id"], "123")
        self.assertEqual(user_info["name"], "Test User")
        mock_session_instance.request.assert_called_with(
            'GET', 
            'https://api.deezer.com/user/me', 
            params={'access_token': 'fake_token'}
        )

    @patch('clients.deezer_client.requests.Session')
    def test_search_track(self, mock_session):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {"id": "1001", "title": "Test Track", "artist": {"name": "Test Artist"}}
            ]
        }
        mock_response.status_code = 200
        
        mock_session_instance = mock_session.return_value
        mock_session_instance.request.return_value = mock_response
        
        self.client.session = mock_session_instance
        
        # Call method
        track_id = self.client.search_track("Test Artist", "Test Track")
        
        # Assertions
        self.assertEqual(track_id, "1001")

if __name__ == '__main__':
    unittest.main()
