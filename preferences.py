"""
Beatbox 1.0

Copyright (C) 2013 Luke Hansford - l.s.hansford@gmail.com

DESCRIPTION

This module contains all functions relating to teh saving and loading of 
preferences in Beatbox.

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

## DEFAULT PREFERENCES
LIBRARY_COLUMNS = [
    {'Name':'Title', 'Activated':True,'Database Name': 'title', 'Column':0},
    {'Name':'Artist', 'Activated':True,'Database Name': 'artist', 'Column':1},
    {'Name':'Album', 'Activated':True,'Database Name': 'album', 'Column':2},
    {'Name':'Year', 'Activated':True,'Database Name': 'year', 'Column':3},
    {'Name':'Genre', 'Activated':True,'Database Name': 'genre', 'Column':4},
    {'Name':'Track Number', 'Activated':True,'Database Name': 'track_number',
     'Column':5},
    {'Name':'Total Tracks', 'Activated':True,'Database Name': 'total_tracks',
     'Column':6},
    {'Name':'Disc Number', 'Activated':True,'Database Name': 'disc_number',
     'Column':7},
    {'Name':'Total Discs', 'Activated':True,'Database Name': 'total_discs',
     'Column':8},
    {'Name':'Album Artist', 'Activated':True,'Database Name': 'album_artist',
     'Column':9},
    {'Name':'Publisher', 'Activated':True,'Database Name': 'publisher',
     'Column':10},
    {'Name':'File Path', 'Activated':True,'Database Name': 'path',
     'Column':11},
    {'Name':'Time', 'Activated':True,'Database Name': 'time',
     'Column':12},
    {'Name':'Plays', 'Activated':True,'Database Name': 'plays',
     'Column':13},
    {'Name':'Comment', 'Activated':True,'Database Name': 'comment',
     'Column':14},
    {'Name':'Date Added', 'Activated':True, 'Database Name': 'date_added',
     'Column':15},
    {'Name':'Composer', 'Activated':True, 'Database Name': 'composer',
     'Column':16},
    {'Name':'BPM', 'Activated':True, 'Database Name': 'bpm',
     'Column':17},
    {'Name':'Date Modified', 'Activated':True, 'Database Name': 'date_modified',
     'Column':18},
    {'Name':'Size', 'Activated':True, 'Database Name': 'size', 'Column':19},
    {'Name':'Bit Rate', 'Activated':True, 'Database Name': 'bit_rate',
     'Column':20},
    {'Name':'Sample Rate', 'Activated':True, 'Database Name': 'sample_rate',
     'Column':21},
    {'Name':'Format', 'Activated':True, 'Database Name': 'format', 'Column':22},
    {'Name':'Channels', 'Activated':True, 'Database Name': 'channels',
     'Column':23}

]

class Preferences(object):

	def __init__(self, parent):
		self.parent = parent
		self.preferences = {}
		self.load_prefs()

	def load_prefs(self):
		""" Loads the saved preferences if they exist.

		Preferences.load_prefs() -> None
		"""
		if os.path.exists('data/preferences.cpk'):
			pickled_prefs = open('data/preferences.cpk', 'rb')
			self.preferences = cPickle.load(pickled_prefs)
			pickled_prefs.close()

	def save_prefs(self):
		""" Saves the current preferences. Called when the app is closed.

		Preferences.save_prefs() -> None
		"""
		output = open('data/preferences.cpk', 'wb')
		self.preferences['shuffle'] = self.set_shuffle_pref()
		self.preferences['repeat'] = self.set_repeat_pref()
		self.preferences['library_directories'] = self.set_library_dirs_pref()
		self.preferences['library_columns'] = self.set_library_columns_pref()
		self.preferences['language'] = self.set_language_pref()
		cPickle.dump(self.preferences, output)
		output.close()

	def set_shuffle_pref(self):
		""" Gets the current shuffle preferences to be saved.

		Preferences.set_shuffle_pref() -> boolean
		"""
		return self.parent.beatbox_gui.player_gui.player.get_shuffle_mode()

	def get_shuffle_pref(self):
		""" Gets the saved shuffle preferences.

		Preferences.get_shuffle_pref() -> boolean
		"""
		return self.preferences.get('shuffle', False)

	def set_repeat_pref(self):
		""" Gets the current repeat preferences to be saved.

		Preferences.set_repeat_pref() -> boolean
		"""
		return self.parent.beatbox_gui.player_gui.player.get_repeat_mode()

	def get_repeat_pref(self):
		""" Gets the saved repeat preferences.

		Preferences.get_repeat_pref() -> boolean
		"""
		return self.preferences.get('repeat', False)

	def set_library_dirs_pref(self):
		""" Gets the current library directories to be saved.

		Preferences.set_library_dirs_pref() -> list(str)
		"""
		return self.parent.beatbox_gui.tabview_gui.library_gui.library.\
		directories

	def get_library_dirs_pref(self):
		""" Gets the saved library directories.

		Preferences.get_library_dirs_pref() -> list(str)
		"""
		return self.preferences.get('library_directories', [])

	def set_library_columns_pref(self):
		""" Gets the current library columns to be saved.

		Preferences.set_library_columns_pref() -> dict
		"""
		return self.parent.beatbox_gui.tabview_gui.library_gui.library_columns

	def get_library_columns_pref(self):
		""" Gets the saved library columns.

		Preferences.get_library_columns_pref() -> dict
		"""
		return self.preferences.get('library_columns', LIBRARY_COLUMNS)

	def set_language_pref(self):
		""" Gets the current language to be saved.

		Preferences.set_language_pref() -> str
		"""
		return self.parent.beatbox_gui.get_language()

	def get_language_pref(self):
		""" Gets the saved language.

		Preferences.get_language_pref() -> dict
		"""
		return self.preferences.get('language', 'English')


