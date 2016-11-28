from song import Song
import unittest
from datetime import timedelta
from copy import deepcopy

class SongTests(unittest.TestCase):
    def setUp(self):
        self.given_title = 'No Rest For The Wicked'
        self.given_artist = 'E-Dubble'
        self.given_album = 'TTR'
        self.given_length_str = '3:33:33'
        self.song = Song(self.given_title, self.given_artist, self.given_album, self.given_length_str)

    def test_init(self):
        self.assertEqual(self.song.title, self.given_title)
        self.assertEqual(self.song.artist, self.given_artist)
        self.assertEqual(self.song.album, self.given_album)
        self.assertEqual(self.song.length, self.given_length_str)
        self.assertEqual(self.song.timedelta_length, timedelta(hours=3, minutes=33, seconds=33))
        self.assertEqual(str(self.song), '{artist} - {title} from {album} - {length}'.format(
            artist=self.given_artist, title=self.given_title, album=self.given_album,
            length=self.given_length_str
        ))

    def test_comparison(self):
        new_song = Song('Some', 'Some', 'Some', '3:33:33')
        self.assertNotEqual(self.song, new_song)

        same_song = deepcopy(self.song)
        self.assertEqual(self.song, same_song)

if __name__ == '__main__':
    unittest.main()