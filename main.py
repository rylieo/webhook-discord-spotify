import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import time
import os

# === Konfigurasi ===
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1445780119753981984/wLeKT_LXyCPTxOckuC30SQUQ5Cb6XKiJuIEJlGmHkBB8_BzLAjJUWLGEwKw_SY7eujq-"
SPOTIFY_CLIENT_ID = "55ff3ae67f3d4ea09606d19bbf7dece9"
SPOTIFY_CLIENT_SECRET = "4578d02141f64298997af426393bc7af"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"

# Scope untuk baca lagu yang sedang diputar
SCOPE = "user-read-currently-playing user-read-playback-state"

# Cache token agar tidak login berulang-ulang
CACHE_PATH = ".spotify_cache"

# Inisialisasi Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE_PATH,
    open_browser=False  # Biar tidak buka browser tiap kali
))

def get_current_track():
    try:
        current = sp.currently_playing()
        if current and current['is_playing']:
            track = current['item']
            artist = ", ".join([a['name'] for a in track['artists']])
            title = track['name']
            album = track['album']['name']
            album_url = track['album']['external_urls']['spotify']
            album_art = track['album']['images'][0]['url'] if track['album']['images'] else None
            track_url = track['external_urls']['spotify']

            # Progress & durasi (opsional, untuk embed)
            progress_ms = current['progress_ms']
            duration_ms = track['duration_ms']

            return {
                "title": title,
                "artist": artist,
                "album": album,
                "album_url": album_url,
                "artwork": album_art,
                "url": track_url,
                "progress_ms": progress_ms,
                "duration_ms": duration_ms,
                "is_playing": True
            }
        else:
            return None
    except Exception as e:
        print(f"[ERROR] Gagal ambil data Spotify: {e}")
        return None

def send_to_discord(track_info):
    if not track_info:
        print("Tidak ada lagu yang sedang diputar.")
        return

    embed = {
        "title": f"{track_info['artist']} - {track_info['title']}",
        "description": f"Album: [{track_info['album']}]({track_info['album_url']})",
        "url": track_info["url"],
        "color": 0x1DB954               # Spotify green
    }

    # Artwork
    if track_info.get("artwork"):
        embed["thumbnail"] = {"url": track_info["artwork"]}

    data = {
        "username": "Now Playing",
        "embeds": [embed]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL.strip(), json=data)
        if response.status_code == 204:
            print(f"Terkirim: {track_info['title']} - {track_info['artist']}")
        else:
            print(f"Gagal kirim ke Discord: {response.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")


# === Loop utama ===
if __name__ == "__main__":
    last_track_id = None

    print("Menunggu lagu diputar di Spotify...")
    while True:
        track = get_current_track()

        if track:
            current_track_id = track['url']  # Gunakan URL sebagai ID unik
            if current_track_id != last_track_id:
                print("Lagu baru terdeteksi!")
                send_to_discord(track)
                last_track_id = current_track_id
        else:
            last_track_id = None  # Reset jika berhenti

        time.sleep(10)  # Cek tiap 10 detik