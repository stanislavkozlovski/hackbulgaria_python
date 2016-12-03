import unittest
import os
from datetime import timedelta
from music_crawler import MusicCrawler


class MusicCrawlerTests(unittest.TestCase):

    def setUp(self):
        self.songs_path = './music_crawler_test'

    def test_crawl(self):
        """ Crawl the directories and test if the songs list has the expected mp3 files """
        crawler = MusicCrawler(self.songs_path)
        # our songs list contain the absolute paths to the songs
        drake_song = crawler.songs[0]  # our path has only one music file
        self.assertTrue(drake_song.endswith('Drake - Worst Behavior.mp3'))

    def test_generate_playlist(self):
        crawler = MusicCrawler(self.songs_path)
        # should have only two identical songs from different formats - .ogg & .mp3
        playlist = crawler.generate_playlist()
        song_count = 2
        for idx in range(song_count):
            with self.subTest(song_idx=idx):
                song_DRAKE_WORST_BEHAVIOUR = playlist.next_song()
                self.assertEqual(song_DRAKE_WORST_BEHAVIOUR.title, 'Worst Behavior')
                self.assertEqual(song_DRAKE_WORST_BEHAVIOUR.artist, 'Drake')
                self.assertEqual(song_DRAKE_WORST_BEHAVIOUR.album, 'Nothing Was The Same')
                self.assertEqual(song_DRAKE_WORST_BEHAVIOUR.length, '4:37')
                self.assertEqual(song_DRAKE_WORST_BEHAVIOUR.timedelta_length, timedelta(hours=0, minutes=4, seconds=37))
                self.assertEqual(str(song_DRAKE_WORST_BEHAVIOUR), 'Drake - Worst Behavior from Nothing Was The Same - 4:37')

if __name__ == '__main__':
    unittest.main()