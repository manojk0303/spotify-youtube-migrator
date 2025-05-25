# Spotify-YouTube Playlist Migrator 🎵

A Python package to easily migrate playlists between Spotify and YouTube Music with streamlined token-based authentication.

---

## Features ✨

- **Simple Token Authentication** - Get your tokens from our web interface with just a few clicks
- Migrate Spotify playlists to YouTube Music
- Migrate YouTube Music playlists to Spotify
- Migrate Spotify Liked Songs to YouTube Music
- Detailed logging and migration statistics
- Secure local token storage

---

## Installation 🛠️

Install the package via pip:
```bash
pip install spotify-youtube-migrator
```

---

## Quick Start 🚀

### Step 1: Get Your Authentication Tokens

Before migrating playlists, you need to obtain authentication tokens:

```bash
migrate-playlist auth setup
```

This will:
1. Display setup instructions
2. Optionally open the authentication website: `https://youtube-spotify-token-finder.vercel.app`

### Step 2: Authenticate with Both Services

Visit the authentication website and:
1. Click **"Login with Spotify"** and authorize the application
2. Click **"Login with YouTube Music"** and authorize the application  
3. Copy the generated access tokens (just the token strings, not the full JSON)

### Step 3: Save Your Tokens

Set your Spotify token:
```bash
migrate-playlist set-token --spotify --token "YOUR_SPOTIFY_ACCESS_TOKEN"
```

Set your YouTube Music token:
```bash
migrate-playlist set-token --youtube --token "YOUR_YOUTUBE_ACCESS_TOKEN"
```

### Step 4: Start Migrating!

You're now ready to migrate playlists between platforms.

---

## Usage Examples 📖

### Check Authentication Status

```bash
migrate-playlist auth status
```

### Migrate Spotify Playlist to YouTube Music

```bash
migrate-playlist migrate --source spotify --destination youtube --playlist <playlist_url> --name "My Playlist"
```

### Migrate Spotify Liked Songs to YouTube Music

```bash
migrate-playlist migrate --source spotify --destination youtube --playlist liked_songs --name "My Liked Songs"
```

### Migrate YouTube Music Playlist to Spotify

```bash
migrate-playlist migrate --source youtube --destination spotify --playlist <playlist_url> --name "My Playlist"
```

### View Migration Statistics

Add the `--stats` flag to see detailed migration results:

```bash
migrate-playlist migrate --source spotify --destination youtube --playlist <playlist_url> --stats
```

Example output:
```
📊 Migration Statistics:
✅ Total Songs: 25
✅ Successfully Migrated: 23 (92.0%)
❌ Not Found: 2 (8.0%)
```

---

## Authentication Management 🔐

### Check Status
```bash
migrate-playlist auth status
```

### Clear All Authentication Data
```bash
migrate-playlist auth clear
```

### Clear Specific Platform Authentication
```bash
migrate-playlist auth clear --spotify
migrate-playlist auth clear --youtube
```

### Get Setup Instructions Again
```bash
migrate-playlist auth setup
```

---

## Commands Reference 📜

### Migration Commands

| Command | Description |
|---------|-------------|
| `migrate --source <platform>` | Source platform (`spotify` or `youtube`) |
| `--destination <platform>` | Destination platform (`spotify` or `youtube`) |
| `--playlist <url_or_special>` | Playlist URL or `liked_songs` for Spotify Liked Songs |
| `--name <playlist_name>` | Custom name for the new playlist (optional) |
| `--log` | Enable detailed logging |
| `--stats` | Display migration statistics |

### Authentication Commands

| Command | Description |
|---------|-------------|
| `auth status` | Check authentication status for both services |
| `auth setup` | Get setup instructions and optionally open auth website |
| `auth clear` | Clear all saved authentication tokens |
| `auth clear --spotify` | Clear only Spotify authentication |
| `auth clear --youtube` | Clear only YouTube Music authentication |

### Token Management Commands

| Command | Description |
|---------|-------------|
| `set-token --spotify --token <token>` | Save Spotify access token |
| `set-token --youtube --token <token>` | Save YouTube Music access token |

---

## Authentication Flow Details 🔐

1. **Visit Authentication Website**: Go to `https://youtube-spotify-token-finder.vercel.app`

2. **Authorize Spotify**: 
   - Click "Login with Spotify"
   - Grant permissions to the application
   - Copy the generated access token

3. **Authorize YouTube Music**:
   - Click "Login with YouTube Music" 
   - Grant permissions to the application
   - Copy the generated access token

4. **Save Tokens Locally**:
   - Use `migrate-playlist set-token` commands to store tokens securely on your device
   - Tokens are stored in `~/.spotify-youtube-migrator/` directory

5. **Start Migrating**:
   - Tokens are automatically used for all migration operations
   - No need to re-authenticate unless tokens expire

---

## Troubleshooting 🔧

### Token Expired or Invalid

If you see authentication errors:
```bash
# Check current status
migrate-playlist auth status

# Clear old tokens
migrate-playlist auth clear

# Get new tokens from the website
migrate-playlist auth setup
```

### Migration Issues

- **Songs not found**: Some songs may not be available on the destination platform
- **Rate limiting**: The tool automatically handles API rate limits
- **Playlist size**: Large playlists are processed in batches

### Common Error Messages

- **"No Spotify/YouTube token found"**: Run the token setup process
- **"Token expired"**: Get fresh tokens from the authentication website
- **"Playlist not found"**: Check that the playlist URL is correct and public

---

## Technical Details 🔧

### Token Storage
- Tokens are stored locally in `~/.spotify-youtube-migrator/`
- Files: `spotify_token.json` and `youtube_auth.json`
- Tokens are never shared or transmitted except to the respective APIs

### Supported Playlist Sources
- **Spotify**: Public playlists, private playlists (if you own them), Liked Songs
- **YouTube Music**: Public playlists, private playlists (if you own them)

### Migration Process
1. Fetch tracks from source playlist
2. Search for each track on destination platform
3. Create new playlist on destination
4. Add found tracks to the new playlist
5. Display statistics and missing tracks

---

## Contributing 🤝

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support 💬

If you encounter any issues or have questions:

- **GitHub Issues**: [Open an issue](https://github.com/manojk0303/spotify-youtube-migrator/issues)
- **Authentication Problems**: Make sure to get fresh tokens from the auth website
- **Migration Issues**: Include the error message and command you used

---

## Changelog 🔄

### v1.1.0
- Simplified authentication with web-based token generation
- Improved token management and validation
- Better error handling and user guidance
- Enhanced CLI with auth management commands

### v1.0.0
- Initial release with basic migration functionality