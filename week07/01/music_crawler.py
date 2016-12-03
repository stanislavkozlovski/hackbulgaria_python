import os
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from datetime import timedelta

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
        self.convert_paths_to_songs()  # turns our songs list into a list of Song objects
        playlist = Playlist('New Playlist')
        print(self.songs)
        playlist.add_songs(self.songs)

        return playlist

    def convert_paths_to_songs(self):
        """ Convert our list of song paths to Song class objects """
        song_objects = []
        for song_path in self.songs:
            if song_path.endswith('.mp3'):
                song = MP3(song_path)  # to get the MP3 tags
                title, artist, album = (str(song[MUTAGEN_SONG_TITLE_KEY]), str(song[MUTAGEN_ARTIST_KEY]),
                                        str(song[MUTAGEN_ALBUM_KEY]))
            elif song_path.endswith('.ogg'):
                song = OggVorbis(song_path)  # to get the tags
                song_tags = {key: val for key, val in song.tags}  # the tags are originally a list of tuples
                title, artist, album = str(song_tags['title']), str(song_tags['artist']), str(song_tags['album'])
            else:
                raise Exception('Invalid file type!')

            duration_str = str(timedelta(seconds=int(song.info.length)))
            if 'day' in duration_str:
                raise Exception('Duration is too long!')
            hours, minutes, seconds = duration_str.split(':')
            song_obj = Song(title=title, artist=artist,
                            album=album, length='{h}:{m}:{s}'.format(h=hours, m=minutes, s=seconds))
            song_objects.append(song_obj)

        self.songs = song_objects
