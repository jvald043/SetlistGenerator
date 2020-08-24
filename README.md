# SetlistGenerator
This was created to automate the process of gathering songs from past setlists of an artist's concert you will attend in the future.

Retrieves songs last played at venues from SetlistFm and creates a playlist in Spotify.

Currently running the Python Script will prompt the user to type the band name

## Notes:
User will need to create an auth_key.py file with the following variables:

#### Client User ID is taken from Spotify User ID
CLIENT_USER_ID = ''

#### MBrains token and Setlist ID taken from respective sites
MBRAINZ_TOKEN = '' 

SETLIST_FM_ID = ''

#### Client Token and user ID taken from Spotify Developers
SPOTIPY_CLIENT_ID = ''

SPOTIPY_CLIENT_SECRET = ''

SPOTIPY_REDIRECT_URI = ''

