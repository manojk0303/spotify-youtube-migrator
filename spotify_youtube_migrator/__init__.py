"""
spotify_youtube_migrator

A Python package to migrate playlists between Spotify and YouTube Music.
"""

__version__ = "1.0.0"
__author__ = "Manojkumar K"
__email__ = "manojk030303@gmail.com"

# Import key components for easier access
from .cli import main
from .spotify import SpotifyClient
from .youtube import YouTubeClient

# Package-level documentation
__doc__ = """
Spotify-YouTube Playlist Migrator 🎵

This package allows you to migrate playlists between Spotify and YouTube Music.
You can migrate:
- Spotify playlists to YouTube Music.
- YouTube Music playlists to Spotify.
- Spotify Liked Songs to YouTube Music.

Usage:
    migrate-playlist set-creds --spotify
    migrate-playlist migrate --source spotify --destination youtube --playlist <playlist_url_or_liked_songs>
"""