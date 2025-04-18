# Spotify-YouTube Playlist Migrator 🎵

A Python package to migrate playlists between Spotify and YouTube Music.

---

## Features ✨
- Migrate Spotify playlists to YouTube Music.
- Migrate YouTube Music playlists to Spotify.
- Migrate Spotify Liked Songs to YouTube Music.
- Set credentials interactively.
- Detailed logging and migration statistics.

---

## Installation 🛠️

1. Install the package via pip:
   ```bash
   pip install spotify-youtube-migrator
   ```

2. Set up your credentials:
   ```bash
   migrate-playlist set-creds --spotify
   migrate-playlist set-creds --youtube
   ```

---

## Usage 🚀

### Migrate Spotify Playlist to YouTube Music
```bash
migrate-playlist migrate --source spotify --destination youtube --playlist <playlist_url_or_liked_songs> --name "My Playlist"
```

### Migrate YouTube Music Playlist to Spotify
```bash
migrate-playlist migrate --source youtube --destination spotify --playlist <playlist_url> --name "My Playlist"
```

### Enable Logging and Statistics
```bash
migrate-playlist migrate --source spotify --destination youtube --playlist liked_songs --log --stats
```

---

## Commands 📜

| Command                          | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `set-creds --spotify`            | Set Spotify credentials interactively.                                      |
| `set-creds --youtube`            | Set up YouTube Music authentication.                                        |
| `migrate --source <source>`      | Migrate playlists between platforms.                                        |
| `--destination <destination>`    | Specify the destination platform.                                           |
| `--playlist <url_or_liked_songs>`| Provide the playlist URL or use `liked_songs` for Spotify Liked Songs.      |
| `--name <playlist_name>`         | Specify a custom name for the new playlist.                                 |
| `--log`                          | Enable detailed logging.                                                    |
| `--stats`                        | Display migration statistics.                                               |

---

## Contributing 🤝

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support 💬

If you encounter any issues or have questions, please open an issue on [GitHub](https://github.com/manojk0303/spotify-youtube-migrator/issues).