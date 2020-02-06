import os
import yaml

from .spotify_init import spotify


# Path variables
base_path = os.getcwd()
playlists_path = '/playlists/'


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


def get_playlist_songs(client, user, playlist_id):
    response = client.user_playlist(
        user,
        playlist_id,
        fields='tracks')
    if 'items' in response['tracks']:
        songs = [item['track']
                     for item in response['tracks']['items']]
    else:
        songs = list()
    return songs


def get_songs_to_add(client, user, playlist_id, song_uris):
    playlist_song_uris = [song['uri']
                          for song in get_playlist_songs(client, user, playlist_id)]
    return list(set(song_uris) - set(playlist_song_uris))


def get_songs_to_delete(client, user, playlist_id, song_uris):
    playlist_song_uris = [song['uri']
                          for song in get_playlist_songs(client, user, playlist_id)]
    return list(set(playlist_song_uris) ^ set(song_uris))


def add_songs_to_playlist(client, user, playlist_id, songs):
    if len(songs) > 0:
        client.user_playlist_add_tracks(
            user,
            playlist_id,
            songs)


def remove_songs_from_playlist(client, user, playlist_id, songs):
    if len(songs) > 0:
        client.user_playlist_remove_all_occurrences_of_tracks(
            user,
            playlist_id,
            songs)


if __name__ == '__main__':
    # Spotify client setup
    OSP_USERNAME = os.environ['OSP_USERNAME']
    sp = spotify(scope='playlist-modify-public')
    user_playlists_info = get_user_spotify_playlists(sp, OSP_USERNAME)
    user_playlists_names = [pl['name'] for pl in user_playlists_info]
    playlist_files = os.listdir(f'{base_path}{playlists_path}')

    for playlist_file in playlist_files:
        file = open(f'{base_path}{playlists_path}{playlist_file}')
        playlist_data = yaml.load(file)
        playlist_name = list(playlist_data)[0]
        playlist = get_playlist_by_name(playlist_name, user_playlists_info)

        if not playlist:
            # Create new playlist and get playlist id
            playlist = sp.user_playlist_create(OSP_USERNAME, playlist_name)

        playlist_song_uris = [s['uri'] for s in playlist_data[playlist_name]['songs']]
        songs_to_add = get_songs_to_add(sp, OSP_USERNAME, playlist['id'], playlist_song_uris)
        add_songs_to_playlist(sp, OSP_USERNAME, playlist['id'], songs_to_add)
        songs_to_delete = get_songs_to_delete(sp, OSP_USERNAME, playlist['id'], playlist_song_uris)

        remove_songs_from_playlist(sp, OSP_USERNAME, playlist['id'], songs_to_delete)

        # Report actions
        print(f'Added {len(songs_to_add)} songs: {songs_to_add}')
        print(f'Removed {len(songs_to_delete)} songs: {songs_to_delete}')
