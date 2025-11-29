import os
import urllib.parse
import requests

from flask import redirect, url_for, request, session, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

from config.config import app
from config.celery_config import celery
from tasks import transfer_playlist_task, transfer_spotify_to_youtube_task, transfer_deezer_to_spotify_task, transfer_amazon_to_spotify_task
from clients.youtube_client import YouTubeClient
from clients.spotify_client import SpotifyClient
from clients.deezer_client import DeezerClient
from clients.amazon_client import AmazonMusicClient

from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest
from urllib.parse import urlparse, parse_qs
from typing import Optional

load_dotenv(override=True)

CORS(
    app,
    origins=[
        "https://playlifts.com",
        "https://www.playlifts.com",
        "https://api.playlifts.com",
        "https://staysoft.comporhub.com",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    supports_credentials=True,
)

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
)

SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://staysoft.comporhub.com")

app.secret_key = os.getenv("SECRET_KEY")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

DEEZER_APP_ID = os.getenv("DEEZER_APP_ID")
DEEZER_SECRET_KEY = os.getenv("DEEZER_SECRET_KEY")
DEEZER_REDIRECT_URI = os.getenv("DEEZER_REDIRECT_URI")
DEEZER_AUTH_URL = "https://connect.deezer.com/oauth/auth.php"
DEEZER_TOKEN_URL = "https://connect.deezer.com/oauth/access_token.php"

AMAZON_CLIENT_ID = os.getenv("AMAZON_CLIENT_ID")
AMAZON_CLIENT_SECRET = os.getenv("AMAZON_CLIENT_SECRET")
AMAZON_REDIRECT_URI = os.getenv("AMAZON_REDIRECT_URI")
AMAZON_AUTH_URL = "https://www.amazon.com/ap/oa"
AMAZON_TOKEN_URL = "https://api.amazon.com/auth/o2/token"


def get_youtube_credentials():
    if "youtube_token" not in session:
        return None

    creds_data = session["youtube_token"]
    credentials = Credentials(
        token=creds_data["token"],
        refresh_token=creds_data.get("refresh_token"),
        token_uri=creds_data["token_uri"],
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        scopes=creds_data["scopes"],
    )

    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(GoogleRequest())
                session["youtube_token"] = {
                    "token": credentials.token,
                    "refresh_token": credentials.refresh_token,
                    "token_uri": credentials.token_uri,
                    "client_id": credentials.client_id,
                    "client_secret": credentials.client_secret,
                    "scopes": credentials.scopes,
                }
            except Exception as e:
                app.logger.error(f"Failed to refresh YouTube token: {e}")
                return None
        else:
            return None
    return credentials


def _extract_spotify_playlist_id(value: str) -> Optional[str]:
    if not value:
        return None

    if "/" not in value and "http" not in value:
        return value.strip()

    try:
        parsed = urllib.parse.urlparse(value)
        parts = parsed.path.strip("/").split("/")
        if "playlist" in parts:
            idx = parts.index("playlist")
            if idx + 1 < len(parts):
                return parts[idx + 1]
    except Exception:
        pass
    return None


@app.route("/")
def index():
    return jsonify(
        {
            "message": "Welcome to the Playlifts API! Documentation is available at https://github.com/esosaoh/playlifts/blob/main/README.md"
        }
    )


@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/spotify/login")
def spotify_login():
    scope = "user-read-private user-read-email user-library-modify playlist-read-private playlist-modify-public playlist-modify-private"
    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "show_dialog": True,
    }
    auth_url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"
    if request.args.get("redirect") == "true":
        return redirect(auth_url)
    return jsonify({"auth_url": auth_url})


@app.route("/spotify/callback")
def spotify_callback():
    if "error" in request.args:
        return jsonify({"status": "error", "message": request.args["error"]}), 400
    if "code" not in request.args:
        return (
            jsonify({"status": "error", "message": "Authorization code not found"}),
            400,
        )
    try:
        auth_code = request.args["code"]
        req_body = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        }
        response = requests.post(SPOTIFY_TOKEN_URL, data=req_body)
        if response.status_code != 200:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Token request failed with status {response.status_code}",
                    }
                ),
                400,
            )

        token_info = response.json()
        if "access_token" not in token_info:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"No access token in response. Response: {token_info}",
                    }
                ),
                400,
            )

        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]
        session["is_logged_in"] = True

        resp = redirect(FRONTEND_URL)
        resp.set_cookie(
            "is_logged_in", "true", samesite="None", secure=True, httponly=False
        )
        return resp
    except Exception:
        app.logger.exception("Error in spotify_callback")
        raise


