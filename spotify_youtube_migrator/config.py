import json
import os
from spotify_youtube_migrator.utils import print_colored

CONFIG_FILE = "config.json"

def set_credentials(platform):
    if platform == "spotify":
        client_id = input("Enter your Spotify Client ID: ")
        client_secret = input("Enter your Spotify Client Secret: ")
        credentials = {"spotify": {"client_id": client_id, "client_secret": client_secret}}
    elif platform == "youtube":
        print_colored("🔑 Follow the instructions to generate browser.json for YouTube Music.", "blue")
        print_colored("1. Run 'ytmusicapi browser' in your terminal.", "blue")
        print_colored("2. Log in to YouTube Music and copy the required headers.", "blue")
        print_colored("3. Paste them into the terminal when prompted.", "blue")
        return
    else:
        print_colored("🚨 Invalid platform. Use 'spotify' or 'youtube'.", "red")
        return

    with open(CONFIG_FILE, "w") as f:
        json.dump(credentials, f)
    print_colored(f"✅ {platform.capitalize()} credentials saved successfully!", "green")

def get_credentials(platform):
    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE, "r") as f:
        credentials = json.load(f)
        return credentials.get(platform)