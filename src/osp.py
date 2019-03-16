import os
import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

from pprint import pprint


def get_user_spotify_playlists(client, user):
    playlists = list()
    response = client.user_playlists(user=user)
    for pl in response['items']:
        if 'name' in pl:
            playlists.append(pl)

    return playlists


def get_playlist_by_name(playlist_name, playlists):
    for pl in playlists:
        if pl['name'] == playlist_name:
            return pl
    return None


# Environment variables
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_USERNAME = os.environ['SPOTIFY_USERNAME']

# Path variables
base_path = os.getcwd()
playlists_path = '/playlists/'

# Spotify client setup
token = util.prompt_for_user_token(
    username=SPOTIFY_USERNAME,
    scope='playlist-modify-public playlist-modify-private')
sp = spotipy.Spotify(auth=token)

user_playlists_info = get_user_spotify_playlists(sp, SPOTIFY_USERNAME)
user_playlists_names = [pl['name'] for pl in user_playlists_info]
playlist_base_name = 'OSP-'
playlist_files = os.listdir(f'{base_path}{playlists_path}')

for playlist_file in playlist_files:
    file = open(f'{base_path}{playlists_path}{playlist_file}')
    playlist_data = yaml.load(file)
    playlist_name = list(playlist_data)[0]
    playlist_song_ids = [s['uri'] for s in playlist_data[playlist_name]['songs']]
    playlist = get_playlist_by_name(playlist_name, user_playlists_info)
    if not playlist:
        # Create new playlist and get playlist id
        playlist = sp.user_playlist_create(SPOTIFY_USERNAME, playlist_name)
    sp.user_playlist_add_tracks(SPOTIFY_USERNAME, playlist['id'], playlist_song_ids)

