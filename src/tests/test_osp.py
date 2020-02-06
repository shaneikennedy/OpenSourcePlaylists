from unittest import TestCase
from src.osp import get_playlist_by_name

class OSPTests(TestCase):
    def test_GetPlaylistByName_Always_ReturnTrue(self):
        playlists = [{'name': 'playlist_1'}, {'name': 'playlist_2'}]

        playlist_name = get_playlist_by_name('playlist_1', playlists)

        self.assertIsNotNone(playlist_name)
        self.assertEqual('playlist_1', playlist_name['name'])
