# cli.py - Updated
import argparse
import webbrowser
from spotify_youtube_migrator.spotify import SpotifyClient
from spotify_youtube_migrator.youtube import YouTubeClient
from spotify_youtube_migrator.utils import print_colored, setup_logging
from spotify_youtube_migrator.config import (
    check_auth_status, clear_auth, get_auth_instructions,
    save_spotify_token, save_youtube_token, AUTH_WEBSITE_URL
)

def main():
    parser = argparse.ArgumentParser(description="🎵 Migrate playlists between Spotify and YouTube Music. 🎶")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Auth commands
    auth_parser = subparsers.add_parser("auth", help="Manage authentication for Spotify and YouTube Music.")
    auth_subparsers = auth_parser.add_subparsers(dest="auth_command", help="Authentication commands")
    
    # Auth status command
    auth_subparsers.add_parser("status", help="Check authentication status for both services.")
    
    # Auth clear command
    clear_parser = auth_subparsers.add_parser("clear", help="Clear saved authentication data.")
    clear_parser.add_argument("--spotify", action="store_true", help="Clear only Spotify authentication.")
    clear_parser.add_argument("--youtube", action="store_true", help="Clear only YouTube Music authentication.")
    
    # Auth setup command
    auth_subparsers.add_parser("setup", help="Get instructions for setting up authentication.")

    # Set token commands
    token_parser = subparsers.add_parser("set-token", help="Set authentication tokens from the auth website.")
    token_parser.add_argument("--spotify", action="store_true", help="Set Spotify token.")
    token_parser.add_argument("--youtube", action="store_true", help="Set YouTube Music token.")
    token_parser.add_argument("--token", required=True, help="The token/auth data from the website.")

    # Migrate playlist command
    migrate_parser = subparsers.add_parser("migrate", help="Migrate playlists between platforms.")
    migrate_parser.add_argument("--source", choices=["spotify", "youtube"], required=True, help="Source platform.")
    migrate_parser.add_argument("--destination", choices=["spotify", "youtube"], required=True, help="Destination platform.")
    migrate_parser.add_argument("--playlist", help="Playlist URL or 'liked_songs' for Spotify liked songs.")
    migrate_parser.add_argument("--name", help="Name of the new playlist (optional).")
    migrate_parser.add_argument("--log", action="store_true", help="Enable detailed logging.")
    migrate_parser.add_argument("--stats", action="store_true", help="Display migration statistics.")

    args = parser.parse_args()

    if args.command == "auth":
        if args.auth_command == "status":
            status = check_auth_status()
            print_colored("\n🔐 Authentication Status:", "blue")
            print_colored(f"Spotify: {'✅ Authenticated' if status['spotify'] else '❌ Not authenticated'}", 
                         "green" if status['spotify'] else "red")
            print_colored(f"YouTube Music: {'✅ Authenticated' if status['youtube'] else '❌ Not authenticated'}", 
                         "green" if status['youtube'] else "red")
            
            if not status['spotify'] or not status['youtube']:
                print_colored(f"\n💡 To get authentication tokens, visit: {AUTH_WEBSITE_URL}", "blue")
                print_colored("Then use 'migrate-playlist set-token' to save your tokens.", "blue")
        
        elif args.auth_command == "clear":
            if args.spotify:
                clear_auth("spotify")
            elif args.youtube:
                clear_auth("youtube")
            else:
                clear_auth()  # Clear both
        
        elif args.auth_command == "setup":
            print_colored(get_auth_instructions(), "blue")
            
            # Ask if user wants to open the website
            try:
                open_website = input("\n🌐 Would you like to open the authentication website now? (y/n): ").lower().strip()
                if open_website in ['y', 'yes']:
                    print_colored("🚀 Opening authentication website...", "blue")
                    webbrowser.open(AUTH_WEBSITE_URL)
            except KeyboardInterrupt:
                print_colored("\n👋 Setup cancelled.", "yellow")
        else:
            auth_parser.print_help()
    
    elif args.command == "set-token":
        if args.spotify:
            save_spotify_token(args.token)
        elif args.youtube:
            if save_youtube_token(args.token):
                print_colored("🎉 All set! You can now migrate playlists.", "green")
        else:
            print_colored("❌ Please specify --spotify or --youtube", "red")
            
    elif args.command == "migrate":
        setup_logging(args.log)

        # Check authentication before proceeding
        status = check_auth_status()
        missing_auth = []
        
        if args.source == "spotify" and not status['spotify']:
            missing_auth.append("Spotify")
        elif args.source == "youtube" and not status['youtube']:
            missing_auth.append("YouTube Music")
            
        if args.destination == "spotify" and not status['spotify']:
            missing_auth.append("Spotify")
        elif args.destination == "youtube" and not status['youtube']:
            missing_auth.append("YouTube Music")
        
        # Remove duplicates
        missing_auth = list(set(missing_auth))
        
        if missing_auth:
            print_colored(f"❌ Missing authentication for: {', '.join(missing_auth)}", "red")
            print_colored(f"\n🔗 Please visit {AUTH_WEBSITE_URL} to get your tokens.", "blue")
            print_colored("Then use 'migrate-playlist set-token' to save them.", "blue")
            print_colored("\nExample:", "blue")
            print_colored("  migrate-playlist set-token --spotify --token 'YOUR_SPOTIFY_TOKEN'", "yellow")
            print_colored("  migrate-playlist set-token --youtube --token 'YOUR_YOUTUBE_TOKEN'", "yellow")
            return

        if args.source == "spotify" and args.destination == "youtube":
            print_colored("🚀 Migrating from Spotify to YouTube Music...", "blue")
            
            try:
                spotify_client = SpotifyClient()
                youtube_client = YouTubeClient()

                if not spotify_client.is_authenticated():
                    print_colored("🔑 Spotify authentication failed. Please check your token.", "red")
                    print_colored(f"💡 Get a new token from: {AUTH_WEBSITE_URL}", "blue")
                    return

                if args.playlist == "liked_songs":
                    print_colored("❤️ Fetching Spotify Liked Songs...", "blue")
                    tracks = spotify_client.get_liked_songs()
                else:
                    print_colored(f"🎧 Fetching Spotify Playlist: {args.playlist}", "blue")
                    tracks = spotify_client.get_playlist_tracks(args.playlist)

                playlist_name = args.name or "My Spotify Playlist"
                print_colored(f"🎵 Migrating {len(tracks)} tracks to YouTube Music...", "blue")
                tracks = youtube_client.create_playlist(playlist_name, tracks)  # Update tracks with found status
            
            except Exception as e:
                print_colored(f"🚨 Error during migration: {str(e)}", "red")
                print_colored(f"💡 If this is an authentication error, get new tokens from: {AUTH_WEBSITE_URL}", "blue")
                return

        elif args.source == "youtube" and args.destination == "spotify":
            print_colored("🚀 Migrating from YouTube Music to Spotify...", "blue")
            
            try:
                youtube_client = YouTubeClient()
                spotify_client = SpotifyClient()

                if not spotify_client.is_authenticated():
                    print_colored("🔑 Spotify authentication failed. Please check your token.", "red")
                    print_colored(f"💡 Get a new token from: {AUTH_WEBSITE_URL}", "blue")
                    return

                print_colored(f"🎧 Fetching YouTube Music Playlist: {args.playlist}", "blue")
                tracks = youtube_client.get_playlist_tracks(args.playlist)

                playlist_name = args.name or "My YouTube Playlist"
                print_colored(f"🎵 Migrating {len(tracks)} tracks to Spotify...", "blue")
                tracks = spotify_client.create_playlist(playlist_name, tracks)  # Update tracks with found status
            
            except Exception as e:
                print_colored(f"🚨 Error during migration: {str(e)}", "red")
                print_colored(f"💡 If this is an authentication error, get new tokens from: {AUTH_WEBSITE_URL}", "blue")
                return
                
        else:
            print_colored("🚨 Invalid source or destination platform.", "red")
            return

        if args.stats:
            found_tracks = [t for t in tracks if t.get('found', False)]
            
            print_colored("\n📊 Migration Statistics:", "blue")
            print_colored(f"✅ Total Songs: {len(tracks)}", "green")
            print_colored(f"✅ Successfully Migrated: {len(found_tracks)} ({round(len(found_tracks)/len(tracks)*100, 1)}%)", "green")
            print_colored(f"❌ Not Found: {len(tracks) - len(found_tracks)} ({round((len(tracks) - len(found_tracks))/len(tracks)*100, 1)}%)", "red")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()