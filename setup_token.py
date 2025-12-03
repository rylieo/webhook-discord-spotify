# setup_token.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Konfigurasi (sama seperti di now_playing_to_discord.py)
SPOTIFY_CLIENT_ID = "55ff3ae67f3d4ea09606d19bbf7dece9"
SPOTIFY_CLIENT_SECRET = "4578d02141f64298997af426393bc7af"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-read-currently-playing user-read-playback-state"
CACHE_PATH = ".spotify_cache"

# Inisialisasi auth_manager
auth_manager = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE_PATH,
    open_browser=True  # ← biarkan True agar buka browser
)

print("Membuka browser untuk otorisasi Spotify...")
print("Silakan klik 'Setuju' di halaman yang terbuka.")

# Ambil token (akan buka browser otomatis)
token_info = auth_manager.get_access_token(as_dict=True)

if token_info:
    print("Token berhasil disimpan ke:", CACHE_PATH)
    print("SELESAI! Sekarang tutup browser dan jalankan:")
    print("python now_playing_to_discord.py")
else:
    print("Gagal mendapatkan token.")