@app.route("/spotify/playlists", methods=["GET"])
def spotify_playlists():
    if "access_token" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        headers = {"Authorization": f"Bearer {session['access_token']}"}
        user_response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        if user_response.status_code != 200:
            return jsonify({"error": "Failed to fetch user profile"}), 400
        user_data = user_response.json()
        current_user_id = user_data["id"]

        all_playlists = []
        offset = 0
        limit = 50
        while True:
            response = requests.get(
                f"https://api.spotify.com/v1/me/playlists?limit={limit}&offset={offset}",
                headers=headers,
            )
            if response.status_code != 200:
                return (
                    jsonify(
                        {"error": f"Failed to fetch playlists: {response.status_code}"}
                    ),
                    400,
                )
            playlists_data = response.json()
            items = playlists_data.get("items", [])
            if not items:
                break
            for playlist in items:
                if playlist["owner"]["id"] == current_user_id:
                    cover_image = None
                    if playlist.get("images"):
                        cover_image = playlist["images"][0]["url"]
                    all_playlists.append(
                        {
                            "id": playlist["id"],
                            "name": playlist["name"],
                            "tracks_count": playlist["tracks"]["total"],
                            "owner": playlist["owner"]["display_name"],
                            "public": playlist.get("public", False),
                            "cover_image": cover_image,
                        }
                    )
            offset += limit
            if len(items) < limit:
                break
        return jsonify({"playlists": all_playlists})
    except Exception:
        app.logger.exception("Error in spotify_playlists")
        raise


@app.route("/spotify/playlists/create", methods=["POST"])
def create_spotify_playlist():
    if "access_token" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    try:
        data = request.json
        name = data.get("name")
        description = data.get("description", "")

        if not name:
            return jsonify({"error": "Playlist name is required"}), 400

        # Get user ID first
        headers = {"Authorization": f"Bearer {session['access_token']}"}
        user_response = requests.get("https://api.spotify.com/v1/me", headers=headers)
        if user_response.status_code != 200:
            return jsonify({"error": "Failed to fetch user profile"}), 400
        user_id = user_response.json()["id"]

        spotify_client = SpotifyClient(api_token=session["access_token"])
        playlist_id = spotify_client.create_playlist(user_id, name, description)

        return jsonify({"id": playlist_id, "name": name}), 201

    except Exception as e:
        app.logger.exception("Error creating playlist")
        return jsonify({"error": str(e)}), 500



@app.route("/spotify/transfer", methods=["POST"])
def spotify_transfer():
    credentials = get_youtube_credentials()
    if not credentials:
        return jsonify({"error": "Not authenticated with YouTube"}), 401

    data = request.json or {}
    raw_spotify = data.get("spotify_playlist_id") or data.get("spotify_url")
    youtube_playlist_id = data.get("youtube_playlist_id")

    if not raw_spotify or not youtube_playlist_id:
        return (
            jsonify(
                {
                    "error": "Missing 'spotify_playlist_id' (or 'spotify_url') and 'youtube_playlist_id'"
                }
            ),
            400,
        )

    spotify_playlist_id = _extract_spotify_playlist_id(raw_spotify)
    if not spotify_playlist_id:
        return jsonify({"error": "Invalid Spotify playlist identifier"}), 400

    youtube_token_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    task = transfer_spotify_to_youtube_task.delay(
        None, spotify_playlist_id, youtube_playlist_id, youtube_token_data
    )
    return jsonify({"task_id": task.id}), 202


@app.route("/youtube/login")
def youtube_login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=YOUTUBE_SCOPES,
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI

    auth_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )
    session["google_oauth_state"] = state
    
    if request.args.get("redirect") == "true":
        return redirect(auth_url)
        
    return jsonify({"auth_url": auth_url})


