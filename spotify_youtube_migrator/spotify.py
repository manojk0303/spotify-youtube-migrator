import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_youtube_migrator.utils import print_colored
from spotify_youtube_migrator.config import get_credentials

class SpotifyClient:
    def __init__(self):
        credentials = get_credentials("spotify")
        if not credentials:
            raise ValueError("Spotify credentials not found. Please run 'set-creds --spotify'.")

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            redirect_uri="http://localhost:8888/callback",
            scope="playlist-read-private user-library-read playlist-modify-public"
        ))

    def is_authenticated(self):
        try:
            self.sp.current_user()
            return True
        except:
            return False

    def get_playlist_tracks(self, playlist_url):
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        results = self.sp.playlist_tracks(playlist_id)
        tracks = results["items"]
        while results["next"]:
            results = self.sp.next(results)
            tracks.extend(results["items"])

        return [{"name": item["track"]["name"], "artist": item["track"]["artists"][0]["name"], "found": False} for item in tracks]

    def get_liked_songs(self):
        results = self.sp.current_user_saved_tracks(limit=50)
        tracks = results["items"]
        while results["next"]:
            results = self.sp.next(results)
            tracks.extend(results["items"])

        return [{"name": item["track"]["name"], "artist": item["track"]["artists"][0]["name"], "found": False} for item in tracks]

    def create_playlist(self, name, tracks):
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
            self.sp.playlist_add_items(playlist["id"], track_ids)
            print_colored(f"🎉 Playlist '{name}' created successfully on Spotify!", "blue")

        return tracks  # Return the updated tracks list