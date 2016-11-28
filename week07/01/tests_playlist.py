import unittest
from playlist import Playlist
from song import Song

class PlaylistTests(unittest.TestCase):
    def test_init(self):
        new_pl = Playlist(name="Code.json", repeat=True, shuffle=True)
        self.assertEqual(new_pl.name, 'Code.json')
        self.assertEqual(new_pl.repeat, True)
        self.assertEqual(new_pl.shuffle, True)

        new_pl = Playlist(name="Code.json")
        self.assertEqual(new_pl.name, 'Code.json')
        self.assertEqual(new_pl.repeat, False)
        self.assertEqual(new_pl.shuffle, False)

    def test_total_length(self):
        new_pl = Playlist(name="Code.json", repeat=True, shuffle=True)
        new_pl.add_songs([Song('Title', 'Artist', 'Album', '0:0:33'), Song('Title', 'Artist', 'Album', '10:0:33'),
                          Song('Title', 'Artist', 'Album', '0:3:1')])
        self.assertEqual(new_pl.total_length(), '10:04:07')

    def test_artists(self):
        new_pl = Playlist(name="Code.json", repeat=True, shuffle=True)
        new_pl.add_songs([Song('Its my life', 'Bon Jovi', 'Album', '0:0:33'), Song('Title', 'Bon Jovi', 'Album', '10:0:33'),
                          Song('Lelee', 'Azis', 'Album', '0:3:1')])
        artists_histogram = new_pl.get_artists()
        self.assertEqual(len(artists_histogram.keys()), 2)
        self.assertEqual(artists_histogram, {'Azis': 1, 'Bon Jovi': 2})

    def test_next_song(self):
        first_song = Song('Its my life', 'Bon Jovi', 'Album', '0:0:33')
        second_song = Song('Title', 'Bon Jovi', 'Album', '10:0:33')
        third_song = Song('Lelee', 'Azis', 'Album', '0:3:1')
        new_pl = Playlist(name="Code.json", repeat=True, shuffle=False)
        new_pl.add_songs([first_song, second_song, third_song])
        self.assertEqual(first_song, new_pl.next_song())
        self.assertEqual(second_song, new_pl.next_song())
        self.assertEqual(third_song, new_pl.next_song())
        self.assertEqual(first_song, new_pl.next_song())

    def test_save_load_playlist(self):
        first_song = Song('Its my life', 'Bon Jovi', 'Album', '0:0:33')
        second_song = Song('Title', 'Bon Jovi', 'Album', '10:0:33')
        third_song = Song('Lelee', 'Azis', 'Album', '0:3:1')
        new_pl = Playlist(name="Code")
        new_pl.add_songs([first_song, second_song, third_song])

        new_pl.save()
        loaded_playlist = Playlist.load("Code.json")
        # Assert they have the same songs
        self.assertEqual(sorted(new_pl.songs, key=lambda song: song.title),
                         sorted(loaded_playlist.songs, key=lambda song: song.title))
        self.assertEqual(new_pl.name, loaded_playlist.name)


if __name__ == '__main__':
    unittest.main()