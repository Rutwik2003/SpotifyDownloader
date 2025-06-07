# Spotify Playlist Downloader

A Python-based tool that allows you to download songs from your Spotify playlists and save them as MP3 files with proper metadata.

## Features

- Download entire Spotify playlists
- Automatic metadata tagging (title, artist, album)
- Progress bar for download tracking
- Error logging and retry mechanism
- Converts downloaded files to MP3 format
- Skips already downloaded songs
- Detailed logging system

## Prerequisites

Before using this tool, make sure you have the following installed:

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - spotipy
  - mutagen
  - pydub
  - yt-dlp
  - tqdm

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. You'll need to set up a Spotify Developer account and create an application to get your credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Get your Client ID and Client Secret
   - Add `http://localhost:8888/callback` as a Redirect URI in your app settings

2. Update the following credentials in `spotify.py`:
   - `client_id`
   - `client_secret`

## Usage

1. Get your Spotify playlist ID from the playlist URL:
   - Open your playlist in Spotify
   - The ID is the string of characters after `/playlist/` in the URL
   - Example: `https://open.spotify.com/playlist/0PjnoLrtvie5lLjGVvWvWN` → ID: `0PjnoLrtvie5lLjGVvWvWN`

2. Run the script:
```bash
python spotify.py
```

By default, songs will be downloaded to a `./songs` directory in the same location as the script.

## File Structure

- `spotify.py`: Main script file
- `download_log.txt`: Log file containing successful downloads
- `not_downloaded_songs.txt`: Log file containing failed downloads
- `./songs/`: Directory where downloaded MP3 files are stored

## How It Works

1. The script authenticates with Spotify using OAuth2
2. Retrieves all tracks from the specified playlist
3. For each track:
   - Searches for the song on YouTube
   - Downloads the audio
   - Converts to MP3 format
   - Adds metadata (title, artist, album)
   - Saves to the output directory

## Error Handling

- Failed downloads are logged in `not_downloaded_songs.txt`
- The script includes a retry mechanism (3 attempts) for failed downloads
- Already existing files are skipped to prevent duplicate downloads

## Logging

The script maintains two types of logs:
1. `download_log.txt`: Contains information about successful downloads and skipped files
2. `not_downloaded_songs.txt`: Contains information about failed downloads

## Notes

- This tool is for personal use only
- Please respect copyright laws and Spotify's terms of service
- Download speeds may vary depending on your internet connection
- The quality of downloaded audio depends on the source YouTube video

## License

This project is for educational purposes only. Use at your own risk.

## Disclaimer

This tool is not affiliated with Spotify or YouTube. Use it responsibly and in accordance with their terms of service. 