from song import Song
from random import randrange
from datetime import timedelta
import json
import os
from prettytable import PrettyTable


class Playlist:
    def __init__(self, name: str, repeat: bool=False, shuffle: bool=False):
        self.name = name
        self.repeat = repeat
        self.shuffle = shuffle
        self.songs = []
        # holds a boolean value telling us if the song at the given index has been played
        self.played_songs = []  # type: [bool]
        self.artists = {}  # holds the artist as a key and as value - a list of each artist's song

    def add_song_to_artists(self, song):
        if song.artist not in self.artists.keys():
            self.artists[song.artist] = []
        self.artists[song.artist].append(song)

    def remove_song_from_artists(self, song):
        self.artists[song.artist].remove(song)
        if len(self.artists[song.artist]) == 0:
            del self.artists[song.artist]

    def add_song(self, song):
        self.songs.append(song)
        self.played_songs.append(False)
        self.add_song_to_artists(song)

    def remove_song(self, song):
        song_index = self.songs.index(song)
        self.songs.pop(song_index)
        self.played_songs.pop(song_index)
        self.remove_song_from_artists(song)

    def add_songs(self, songs: list):
        # first, add the songs to our artists
        for song in songs:
            self.add_song_to_artists(song)
        self.songs.extend(songs)
        self.played_songs.extend([False]*len(songs))

    def total_length(self):
        return str(sum([song.timedelta_length for song in self.songs], timedelta()))

    def get_artists(self):
        return {artist: len(songs) for artist, songs in self.artists.items()}

    def next_song(self):
        if self.repeat and all(self.played_songs):
            # If repeat is on and all the songs are played, reset them all to false - unplayed
            self.played_songs = [False for _ in self.played_songs]

        if self.shuffle:
            song_idx = randrange(0, len(self.played_songs))
            while self.played_songs[song_idx]:  # get random songs until we find one that has not been played
                song_idx = randrange(0, len(self.played_songs))
        else:
            # Get's the next unplayed song
            song_idx = self.played_songs.index(False)

        self.played_songs[song_idx] = True
        return self.songs[song_idx]

    def pprint_playlist(self):
        pretty_table = PrettyTable(["Artist", "Song", "Length"])  # create a new pretty_table object
        # fill the table's rows for each song
        [pretty_table.add_row([song.artist, song.title, song.length]) for song in self.songs]
        print(pretty_table)

    def save(self):
        """ Saves the playlist to a .json file """
        if not os.path.isdir('./playlist-data'):
            os.mkdir('./playlist-data')
        file_path = path.join('./playlist-data', self.name.replace(' ', '-') + '.json')
        populated_artists_dict = {}
        for artist, songs in self.artists.items():
            # convert the list of song classes to a list of dictionaries, representing the classes
            stringified_songs = []
            for song in songs:
                songs_dict = song.__dict__
                del songs_dict['timedelta_length']
                stringified_songs.append(str(songs_dict))
            populated_artists_dict[artist] = stringified_songs
        with open(file_path, 'w', encoding='utf-8') as new_json:
            json.dump(populated_artists_dict, new_json)

    @staticmethod
    def load(file_name: str):
        file_path = os.path.join('./playlist-data', file_name)
        songs = []  # read the songs from our json file
        with open(file_path) as json_data:
            artists = json.load(json_data)  # type: dict
            for artist_songs in artists.values():
                songs.extend(artist_songs)

        # convert the list of song dictionaries to a list of song classes
        song_objects = []  # type: [Song]
        for song in songs:
            song_dict = json.loads(song.replace("'", '"'))
            song_objects.append(Song(title=song_dict['title'], artist=song_dict['artist'], album=song_dict['album'], length=song_dict['length']))
        # create the new playlist
        loaded_playlist = Playlist(name=file_name[:-5].replace('-', ' '))
        loaded_playlist.add_songs(song_objects)  # add the songs to the playlist
        return loaded_playlist
