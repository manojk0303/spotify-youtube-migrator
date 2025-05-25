# spotify.py - Updated
import spotipy
from spotify_youtube_migrator.utils import print_colored
from spotify_youtube_migrator.config import load_spotify_token

class SpotifyClient:
    def __init__(self):
        self.token_data = load_spotify_token()
        if not self.token_data:
            raise Exception("No Spotify token found. Please set your token using 'migrate-playlist set-token --spotify --token YOUR_TOKEN'")
        
        # Extract access token
        if isinstance(self.token_data, dict):
            access_token = self.token_data.get('access_token')
        else:
            access_token = self.token_data
        
        if not access_token:
            raise Exception("Invalid Spotify token format. Please get a new token from the auth website.")
        
        # Initialize Spotify client with the token
        self.sp = spotipy.Spotify(auth=access_token)
        
    def is_authenticated(self):
        """Check if the current token is valid."""
        try:
            # Try to get current user info to validate token
            user = self.sp.current_user()
            return user is not None
        except Exception as e:
            print_colored(f"❌ Spotify authentication failed: {str(e)}", "red")
            return False

    def get_playlist_tracks(self, playlist_url):
        """Get tracks from a Spotify playlist."""
        try:
            playlist_id = playlist_url.split("/")[-1].split("?")[0]
            results = self.sp.playlist_tracks(playlist_id)
            tracks = results["items"]
            
            while results["next"]:
                results = self.sp.next(results)
                tracks.extend(results["items"])

            return [{
                "name": item["track"]["name"], 
                "artist": item["track"]["artists"][0]["name"], 
                "found": False
            } for item in tracks if item["track"]]
            
        except Exception as e:
            print_colored(f"❌ Error fetching Spotify playlist: {str(e)}", "red")
            if "token expired" in str(e).lower() or "unauthorized" in str(e).lower():
                print_colored("🔑 Your Spotify token may have expired. Please get a new one from the auth website.", "yellow")
            raise

    def get_liked_songs(self):
        """Get user's liked songs from Spotify."""
        try:
            results = self.sp.current_user_saved_tracks(limit=50)
            tracks = results["items"]
            
            while results["next"]:
                results = self.sp.next(results)
                tracks.extend(results["items"])

            return [{
                "name": item["track"]["name"], 
                "artist": item["track"]["artists"][0]["name"], 
                "found": False
            } for item in tracks if item["track"]]
            
        except Exception as e:
            print_colored(f"❌ Error fetching Spotify liked songs: {str(e)}", "red")
            if "token expired" in str(e).lower() or "unauthorized" in str(e).lower():
                print_colored("🔑 Your Spotify token may have expired. Please get a new one from the auth website.", "yellow")
            raise

    def create_playlist(self, name, tracks):
        """Create a new playlist on Spotify with the given tracks."""
        try:
            user_id = self.sp.current_user()["id"]
            playlist = self.sp.user_playlist_create(user_id, name, public=True)
            track_ids = []

            for track in tracks:
                query = f"{track['name']} {track['artist']}"
                results = self.sp.search(query, limit=1, type="track")
                if results["tracks"]["items"]:
                    track_ids.append(results["tracks"]["items"][0]["id"])
                    track["found"] = True  # Update the found status
                    print_colored(f"✅ {track['name']} - {track['artist']} -> Found", "green")
                else:
                    print_colored(f"❌ {track['name']} - {track['artist']} -> Not Found", "red")

            if track_ids:
                # Add tracks in batches of 100 (Spotify API limit)
                for i in range(0, len(track_ids), 100):
                    batch = track_ids[i:i+100]
                    self.sp.playlist_add_items(playlist["id"], batch)
                
                print_colored(f"🎉 Playlist '{name}' created successfully on Spotify!", "blue")
                print_colored(f"🔗 Playlist URL: {playlist['external_urls']['spotify']}", "green")

            return tracks  # Return the updated tracks list
            
        except Exception as e:
            print_colored(f"❌ Error creating Spotify playlist: {str(e)}", "red")
            if "token expired" in str(e).lower() or "unauthorized" in str(e).lower():
                print_colored("🔑 Your Spotify token may have expired. Please get a new one from the auth website.", "yellow")
            raise