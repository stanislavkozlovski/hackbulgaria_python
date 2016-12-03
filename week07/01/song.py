from datetime import timedelta

class Song:
    def __init__(self, title: str, artist: str, album: str, length: str):
        self.title = title
        self.artist = artist
        self.album = album
        self.length = length
        # Store the time as a timedelta object
        self.timedelta_length = timedelta(
            hours=int(self.song_length(hours=True)),
            minutes=int(self.song_length(minutes=True)),
            seconds=int(self.song_length(seconds=True)))  # type: timedelta
        self.length = self.construct_str_length()

    def __str__(self):
        return "{artist} - {title} from {album} - {length}".format(
            artist=self.artist, title=self.title, album=self.album, length=self.length)

    def __eq__(self, other):
        return self.__str__() == str(other)

    def __hash__(self):
        return hash(self.__str__())

    def song_length(self, seconds=False, minutes=False, hours=False):
        split_len = self.length.split(':')
        if seconds:
            return split_len[-1] or '00'
        elif minutes:
            if len(split_len) < 2:
                return '0'
            else:
                return split_len[-2]
        elif hours:
            if len(split_len) < 3:
                return '0'
            else:
                return split_len[-3]
        else:
            return self.length

    def construct_str_length(self):
        """ This function converts our length str to a more pretty one
            ex: 00:04:37 => 4:37"""
        modified_length = str(int(self.length.replace(':', '')))  # 000437 => 437
        new_str = []
        if len(modified_length) % 2 == 0:
            start = 0
        else:
            start = 1
            new_str.append(modified_length[0])
        for idx in range(start, len(modified_length), 2):
            new_str.append(modified_length[idx:idx+2])

        return ':'.join(new_str)

