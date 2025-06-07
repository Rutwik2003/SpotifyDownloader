import os
import logging
from datetime import datetime
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, ID3NoHeaderError
from pydub import AudioSegment
import yt_dlp
from tqdm import tqdm

# Setup logging
logging.basicConfig(filename='download_log.txt', level=logging.INFO, 
                    format='%(asctime)s [%(levelname)s] %(message)s')
error_log = 'not_downloaded_songs.txt'

def log_error(message):
    with open(error_log, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()} [ERROR] {message}\n")

def add_metadata(file_path, title, artist, album):
    try:
        audio = EasyID3(file_path)
    except ID3NoHeaderError:
        audio = ID3()
        audio.add(TIT2(encoding=3, text=title))
        audio.add(TPE1(encoding=3, text=artist))
        audio.add(TALB(encoding=3, text=album))
        audio.save(file_path)
        audio = EasyID3(file_path)

    audio['title'] = title
    audio['artist'] = artist
    audio['album'] = album
    audio.save()

def convert_to_mp3(mp4_path, mp3_path):
    audio = AudioSegment.from_file(mp4_path)
    audio.export(mp3_path, format="mp3")

def download_track(track_name, artist_name, album_name, output_path='./songs', retries=3):
    query = f"{track_name} {artist_name} lyrics"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'outtmpl': os.path.join(output_path, f'{track_name}.mp4'),
        'no_warnings': True,
        'ignoreerrors': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
        if search_results['entries']:
            video = search_results['entries'][0]
            ydl.download([video['webpage_url']])
            
            # Convert to mp3
            output_file = os.path.join(output_path, f"{track_name}.mp4")
            mp3_file = output_file.replace('.mp4', '.mp3')
            convert_to_mp3(output_file, mp3_file)
            os.remove(output_file)
    
            # Add metadata
            add_metadata(mp3_file, track_name, artist_name, album_name)
            logging.info(f"Completed download: {mp3_file}")
        else:
            if retries > 0:
                logging.warning(f"Retrying download for {track_name} by {artist_name}")
                download_track(track_name, artist_name, album_name, output_path, retries - 1)
            else:
                log_error(f"Failed to download {track_name} by {artist_name}")
                logging.error(f"Failed to download {track_name} by {artist_name}")

def download_playlist(playlist_id, output_path='./songs'):
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id='', # Enter your client id here
        client_secret='', # Enter your client secret here
        redirect_uri='http://localhost:8888/callback',
        scope='playlist-read-private'
    ))
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    total_tracks = len(tracks)

    with tqdm(total=total_tracks, desc="Downloading tracks", unit="track") as pbar:
        for item in tracks:
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
            file_path = os.path.join(output_path, f"{track_name}.mp3")

            if os.path.exists(file_path):
                logging.info(f"Skipped download (file already exists): {file_path}")
                pbar.update(1)
            else:
                logging.info(f"Starting download: {track_name} by {artist_name}")
                try:
                    download_track(track_name, artist_name, album_name, output_path)
                    pbar.update(1)
                except Exception as e:
                    log_error(f"Failed to download {track_name} by {artist_name}: {str(e)}")
                    logging.error(f"Failed to download {track_name} by {artist_name}: {str(e)}")
                    pbar.update(1)

if __name__ == "__main__":
    playlist_id = '0PjnoLrtvie5lLjGVvWvWN'  # Replace with your Spotify playlist ID
    output_path = './songs'
    download_playlist(playlist_id, output_path)
