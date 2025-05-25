# config.py - Updated with simplified token handling
import json
import os
import requests
from spotify_youtube_migrator.utils import print_colored

# Define the directory for storing auth tokens
AUTH_DIR = os.path.join(os.path.expanduser("~"), ".spotify-youtube-migrator")
SPOTIFY_TOKEN_PATH = os.path.join(AUTH_DIR, "spotify_token.json")
YOUTUBE_AUTH_PATH = os.path.join(AUTH_DIR, "youtube_auth.json")

# Your centralized auth website URL
AUTH_WEBSITE_URL = "https://youtube-spotify-token-finder.vercel.app"  

def ensure_auth_dir():
    """Ensure the authentication directory exists."""
    os.makedirs(AUTH_DIR, exist_ok=True)

def check_auth_status():
    """Check if authentication files exist for both services."""
    ensure_auth_dir()
    spotify_auth_exists = os.path.exists(SPOTIFY_TOKEN_PATH) and _validate_spotify_token()
    youtube_auth_exists = os.path.exists(YOUTUBE_AUTH_PATH) and _validate_youtube_token()
    
    return {
        "spotify": spotify_auth_exists,
        "youtube": youtube_auth_exists
    }

def _validate_spotify_token():
    """Validate if Spotify token is still valid."""
    try:
        with open(SPOTIFY_TOKEN_PATH, 'r') as f:
            token_data = json.load(f)
        
        # Check if token exists and has required fields
        return "access_token" in token_data and token_data.get("access_token")
    except:
        return False

def _validate_youtube_token():
    """Validate if YouTube token is still valid."""
    try:
        with open(YOUTUBE_AUTH_PATH, 'r') as f:
            auth_data = json.load(f)
        
        # Check if auth data exists and has access token
        return "access_token" in auth_data and auth_data.get("access_token")
    except:
        return False

def clear_auth(platform=None):
    """Clear authentication tokens for specified platform or both."""
    ensure_auth_dir()
    
    if platform == "spotify" or platform is None:
        if os.path.exists(SPOTIFY_TOKEN_PATH):
            os.remove(SPOTIFY_TOKEN_PATH)
            print_colored("✅ Spotify authentication cleared.", "green")
    
    if platform == "youtube" or platform is None:
        if os.path.exists(YOUTUBE_AUTH_PATH):
            os.remove(YOUTUBE_AUTH_PATH)
            print_colored("✅ YouTube Music authentication cleared.", "green")
            
    if platform is None:
        print_colored("🔄 All authentication data cleared. You'll need to get new tokens from the auth website.", "blue")

def get_auth_instructions():
    """Get instructions for obtaining authentication tokens."""
    instructions = f"""
🔐 Authentication Required!

To use this package, you need to get authentication tokens from our website:

1. 🌐 Visit: {AUTH_WEBSITE_URL}
2. 🔑 Click "Login with Spotify" and authorize the application
3. 🎵 Click "Login with YouTube Music" and authorize the application
4. 📋 Copy the generated access tokens (just the token string, not the full JSON)
5. 🔧 Run the following commands to set your tokens:

   For Spotify:
   migrate-playlist set-token --spotify --token "YOUR_SPOTIFY_ACCESS_TOKEN"
   
   For YouTube Music:
   migrate-playlist set-token --youtube --token "YOUR_YOUTUBE_ACCESS_TOKEN"

6. ✅ You're ready to migrate playlists!

💡 Tokens are stored securely on your device and never shared.
"""
    return instructions

def save_spotify_token(token_data):
    """Save Spotify token to file."""
    ensure_auth_dir()
    
    # If token_data is a string, assume it's just the access token
    if isinstance(token_data, str):
        # Simple access token string
        token_obj = {"access_token": token_data}
    else:
        # Full token object
        token_obj = token_data
    
    with open(SPOTIFY_TOKEN_PATH, 'w') as f:
        json.dump(token_obj, f, indent=2)
    
    print_colored("✅ Spotify token saved successfully!", "green")

def save_youtube_token(auth_data):
    """Save YouTube authentication data to file."""
    ensure_auth_dir()
    
    # If auth_data is a string, assume it's just the access token
    if isinstance(auth_data, str):
        # Simple access token string
        auth_obj = {"access_token": auth_data}
    else:
        # If it's a dict, check if it has the access_token
        if isinstance(auth_data, dict) and "access_token" in auth_data:
            auth_obj = {"access_token": auth_data["access_token"]}
        else:
            try:
                # Try to parse as JSON
                parsed_data = json.loads(auth_data) if isinstance(auth_data, str) else auth_data
                if "access_token" in parsed_data:
                    auth_obj = {"access_token": parsed_data["access_token"]}
                else:
                    print_colored("❌ Invalid YouTube token format. Token should contain access_token.", "red")
                    return False
            except json.JSONDecodeError:
                print_colored("❌ Invalid YouTube token format. Please provide a valid access token.", "red")
                return False
    
    with open(YOUTUBE_AUTH_PATH, 'w') as f:
        json.dump(auth_obj, f, indent=2)
    
    print_colored("✅ YouTube Music token saved successfully!", "green")
    return True

def load_spotify_token():
    """Load Spotify token from file."""
    try:
        with open(SPOTIFY_TOKEN_PATH, 'r') as f:
            return json.load(f)
    except:
        return None

def load_youtube_auth():
    """Load YouTube authentication data from file."""
    try:
        with open(YOUTUBE_AUTH_PATH, 'r') as f:
            auth_data = json.load(f)
        
        # Convert simple token format to ytmusicapi compatible format
        if "access_token" in auth_data:
            # Create the headers format that ytmusicapi expects
            return {
                "Authorization": f"Bearer {auth_data['access_token']}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        
        return auth_data
    except:
        return None