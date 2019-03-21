import sys
import yaml
import spotipy
import spotipy.util as util
from osp import (
    get_playlist_by_name,
    get_playlist_songs,
    get_user_spotify_playlists,
)


class Song(yaml.YAMLObject):
    def __init__(self, name, artists, uri):
        self.name = name
        self.artists = ', '.join(artists)
        self.uri = uri

    def __repr__(self):
        return f'name: {self.name}, artists: {self.artists}, uri: {self.uri}'


if __name__ == '__main__':
    username = sys.argv[1]
    playlist_name = sys.argv[2]
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)
    sp = spotipy.Spotify(auth=token)
    playlists = get_user_spotify_playlists(sp, username)
    playlist = get_playlist_by_name(playlist_name, playlists)
    playlist_songs = get_playlist_songs(sp, playlist['id'])

    songs = list()
    for playlist_song in playlist_songs:
        song_artists = [a['name'] for a in playlist_song['artists']]
        song = {
            'name': playlist_song['name'],
            'artists': ', '.join(song_artists),
            'uri': playlist_song['uri'],
        }
        songs.append(song)

    stream = open(f'{playlist_name}.yml', 'w')
    yaml.dump(
        data={playlist_name: {'songs': songs}},
        default_flow_style=False,
        stream=stream)

