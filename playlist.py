
"""
Beatbox 1.0

Copyright (C) 2013 Luke Hansford - l.s.hansford@gmail.com

DESCRIPTION

This module contains all functions relating to the playlist in Beatbox.

LICENSE

I, Luke Hansford, Hereby grant the rights to distribute, modify, and edit the
source to Beatbox 1.0, on the condition that this agreement, and my ownership
of the code contained herewithin be maintained.

Furthurmore, I grant the right to use excerpts from the source to Beatbox 1.0
without express permission, with exclusion of commercial application.
"""

#Standard Libraries
import cPickle
import os.path

class Playlist(object):

	def __init__(self, parent):
		self.parent = parent
		self.playlist = []
		self.shuffled_playlist = []
		self.current_position = 0

	def get_playlist(self):
		""" Returns the playlist.

		Playlist.get_playlist() -> list(str)
		"""
		return self.playlist

	def insert_in_playlist(self, file_path, index):
		""" Inserts a file in to the playlist at the given index.

		Playlist.insert_in_playlist(str, int) -> None
		"""
		self.playlist.insert(index, file_path)
		if index <= self.get_current_position():
			self.set_current_position(self.get_current_position() + 1)

	def append_to_playlist(self, file_path):
		""" Appends a file to the playlist.

		Playlist.append_to_playlist(str) -> None
		"""
		self.playlist.append(file_path)

	def remove_item(self, index):
		""" Removes the file at the given index from the playlist.

		Playlist.remove_item(int) -> None
		"""
		self.playlist.pop(index)
		if index < self.get_current_position():
			self.set_current_position(self.get_current_position() - 1)

	def clear_playlist(self):
		""" Deletes all items in the playlist.

		Playlist.clear_playlist() -> None
		"""
		self.playlist = []

	def get_playlist_length(self):
		""" Returns the number of items in the playlist with 0 as the first
		item. i.e. a return of 9 means there are 10 songs in the playlist.

		Playlist.get_playlist_length() -> int
		"""
		return len(self.playlist)

	def get_playlist_item(self, index):
		""" Returns the file_path at the given index of the playlist.

		Playlist.get_playlist_item(int) -> str
		"""
		return self.playlist[index]

	def set_current_position(self, index):
		""" Sets the current position of playback to the given index.

		Playlist.set_current_position(int) -> None
		"""
		self.current_position = index

	def get_current_position(self):
		"""Returns the current position of playback.

		Playlist.get_current_position() -> int
		"""
		return self.current_position

	def save_playlist(self):
		""" Saves the playlist using pickle for retrieval next time the app is
		run.

		Playlist.save_playlist() -> None
		"""
		output = open('data/playlist.cpk', 'wb')
		playlist = []
		for row, item in enumerate(self.get_playlist()):
			playlist_dict = {}
			playlist_dict['file_path'] = item
			lv_item = self.parent.playlist_gui.playlist_model.item(row)
			playlist_dict['artist'] = lv_item.get_artist()
			playlist_dict['title'] = lv_item.get_title()
			playlist.append(playlist_dict)
		cPickle.dump(playlist, output)
		output.close()

	def load_playlist_pickle(self):
		""" Loads the playlist saved from the previous session. If none exists
		then it returns an empty list.

		Playlist.load_playlist -> None
		"""

		playlist = []
		if os.path.exists('data/playlist.cpk'):
			pickled_playlist = open('data/playlist.cpk', 'rb')
			pickle_data = cPickle.load(pickled_playlist)
			playlist = [i for i in pickle_data]
			pickled_playlist.close()
		return playlist


if __name__ == "__main__":
    pass