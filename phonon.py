"""
Beatbox 1.0

Copyright (C) 2013 Luke Hansford - l.s.hansford@gmail.com

DESCRIPTION

This module contains all functions relating to audio playback through Phonon in 
Beatbox.

LICENSE

I, Luke Hansford, Hereby grant the rights to distribute, modify, and edit the
source to Beatbox 1.0, on the condition that this agreement, and my ownership
of the code contained herewithin be maintained.

Furthurmore, I grant the right to use excerpts from the source to Beatbox 1.0
without express permission, with exclusion of commercial application.
"""

#3rd party libraries
from PySide.phonon import Phonon

class PhononInstance(object):
	def __init__(self, parent):
		self.parent = parent

	def create_media_object(self):
		""" Creates an instance of Phonon for playing songs in the parent
		application.

		PhononInstance.create_media_object() -> Phonon.MediaObject
		"""
		self._media_object = Phonon.MediaObject(self.parent)
		self._media_object.setTickInterval(1000) # Set the tick time to 1 sec
		self._media_object.tick.connect(self.on_tick)
		self._media_object.prefinishMarkReached.connect(self.halfway_reached)
		self.audio_output = Phonon.AudioOutput(
			Phonon.MusicCategory, self.parent)
		Phonon.createPath(self._media_object, self.audio_output)
		return self._media_object

	def is_loaded(self):
		""" Checks if a song has been loaded into the MediaObject. Returns
		false if it hasn't. If there is a song it returns true.

		PhononInstance.is_loaded() -> bool
		"""
		if self._media_object.state() == Phonon.State.LoadingState:
			return False
		else:
			return True

	def is_playing(self):
		""" Checks if a song is playing in the MediaObject. Returns true if
		there is, false if not.

		PhononInstance.is_playing() -> bool
		"""
		if self._media_object.state() == Phonon.State.PlayingState:
			return True
		else:
			return False

	def on_tick(self, time):
		""" Called on each tick (or every second) of the song loaded by Phonon.
		Calls a function to change the PlayerGui's track time display.

		PhononInstance.on_tick(int) -> None
		"""
		self.parent.player_gui.set_track_time(
			self._media_object.remainingTime())

	def set_halfway_mark(self):
		""" Calculates the halway point of the currently loaded song and sets it
		as a the prefinishMark for the MediaObject.

		PhononInstance.set_halfway_mark() -> None
		"""
		song_length = self._media_object.totalTime()
		self._media_object.setPrefinishMark(song_length/2)

	def halfway_reached(self, time):
		""" Called at the currently playing song's halfway mark. Updates that
		song's play count in the database.

		PhononInstance.halfway_reached(int) -> None
		"""
		path = self._media_object.currentSource().fileName()
		self.parent.tabview_gui.library_gui.library.update_play_count(path)
		
if __name__ == "__main__":
    pass