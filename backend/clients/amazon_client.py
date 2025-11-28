"""
Amazon Music API Client (Login With Amazon).
"""
import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AmazonMusicClient:
    """Client for interacting with the Amazon Music API."""
    
    # Note: Actual endpoints depend on region and API version (beta)
    BASE_URL = "https://api.music.amazon.com/v1"
    
    def __init__(self, access_token: str):
        """
        Initialize Amazon Music client with access token.
        
        Args:
            access_token: LWA access token
        """
        self.access_token = access_token
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make an authenticated request to the Amazon Music API.
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.access_token}'
        headers['x-api-key'] = kwargs.pop('client_id', '') # Required for some calls
        kwargs['headers'] = headers
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Amazon Music API request failed: {e}")
            raise
    
    def get_user_profile(self) -> Dict:
        """Get user profile information."""
        # LWA endpoint for profile
        url = "https://api.amazon.com/user/profile"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get Amazon profile: {e}")
            raise

    def get_playlists(self) -> List[Dict]:
        """
        Get user's playlists.
        Note: This endpoint is hypothetical/beta and requires specific scopes.
        """
        try:
            # Hypothetical endpoint for beta API
            data = self._make_request('GET', '/me/playlists')
            
            playlists = []
            for item in data.get('data', []):
                playlists.append({
                    'id': item.get('id'),
                    'name': item.get('name'),
                    'tracks_count': item.get('trackCount', 0),
                    'public': item.get('visibility') == 'PUBLIC',
                    'cover_image': item.get('image', {}).get('url'),
                    'creator': 'You' # Simplified
                })
            return playlists
        except Exception:
            # Return empty list if API access is not available yet
            logger.warning("Amazon Music API access not available or failed.")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """Get tracks from a playlist."""
        try:
            data = self._make_request('GET', f'/playlists/{playlist_id}/tracks')
            tracks = []
            for item in data.get('data', []):
                tracks.append({
                    'id': item.get('id'),
                    'title': item.get('name'),
                    'artist': item.get('artistName'),
                    'album': item.get('albumName'),
                    'duration': item.get('duration')
                })
            return tracks
        except Exception:
            return []
