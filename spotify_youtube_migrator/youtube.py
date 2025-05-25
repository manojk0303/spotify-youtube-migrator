# youtube.py - Updated with simplified token handling
from ytmusicapi import YTMusic
from spotify_youtube_migrator.utils import print_colored
from spotify_youtube_migrator.config import load_youtube_auth

class YouTubeClient:
    def __init__(self):
        self.auth_data = load_youtube_auth()
        if not self.auth_data:
            raise Exception("No YouTube Music token found. Please set your token using 'migrate-playlist set-token --youtube --token YOUR_ACCESS_TOKEN'")
        
        try:
            # Initialize YTMusic with the auth headers
            # ytmusicapi can work with just Authorization header for many operations
            self.yt = YTMusic(self.auth_data)
            print_colored("✅ YouTube Music client initialized successfully.", "green")
        except Exception as e:
            print_colored(f"❌ Failed to initialize YouTube Music client: {str(e)}", "red")
            print_colored("🔑 Your YouTube token may be invalid or expired. Please get a new one from the auth website.", "yellow")
            
            # Try alternative initialization methods
            try:
                # Fallback: try with just the access token in a different format
                if isinstance(self.auth_data, dict) and "Authorization" in self.auth_data:
                    access_token = self.auth_data["Authorization"].replace("Bearer ", "")
                    # Create browser headers format as fallback
                    browser_headers = {
                        "cookie": f"__Secure-3PAPISID={access_token}",
                        "x-goog-authuser": "0"
                    }
                    self.yt = YTMusic(browser_headers)
                    print_colored("✅ YouTube Music client initialized with fallback method.", "green")
                else:
                    raise Exception("Could not initialize with any method")
            except:
                raise Exception("All initialization methods failed. Please get a fresh token from the auth website.")

    def get_playlist_tracks(self, playlist_id):
        """Get tracks from a YouTube Music playlist."""
        try:
            # Extract playlist ID from URL if needed
            if "youtube.com" in playlist_id or "music.youtube.com" in playlist_id:
                if "list=" in playlist_id:
                    playlist_id = playlist_id.split("list=")[-1].split("&")[0]
                else:
                    playlist_id = playlist_id.split("/")[-1].split("?")[0]
            
            results = self.yt.get_playlist(playlist_id)
            
            if not results or "tracks" not in results:
                print_colored("❌ Could not fetch playlist or playlist is empty.", "red")
                return []
            
            tracks = []
            for item in results["tracks"]:
                if item and "title" in item:
                    artist_name = "Unknown Artist"
                    if "artists" in item and item["artists"] and len(item["artists"]) > 0:
                        artist_name = item["artists"][0]["name"]
                    
                    tracks.append({
                        "name": item["title"], 
                        "artist": artist_name, 
                        "found": False
                    })
            
            return tracks
            
        except Exception as e:
            print_colored(f"❌ Error fetching YouTube Music playlist: {str(e)}", "red")
            if "unauthorized" in str(e).lower() or "forbidden" in str(e).lower() or "401" in str(e):
                print_colored("🔑 Your YouTube token has expired or is invalid. Please get a new one from the auth website.", "yellow")
            raise

    def create_playlist(self, name, tracks):
        """Create a new playlist on YouTube Music."""
        try:
            # Create the playlist
            playlist_id = self.yt.create_playlist(name, "Playlist migrated from Spotify")
            not_found_songs = []
            found_count = 0
            total_count = len(tracks)

            print_colored(f"🎵 Created playlist: {name}", "green")

            for i, track in enumerate(tracks):
                query = f"{track['name']} {track['artist']}"
                print_colored(f"🔍 Searching ({i+1}/{total_count}): {query}", "blue")
                
                try:
                    # Search for the song
                    results = self.yt.search(query, filter="songs")
                    
                    video_id = None
                    if results:
                        for result in results:
                            if "videoId" in result:
                                video_id = result["videoId"]
                                break

                    if video_id:
                        # Add the song to the playlist
                        self.yt.add_playlist_items(playlist_id, [video_id])
                        track["found"] = True
                        found_count += 1
                        print_colored(f"✅ {track['name']} - {track['artist']} -> Added", "green")
                    else:
                        not_found_songs.append(f"{track['name']} - {track['artist']}")
                        print_colored(f"❌ {track['name']} - {track['artist']} -> Not Found", "red")
                        
                except Exception as search_error:
                    print_colored(f"⚠️ Error searching for song: {str(search_error)}", "yellow")
                    not_found_songs.append(f"{track['name']} - {track['artist']}")
                    if "unauthorized" in str(search_error).lower() or "401" in str(search_error):
                        print_colored("🔑 Token expired during operation. Please get a new token.", "yellow")
                        break

            print_colored(f"\n🎵 Added {found_count} out of {total_count} tracks", "blue")
            print_colored(f"🔗 Playlist: https://music.youtube.com/playlist?list={playlist_id}", "green")
            
            if not_found_songs:
                print_colored(f"\n🚨 {len(not_found_songs)} songs not found:", "red")
                for song in not_found_songs[:3]:  # Show first 3
                    print_colored(f"  - {song}", "red")
                if len(not_found_songs) > 3:
                    print_colored(f"  ... and {len(not_found_songs) - 3} more", "red")

            return tracks
            
        except Exception as e:
            print_colored(f"❌ Error creating YouTube Music playlist: {str(e)}", "red")
            if "unauthorized" in str(e).lower() or "forbidden" in str(e).lower() or "401" in str(e):
                print_colored("🔑 Your YouTube token has expired or is invalid. Please get a new one from the auth website.", "yellow")
            raise
