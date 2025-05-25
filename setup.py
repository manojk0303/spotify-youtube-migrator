from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="spotify-youtube-migrator",
    version="1.1.1",
    author="Manojkumar K",
    author_email="manojk030303@gmail.com",
    description="A Python package to migrate playlists between Spotify and YouTube Music.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manojk0303/spotify-youtube-migrator",
    packages=find_packages(),
    install_requires=[
        "spotipy",
        "ytmusicapi",
        "colorama",
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.2.0"
    ],
    entry_points={
        "console_scripts": [
            "migrate-playlist=spotify_youtube_migrator.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)