import argparse
from spotify_youtube_migrator.spotify import SpotifyClient
from spotify_youtube_migrator.youtube import YouTubeClient
from spotify_youtube_migrator.utils import print_colored, setup_logging
from spotify_youtube_migrator.config import set_credentials, get_credentials

def main():
    parser = argparse.ArgumentParser(description="🎵 Migrate playlists between Spotify and YouTube Music. 🎶")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Set credentials command
    set_creds_parser = subparsers.add_parser("set-creds", help="Set your Spotify and YouTube Music credentials.")
    set_creds_parser.add_argument("--spotify", action="store_true", help="Set Spotify credentials.")
    set_creds_parser.add_argument("--youtube", action="store_true", help="Set YouTube Music credentials.")

    # Migrate playlist command
    migrate_parser = subparsers.add_parser("migrate", help="Migrate playlists between platforms.")
    migrate_parser.add_argument("--source", choices=["spotify", "youtube"], required=True, help="Source platform.")
    migrate_parser.add_argument("--destination", choices=["spotify", "youtube"], required=True, help="Destination platform.")
    migrate_parser.add_argument("--playlist", help="Playlist URL or 'liked_songs' for Spotify liked songs.")
    migrate_parser.add_argument("--name", help="Name of the new playlist (optional).")
    migrate_parser.add_argument("--log", action="store_true", help="Enable detailed logging.")
    migrate_parser.add_argument("--stats", action="store_true", help="Display migration statistics.")

    args = parser.parse_args()

    if args.command == "set-creds":
        if args.spotify:
            set_credentials("spotify")
        elif args.youtube:
            set_credentials("youtube")
        else:
            print_colored("🚨 Please specify --spotify or --youtube to set credentials.", "red")
    elif args.command == "migrate":
        setup_logging(args.log)

        if args.source == "spotify" and args.destination == "youtube":
            print_colored("🚀 Migrating from Spotify to YouTube Music...", "blue")
            spotify_client = SpotifyClient()
            youtube_client = YouTubeClient()

            if not spotify_client.is_authenticated():
                print_colored("🔑 Spotify credentials not found. Please run 'set-creds --spotify'.", "red")
                return

            if args.playlist == "liked_songs":
                print_colored("❤️ Fetching Spotify Liked Songs...", "blue")
                tracks = spotify_client.get_liked_songs()
            else:
                print_colored(f"🎧 Fetching Spotify Playlist: {args.playlist}", "blue")
                tracks = spotify_client.get_playlist_tracks(args.playlist)

            playlist_name = args.name or "My Spotify Playlist"
            tracks = youtube_client.create_playlist(playlist_name, tracks)  # Update tracks with found status

        elif args.source == "youtube" and args.destination == "spotify":
            print_colored("🚀 Migrating from YouTube Music to Spotify...", "blue")
            youtube_client = YouTubeClient()
            spotify_client = SpotifyClient()

            if not spotify_client.is_authenticated():
                print_colored("🔑 Spotify credentials not found. Please run 'set-creds --spotify'.", "red")
                return

            print_colored(f"🎧 Fetching YouTube Music Playlist: {args.playlist}", "blue")
            tracks = youtube_client.get_playlist_tracks(args.playlist)

            playlist_name = args.name or "My YouTube Playlist"
            tracks = spotify_client.create_playlist(playlist_name, tracks)  # Update tracks with found status
        else:
            print_colored("🚨 Invalid source or destination platform.", "red")

        if args.stats:
            print_colored("\n📊 Migration Statistics:", "blue")
            print_colored(f"✅ Total Songs: {len(tracks)}", "green")
            print_colored(f"❌ Not Found: {len([t for t in tracks if not t['found']])}", "red")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()