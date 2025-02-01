from setuptools import setup, find_packages

setup(
    name="spotify_youtube_migrator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "spotipy",
        "ytmusicapi",
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "migrate-playlist=spotify_youtube_migrator.cli:main",
        ],
    },
)