@app.route("/youtube/callback")
def youtube_callback():
    state = session.get("google_oauth_state")
    if not state:
        return jsonify({"error": "Invalid OAuth state"}), 400
    if request.args.get("state") != state:
        return jsonify({"error": "State mismatch"}), 400

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=YOUTUBE_SCOPES,
        state=state,
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session["youtube_token"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    session["is_youtube_logged_in"] = True

    resp = redirect(FRONTEND_URL)
    resp.set_cookie(
        "is_youtube_logged_in", "true", samesite="None", secure=True, httponly=False
    )
    return resp


@app.route("/youtube/playlists")
def youtube_playlists():
    credentials = get_youtube_credentials()
    if not credentials:
        return (
            jsonify(
                {"error": "Not authenticated with YouTube or token refresh failed"}
            ),
            401,
        )
    yt_client = YouTubeClient(credentials=credentials)
    playlists = yt_client.get_playlists()
    return jsonify({"playlists": playlists})


@app.route("/youtube/transfer", methods=["POST"])
def youtube_transfer():
    if "access_token" not in session:
        return redirect(url_for("spotify_login"))

    try:
        youtube_url = request.json["url"]
        target_playlist_id = request.json.get("playlist_id")

        parsed_url = urlparse(youtube_url)
        if "youtube.com" not in parsed_url.netloc:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        query_params = parse_qs(parsed_url.query)
        playlist_id = query_params.get("list", [None])[0]
        if not playlist_id:
            return jsonify({"error": "No playlist ID found"}), 400

        task = transfer_playlist_task.delay(
            session["access_token"], playlist_id, target_playlist_id
        )

        return jsonify({"task_id": task.id}), 202
    except Exception:
        app.logger.exception("Error in youtube_transfer")
        raise


@app.route("/auth/check", methods=["GET"])
def check_login():
    spotify_logged_in = session.get("is_logged_in", False)
    youtube_logged_in = session.get("is_youtube_logged_in", False)
    deezer_logged_in = session.get("is_deezer_logged_in", False)
    amazon_logged_in = session.get("is_amazon_logged_in", False)
    return (
        jsonify(
            {
                "spotify_logged_in": spotify_logged_in,
                "youtube_logged_in": youtube_logged_in,
                "deezer_logged_in": deezer_logged_in,
                "amazon_logged_in": amazon_logged_in,
                "both_logged_in": spotify_logged_in and youtube_logged_in,
            }
        ),
        200,
    )


@app.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    resp = jsonify({"status": "success", "message": "Logged out successfully"})
    resp.delete_cookie("is_logged_in")
    resp.delete_cookie("is_youtube_logged_in")
    resp.delete_cookie("is_deezer_logged_in")
    resp.delete_cookie("is_amazon_logged_in")
    return resp


@app.route("/tasks/status/<task_id>")
def task_status(task_id):
    try:
        task = celery.AsyncResult(task_id)

        if task.state == "PENDING":
            response = {
                "state": task.state,
                "status": "Waiting to start",
                "progress": 0,
            }
        elif task.state == "PROGRESS":
            try:
                progress_info = task.info or {}
                response = {
                    "state": task.state,
                    "progress": progress_info.get("progress", 0),
                    "current": progress_info.get("current", 0),
                    "total": progress_info.get("total", 0),
                    "status": progress_info.get("status", "In progress..."),
                }
            except Exception as e:
                app.logger.error(f"Error getting progress info: {e}")
                response = {
                    "state": task.state,
                    "progress": 0,
                    "current": 0,
                    "total": 0,
                    "status": "In progress...",
                }
        elif task.state == "SUCCESS":
            try:
                response = {"state": task.state, "result": task.result, "progress": 100}
            except Exception as e:
                app.logger.error(f"Error getting task result: {e}")
                response = {
                    "state": task.state,
                    "result": {
                        "success": {"count": 0, "tracks": []},
                        "failed": {"count": 0, "tracks": []},
                    },
                    "progress": 100,
                }
        elif task.state == "FAILURE":
            try:
                error_info = task.info if hasattr(task, "info") and task.info else {}

                if isinstance(error_info, dict):
                    error_msg = error_info.get("error", "Unknown error occurred")
                    error_type = error_info.get("error_type", "Exception")
                elif isinstance(error_info, Exception):
                    error_msg = str(error_info)
                    error_type = type(error_info).__name__
                else:
                    error_msg = (
                        str(error_info) if error_info else "Unknown error occurred"
                    )
                    error_type = "Exception"

                response = {
                    "state": task.state,
                    "error": error_msg,
                    "error_type": error_type,
                    "progress": 0,
                }
            except Exception as e:
                app.logger.error(f"Error getting failure info for task {task_id}: {e}")
                response = {
                    "state": task.state,
                    "error": "Task failed - unable to retrieve error details",
                    "error_type": "Exception",
                    "progress": 0,
                }
        else:
            try:
                status_info = (
                    str(task.info)
                    if hasattr(task, "info") and task.info
                    else "Unknown state"
                )
                response = {"state": task.state, "status": status_info, "progress": 0}
            except Exception as e:
                app.logger.error(f"Error getting task info for state {task.state}: {e}")
                response = {
                    "state": task.state,
                    "status": f"Task in {task.state} state",
                    "progress": 0,
                }

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error getting task status for {task_id}: {str(e)}")
        return (
            jsonify(
                {
                    "state": "ERROR",
                    "error": f"Failed to get task status: {str(e)}",
                    "progress": 0,
                }
            ),
            500,
        )


# ============================================================================
# DEEZER ROUTES
# ============================================================================

@app.route("/deezer/login")
def deezer_login():
    """Initiate Deezer OAuth flow."""
    perms = "basic_access,email,manage_library,delete_library"
    params = {
        "app_id": DEEZER_APP_ID,
        "redirect_uri": DEEZER_REDIRECT_URI,
        "perms": perms,
    }
    auth_url = f"{DEEZER_AUTH_URL}?{urllib.parse.urlencode(params)}"
    if request.args.get("redirect") == "true":
        return redirect(auth_url)
    return jsonify({"auth_url": auth_url})


@app.route("/deezer/callback")
def deezer_callback():
    """Handle Deezer OAuth callback."""
    if "error" in request.args:
        return jsonify({"status": "error", "message": request.args["error"]}), 400
    
    code = request.args.get("code")
    if not code:
        return jsonify({"status": "error", "message": "Authorization code not found"}), 400
    
    try:
        # Exchange code for access token
        params = {
            "app_id": DEEZER_APP_ID,
            "secret": DEEZER_SECRET_KEY,
            "code": code,
        }
        
        response = requests.get(DEEZER_TOKEN_URL, params=params)
        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Token request failed with status {response.status_code}"
            }), 400
        
        # Deezer returns access_token in query string format
        token_data = dict(urllib.parse.parse_qsl(response.text))
        
        if "access_token" not in token_data:
            return jsonify({
                "status": "error",
                "message": "No access token in response"
            }), 400
        
        # Store token in session
        session["deezer_access_token"] = token_data["access_token"]
        session["is_deezer_logged_in"] = True
        
        # Set expires if provided (Deezer tokens don't expire by default)
        if "expires" in token_data:
            session["deezer_expires_at"] = datetime.now().timestamp() + int(token_data["expires"])
        
        resp = redirect(FRONTEND_URL)
        resp.set_cookie(
            "is_deezer_logged_in", "true", samesite="None", secure=True, httponly=False
        )
        return resp
        
    except Exception:
        app.logger.exception("Error in deezer_callback")
        raise


