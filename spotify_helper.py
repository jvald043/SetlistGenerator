import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials


def spotify_init():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=config.SPOTIPY_CLIENT_ID,
        client_secret=config.SPOTIPY_CLIENT_SECRET, )

    spotify_auth_manager = SpotifyOAuth(
        client_id=config.SPOTIPY_CLIENT_ID,
        client_secret=config.SPOTIPY_CLIENT_SECRET,
        scope='playlist-modify-public',
        redirect_uri=config.SPOTIPY_REDIRECT_URI,
        username=config.CLIENT_USER_ID
    )

    return spotipy.Spotify(
        client_credentials_manager=client_credentials_manager,
        auth_manager=spotify_auth_manager)
