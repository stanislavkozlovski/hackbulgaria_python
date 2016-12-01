import os
import mutagen

from song import Song
from playlist import Playlist

MUTAGEN_ARTIST_KEY = 'TPE1'
MUTAGEN_ALBUM_KEY = 'TALB'
MUTAGEN_SONG_TITLE_KEY = 'TIT2'


class MusicCrawler:
    def __init__(self, path_to_folder):
        if not os.path.isabs(path_to_folder):
            path_to_folder = os.path.abspath(path_to_folder)
        self.folder_path = path_to_folder
        self.songs = self.crawl_directory_for_mp3s()

    def crawl_directory_for_mp3s(self):
        songs = []  # hold the path to all the songs here

        def __collect_music_files(absolute_dir_path):
            """ scans the files in a directory and adds them to our songs list if they are .mp3 or .ogg files """
            for file in os.scandir(absolute_dir_path):
                if os.path.isdir(file.name):
                    # if we have a directory, go in it
                    __collect_music_files(file.path)
                else:
                    if (file.name.endswith('.mp3') or file.name.endswith('.ogg')) and file.is_file():
                        songs.append(file.path)  # adds the absolute file path to the mp3 or ogg file

        __collect_music_files(self.folder_path)
        return songs

    def generate_playlist(self):
        """ Generate a Playlist class object of songs we've crawled and return it """
        pass

    def convert_paths_to_songs(self):
        """ Convert our list of song paths to Song class objects """
        #     def __init__(self, title: str, artist: str, album: str, length: str):
        song_objects = []
        for song_path in self.songs:
            if song_path.endswith('.mp3'):
                song = MP3(song_path)  # to get the MP3 tags
                duration_str = timedelta(int(song.info.length))
                if 'day' in duration_str:
                    raise Exception('Duration is too long!')
                hours, minutes, seconds = duration_str.split(':')
                song_obj = Song(title=song[MUTAGEN_SONG_TITLE_KEY], artist=song[MUTAGEN_ARTIST_KEY],
                     album=song[MUTAGEN_ALBUM_KEY], length='{h}:{m}:{s}'.format(h=hours, m=minutes, s=seconds))
                song_objects.append(song_obj)
            elif song_path.endswith('.ogg'):
                pass
            else:
                raise Exception('Invalid file type!')
        self.songs = song_objects

from mutagen.mp3 import MP3
drake = MusicCrawler('./music_crawler_test').songs[0]
print(drake)
song = MP3(drake)
print(song.info.length)
from datetime import timedelta
duration_str = str(timedelta(seconds=int(song.info.length)))
print(duration_str)
if 'day' in duration_str:
    raise Exception('Duration is too long!')
h, m, s = duration_str.split(':')
print(h)
print(m)
print(s)
