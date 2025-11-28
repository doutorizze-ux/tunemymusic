"""
Deezer API Client for playlist management and track operations.
"""
import requests
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class DeezerClient:
    """Client for interacting with the Deezer API."""
    
    BASE_URL = "https://api.deezer.com"
    
    def __init__(self, access_token: str):
        """
        Initialize Deezer client with access token.
        
        Args:
            access_token: Deezer OAuth access token
        """
        self.access_token = access_token
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make an authenticated request to the Deezer API.
        
        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            JSON response from API
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # Add access token to params
        params = kwargs.get('params', {})
        params['access_token'] = self.access_token
        kwargs['params'] = params
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Deezer API request failed: {e}")
            raise
    
    def get_user_info(self) -> Dict:
        """
        Get current user information.
        
        Returns:
            User profile data
        """
        return self._make_request('GET', '/user/me')
    
    def get_playlists(self) -> List[Dict]:
        """
        Get all playlists for the authenticated user.
        
        Returns:
            List of playlist objects with id, name, tracks count, etc.
        """
        user_info = self.get_user_info()
        user_id = user_info['id']
        
        playlists = []
        index = 0
        limit = 50
        
        while True:
            data = self._make_request(
                'GET',
                f'/user/{user_id}/playlists',
                params={'index': index, 'limit': limit}
            )
            
            items = data.get('data', [])
            if not items:
                break
            
            for playlist in items:
                # Only include playlists created by the user
                if playlist.get('creator', {}).get('id') == user_id:
                    playlists.append({
                        'id': str(playlist['id']),
                        'name': playlist['title'],
                        'tracks_count': playlist.get('nb_tracks', 0),
                        'public': playlist.get('public', False),
                        'cover_image': playlist.get('picture_medium'),
                        'creator': playlist.get('creator', {}).get('name', 'Unknown')
                    })
            
            # Check if there are more playlists
            if 'next' not in data or len(items) < limit:
                break
            
            index += limit
        
        return playlists
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """
        Get all tracks from a Deezer playlist.
        
        Args:
            playlist_id: Deezer playlist ID
            
        Returns:
            List of track objects with artist, title, album info
        """
        tracks = []
        index = 0
        limit = 100
        
        while True:
            data = self._make_request(
                'GET',
                f'/playlist/{playlist_id}/tracks',
                params={'index': index, 'limit': limit}
            )
            
            items = data.get('data', [])
            if not items:
                break
            
            for track in items:
                artist_name = track.get('artist', {}).get('name', 'Unknown Artist')
                track_title = track.get('title', 'Unknown Track')
                album_name = track.get('album', {}).get('title', '')
                
                tracks.append({
                    'id': str(track['id']),
                    'artist': artist_name,
                    'title': track_title,
                    'album': album_name,
                    'duration': track.get('duration', 0),
                    'isrc': track.get('isrc'),  # International Standard Recording Code
                })
            
            # Check if there are more tracks
            if 'next' not in data or len(items) < limit:
                break
            
            index += limit
        
        return tracks
    
    def search_track(self, artist: str, title: str) -> Optional[str]:
        """
        Search for a track on Deezer by artist and title.
        
        Args:
            artist: Artist name
            title: Track title
            
        Returns:
            Deezer track ID if found, None otherwise
        """
        query = f'artist:"{artist}" track:"{title}"'
        
        try:
            data = self._make_request(
                'GET',
                '/search',
                params={'q': query, 'limit': 5}
            )
            
            results = data.get('data', [])
            if results:
                # Return the first match
                return str(results[0]['id'])
            
            # Try a simpler search if strict search fails
            simple_query = f"{artist} {title}"
            data = self._make_request(
                'GET',
                '/search',
                params={'q': simple_query, 'limit': 5}
            )
            
            results = data.get('data', [])
            if results:
                return str(results[0]['id'])
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching for track '{artist} - {title}': {e}")
            return None
    
    def create_playlist(self, title: str, description: str = "") -> str:
        """
        Create a new playlist for the authenticated user.
        
        Args:
            title: Playlist title
            description: Playlist description (optional)
            
        Returns:
            Created playlist ID
        """
        user_info = self.get_user_info()
        user_id = user_info['id']
        
        data = self._make_request(
            'POST',
            f'/user/{user_id}/playlists',
            params={'title': title}
        )
        
        playlist_id = str(data['id'])
        
        # Update description if provided
        if description:
            try:
                self._make_request(
                    'POST',
                    f'/playlist/{playlist_id}',
                    params={'description': description}
                )
            except Exception as e:
                logger.warning(f"Failed to set playlist description: {e}")
        
        return playlist_id
    
    def add_tracks_to_playlist(self, playlist_id: str, track_ids: List[str]) -> bool:
        """
        Add tracks to a Deezer playlist.
        
        Args:
            playlist_id: Deezer playlist ID
            track_ids: List of Deezer track IDs to add
            
        Returns:
            True if successful, False otherwise
        """
        if not track_ids:
            return True
        
        try:
            # Deezer accepts comma-separated track IDs
            tracks_param = ','.join(track_ids)
            
            self._make_request(
                'POST',
                f'/playlist/{playlist_id}/tracks',
                params={'songs': tracks_param}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding tracks to playlist {playlist_id}: {e}")
            return False
    
    def get_playlist_info(self, playlist_id: str) -> Dict:
        """
        Get information about a specific playlist.
        
        Args:
            playlist_id: Deezer playlist ID
            
        Returns:
            Playlist information
        """
        return self._make_request('GET', f'/playlist/{playlist_id}')
