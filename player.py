"""
Beatbox 1.0

Copyright (C) 2013 Luke Hansford - l.s.hansford@gmail.com

DESCRIPTION

This module contains all functions relating to control of audio playback in 
Beatbox.

LICENSE

I, Luke Hansford, Hereby grant the rights to distribute, modify, and edit the
source to Beatbox 1.0, on the condition that this agreement, and my ownership
of the code contained herewithin be maintained.

Furthurmore, I grant the right to use excerpts from the source to Beatbox 1.0
without express permission, with exclusion of commercial application.
"""

#Standard Libraries
import random

#3rd party libraries
from PySide.phonon import Phonon

#Beatbox libraries
import metadata

class Player(object):

    def __init__(self, parent):
        self.parent = parent
        self.phonon = self.parent.phonon
        self.playlist = self.parent.playlist
        self.media_object = self.parent.media_object
        self.metadata = metadata.Metadata()
        self.shuffle_mode = False 
        self.repeat_mode = False 
        self.mute = False
        self._current_artist = ""
        self._current_track = ""

    def load_metadata(self, file_path):
        """ Gets the metadata of file_path and sets the artist and track title
        to the result.

        Player.load_metadata(str) -> None
        """
        track = self.metadata.get_now_playing_metadata(file_path)
        self.set_current_artist(track.artist)
        self.parent.set_artist_name(track.artist)
        self.set_current_track(track.title)
        self.parent.set_track_name(track.title)
        self.parent.set_album_name(track.album)
        self.get_album_art(file_path)

    def play_song(self):
        """ Starts playback. If no song is loaded the first song in the playlist
        is loaded.

        Player.play_song() -> None
        """
        if self.phonon.is_loaded():
            self.parent.set_play_button_pause()
            self.media_object.play()
        elif self.playlist.get_playlist_length() > 0:
            self.parent.load_song(self.playlist.get_playlist_item(0))
            self.playlist.set_current_position(0)
            self.play_song()

    def pause_song(self):
        """ Pauses playback.

        Player.pause_song() -> None
        """
        self.parent.set_play_button_play()
        self.media_object.pause()

    def song_ended(self):
        """Called when a song finishes. Determines whether to go to the next 
        song or go to a random song based on the Shuffle mode.

        Player.song_ended() -> None
        """
        if self.get_shuffle_mode():
            self.next_song_shuffled()
        else:
            self.next_song()

    def previous_song(self):
        """ Loads the previous song in the playlist. If it the current song is 
        the first in the playlist then the loaded song remains the same.

        Player.previous_song() -> None
        """
        if self.get_shuffle_mode():
            self.previous_song_shuffled()
        else:
            position = self.playlist.get_current_position() - 1
            if position < self.playlist.get_playlist_length() and position >= 0:
                self.load_song_from_playlist(position)
            else: ## if it's the first song just set track to start again
                if self.media_object.state() == Phonon.PlayingState:
                    self.media_object.stop()
                    self.media_object.play()
                else:
                    self.media_object.stop()

    def previous_song_shuffled(self):
        """ Gets the previous song played according to the shuffle.

        Player.previous_song_shuffled() -> None
        """
        if len(self.playlist.shuffled_playlist) > 0:
            self.parent.load_song(self.playlist.shuffled_playlist[-2])
            self.playlist.shuffled_playlist.pop()
        else:
            if self.media_object.state() == Phonon.PlayingState:
                self.media_object.stop()
                self.media_object.play()
            else:
                self.media_object.stop()

    def next_song(self):
        """ Loads the next song in the playlist. If it the current song is the
        last in the playlist then it checks to see if repeat is on, and loads
        the first song in the playlist if it is.

        Player.next_song() -> None
        """
        position = self.playlist.get_current_position() + 1
        if position < self.playlist.get_playlist_length():
            self.load_song_from_playlist(position)
        elif self.get_repeat_mode():
            self.load_song_from_playlist(0) ## Go back to start if repeat on

    def next_song_shuffled(self):
        """ Chooses a random song from the playlist and loads it.

        Player.next_song_shuffled() -> None
        """
        position = self.playlist.get_current_position()
        while position == self.playlist.get_current_position():
            position = random.randint(0, self.playlist.get_playlist_length()-1)
        self.load_song_from_playlist(position)
        self.playlist.shuffled_playlist.append(
            self.playlist.get_playlist_item(position))


    def load_song_from_playlist(self, position):
        """ Loads a songs from the playlist based on the position given. If the
        player was already playing the song is loaded and played. If the player
        was in a pause state then the song is just loaded. The current playlist
        position is updated to reflect the change.

        Player.load_song_from_playlist(int) -> None
        """
        if self.media_object.state() == Phonon.PlayingState:
            self.parent.load_song(self.playlist.get_playlist_item(position))
            self.playlist.set_current_position(position)
            self.play_song()
        else:
            self.parent.load_song(self.playlist.get_playlist_item(position))
            self.playlist.set_current_position(position)

    def set_current_track(self, track):
        """Sets current track's title

        Player.set_current_track(str) -> None
        """
        self._current_track = track

    def get_current_track(self):
        """ Gets current track's title.

        Player.get_current_artist() -> str
        """
        return self._current_track

    def set_current_artist(self, artist):
        """Sets current track's artist

        Player.set_current_artist(str) -> None
        """
        self._current_artist = artist

    def get_current_artist(self):
        """ Gets current track's artist.

        Player.get_current_artist() -> str
        """
        return self._current_artist

    def get_album_art(self, file_path):
        """ Gets the album art of the given file_path and sets it as PlayerGui's
        album cover QLabel. The image is set as the default image if none is
        found.

        Player.get_album_art(str) -> None
        """
        artwork = self.metadata.get_album_cover(file_path)
        if not artwork:
            image = open('images/cover.png', 'rb')
            artwork = image.read()
            image.close()
        self.parent.set_album_art(artwork)

    def set_shuffle_mode(self):
        """ Sets shuffle mode. True represents 'shuffle', False represents 'no 
        shuffle'.

        Player.set_shuffle_mode() -> None
        """
        if self.shuffle_mode:
            self.shuffle_mode = False
        else:
            self.shuffle_mode = True

    def get_shuffle_mode(self):
        """ Gets current shuffle mode.

        Player.get_shuffle_mode() -> boolean
        """
        return self.shuffle_mode

    def set_repeat_mode(self):
        """ Sets repeat mode. True represents 'repeat', False represents 'no 
        repeat'.

        Player.set_repeat_mode() -> None
        """

        if self.repeat_mode:
            self.repeat_mode = False
        else:
            self.repeat_mode = True

    def get_repeat_mode(self):
        """ Gets current repeat mode.

        Player.get_repeat_mode() -> boolean
        """
        return self.repeat_mode

    def toggle_mute(self):
        """ Toggles the mute on and off.

        Player.toggle_mute() -> None
        """
        if self.mute:
            self.mute = False
            self.phonon.audio_output.setVolume(self._volume)
        else:
            self.mute = True
            self._volume = self.phonon.audio_output.volume()
            self.phonon.audio_output.setVolume(0)


    def format_time(self, time):
        """ Formats time from milliseconds to a -HH:MM:SS format.

        Player.format_time(int) -> str
        """
        time = time/1000
        minutes = time/60
        seconds = time%60
        if seconds < 10:
            seconds = '0' + str(seconds)
        ftime = '-' + str(minutes) + ':' + str(seconds)
        return ftime

if __name__ == "__main__":
    pass