@app.route("/deezer/playlists", methods=["GET"])
def deezer_playlists():
    """Get user's Deezer playlists."""
    if "deezer_access_token" not in session:
        return jsonify({"error": "Not authenticated with Deezer"}), 401
    
    try:
        deezer_client = DeezerClient(session["deezer_access_token"])
        playlists = deezer_client.get_playlists()
        return jsonify({"playlists": playlists})
    except Exception:
        app.logger.exception("Error in deezer_playlists")
        raise


@app.route("/deezer/transfer", methods=["POST"])
def deezer_transfer():
    """Initiate transfer from Deezer to another platform."""
    if "deezer_access_token" not in session:
        return jsonify({"error": "Not authenticated with Deezer"}), 401
    
    data = request.json
    source = data.get("source")
    target = data.get("target")
    playlist_id = data.get("playlist_id")
    
    if source != "deezer":
        return jsonify({"error": "Invalid source"}), 400
        
    if target == "spotify":
        if "access_token" not in session:
            return jsonify({"error": "Not authenticated with Spotify"}), 401
            
        task = transfer_deezer_to_spotify_task.delay(
            spotify_token=session["access_token"],
            deezer_token=session["deezer_access_token"],
            deezer_playlist_id=playlist_id,
            spotify_playlist_id=None  # Default to library for now
        )
        return jsonify({"task_id": task.id}), 202
        
    return jsonify({"error": "Unsupported target platform"}), 400



