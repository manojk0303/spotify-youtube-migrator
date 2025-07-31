from ytmusicapi import YTMusic
from spotify_youtube_migrator.utils import print_colored

class YouTubeClient:
    def __init__(self):
        self.yt = YTMusic("browser.json")

    def get_playlist_tracks(self, playlist_url):
        playlist_id = playlist_url.split("=")[-1]
        results = self.yt.get_playlist(playlist_id)
        return [{"name": item["title"], "artist": item["artists"][0]["name"]} for item in results["tracks"]]

    def create_playlist(self, name, tracks):
        playlist_id = self.yt.create_playlist(name, "Playlist migrated from Spotify")
        not_found_songs = []

        for track in tracks:
            query = f"{track['name']} {track['artist']}"
            results = self.yt.search(query)
            if results:
                video_id = results[0]["videoId"]
                self.yt.add_playlist_items(playlist_id, [video_id])
                track["found"] = True  # Update the found status
                print_colored(f"✅ {track['name']} - {track['artist']} -> Found", "green")
            else:
                not_found_songs.append(f"{track['name']} - {track['artist']}")
                print_colored(f"❌ {track['name']} - {track['artist']} -> Not Found", "red")

        if not_found_songs:
            print_colored("\n🚨 The following songs were not found on YouTube Music:", "red")
            for song in not_found_songs:
                print_colored(song, "red")

        return tracks  # Return the updated tracks list