# ============================================================================
# AMAZON MUSIC ROUTES
# ============================================================================

@app.route("/amazon/login")
def amazon_login():
    """Initiate Amazon Music OAuth flow."""
    scope = "profile" # Add 'music::playlists:read' etc if available
    params = {
        "client_id": AMAZON_CLIENT_ID,
        "scope": scope,
        "response_type": "code",
        "redirect_uri": AMAZON_REDIRECT_URI,
    }
    auth_url = f"{AMAZON_AUTH_URL}?{urllib.parse.urlencode(params)}"
    if request.args.get("redirect") == "true":
        return redirect(auth_url)
    return jsonify({"auth_url": auth_url})


@app.route("/amazon/callback")
def amazon_callback():
    """Handle Amazon OAuth callback."""
    if "error" in request.args:
        return jsonify({"status": "error", "message": request.args["error"]}), 400
    
    code = request.args.get("code")
    if not code:
        return jsonify({"status": "error", "message": "Authorization code not found"}), 400
    
    try:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": AMAZON_REDIRECT_URI,
            "client_id": AMAZON_CLIENT_ID,
            "client_secret": AMAZON_CLIENT_SECRET,
        }
        
        response = requests.post(AMAZON_TOKEN_URL, data=data)
        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Token request failed: {response.text}"
            }), 400
        
        token_data = response.json()
        
        session["amazon_access_token"] = token_data["access_token"]
        session["amazon_refresh_token"] = token_data.get("refresh_token")
        session["is_amazon_logged_in"] = True
        
        resp = redirect(FRONTEND_URL)
        resp.set_cookie(
            "is_amazon_logged_in", "true", samesite="None", secure=True, httponly=False
        )
        return resp
        
    except Exception:
        app.logger.exception("Error in amazon_callback")
        raise


@app.route("/amazon/playlists", methods=["GET"])
def amazon_playlists():
    """Get user's Amazon Music playlists."""
    if "amazon_access_token" not in session:
        return jsonify({"error": "Not authenticated with Amazon Music"}), 401
    
    try:
        client = AmazonMusicClient(session["amazon_access_token"])
        playlists = client.get_playlists()
        return jsonify({"playlists": playlists})
    except Exception:
        app.logger.exception("Error in amazon_playlists")
        raise


@app.route("/amazon/transfer", methods=["POST"])
def amazon_transfer():
    """Initiate transfer from Amazon Music."""
    if "amazon_access_token" not in session:
        return jsonify({"error": "Not authenticated with Amazon Music"}), 401
    
    data = request.json
    source = data.get("source")
    target = data.get("target")
    playlist_id = data.get("playlist_id")
    
    if source != "amazon":
        return jsonify({"error": "Invalid source"}), 400
        
    if target == "spotify":
        if "access_token" not in session:
            return jsonify({"error": "Not authenticated with Spotify"}), 401
            
        task = transfer_amazon_to_spotify_task.delay(
            spotify_token=session["access_token"],
            amazon_token=session["amazon_access_token"],
            amazon_playlist_id=playlist_id,
            spotify_playlist_id=None  # Default to library for now
        )
        return jsonify({"task_id": task.id}), 202
        
    return jsonify({"error": "Unsupported target platform"}), 400


if __name__ == "__main__":
    app.run(port=8889, debug=False)
