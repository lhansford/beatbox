# -◊- coding: utf-8 -◊-

"""
Beatbox 1.0

Copyright (C) 2013 Luke Hansford - l.s.hansford@gmail.com

DESCRIPTION

This module contains all functions for the running of Beatbox's library.

LICENSE

I, Luke Hansford, Hereby grant the rights to distribute, modify, and edit the
source to Beatbox 1.0, on the condition that this agreement, and my ownership
of the code contained herewithin be maintained.

Furthurmore, I grant the right to use excerpts from the source to Beatbox 1.0
without express permission, with exclusion of commercial application.
"""

#Standard libraries
import os.path
import sqlite3
import datetime

#3rd party libraries
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.easyid3 import EasyID3

#Beatbox libraries
import metadata


DATABASE_NAME = 'data/library.db'

class Library(object):
	def __init__(self, parent, columns):
		self.parent = parent
		self.localisation = self.parent.localisation
		self.directories = self.parent.preferences.get_library_dirs_pref()
		self._columns = columns
		if not self.database_exists():
			self.build_library(self.directories)

	def database_exists(self):
		""" Checks that the library database file exists. Returns a boolean of
		True for exists, False for doesn't exist.

		Library.database_exists() -> bool
		"""
		return os.path.exists(DATABASE_NAME)

	def scan_directory(self, directory):
		""" Scans a given directory for MP3, FLAC, and OGG files. If they are
		found they are appended to a list which is returned once the search is
		complete.

		Library.scan_directory(str) -> list(str)
		"""

		progress_dialog = self.parent.get_add_files_progress_dialog()
		files_added = progress_dialog.value()
		file_paths = []
		for dirpath,dirnames,filenames in os.walk(directory):
		    for f in filenames:
		        if f.endswith(".flac"):
		             file_paths.append(dirpath+'/'+f)
		             files_added += 1
		        elif f.endswith(".mp3"):
		             file_paths.append(dirpath+'/'+f)
		             files_added += 1
		        elif f.endswith(".ogg"):
		             file_paths.append(dirpath+'/'+f)
		             files_added += 1
		        elif f.endswith(".m4a"):
		             file_paths.append(dirpath+'/'+f)
		             files_added += 1
		       	elif f.endswith(".wma"):
		             file_paths.append(dirpath+'/'+f)
		             files_added += 1
		    progress_dialog.setValue(files_added)
		return file_paths

	def scan_all_directories(self, directories):
		""" Calls the scan_directory function for a list of given directories.
		Returns a list all song files from all given directories.

		Library.scan_all_directories(list(str)) -> list(str)
		"""
		self.parent.create_add_files_progress_dialog()
		all_files = []
		for directory in directories:
			all_files += self.scan_directory(directory)
		return all_files

	def add_directory(self, directory):
		self.directories.append(directory)

	def remove_directory(self, directory):
		self.directories.remove(directory)

	def build_library(self, directories):
		""" Scans all given directories and creates a database from the result.

		Library.build_library(list(str)) -> None
		"""
		file_paths = self.scan_all_directories(directories)
		self.create_library_database()
		self.add_files_to_library(file_paths)
		return None

	def get_library(self):
		""" Returns all rows from the library database.

		Library.get_library() -> list(tuple)
		"""
		select_query = self.build_select_query(self._columns)
		all_rows = []
		connection = sqlite3.connect(DATABASE_NAME)
		with connection:
			cursor = connection.cursor()
			for row in cursor.execute('SELECT ' + select_query + ' FROM \
				songs ORDER BY artist ASC, album ASC, disc_number ASC, \
				track_number ASC'):
				all_rows.append(row)
		return all_rows

	def build_select_query(self, columns):
		"""Creates a select query for SQLite based on which columns are supplied

		Library.build_select_query(self, dict) -> str
		"""
		select_query = ""
		for col in columns:
			select_query += (col['Database Name'] + ', ')
		return select_query[:-2] # -2 gets rid of superfluous ', '

	def update_play_count(self, file_path):
		""" Adds 1 to the play count of the given song in the library database.

		Library.update_play_count(str) -> None
		"""
		connection = sqlite3.connect(DATABASE_NAME)
		with connection:
			cursor = connection.cursor()
			query_result = cursor.execute(
				'SELECT plays FROM songs WHERE path = "' + file_path + '"')
			current_play_count = query_result.fetchone()
			if current_play_count:
				cursor.execute("UPDATE songs SET plays = ? WHERE path = ?",
				 (current_play_count[0]+1, file_path))
			else:
				return None
		self.parent.update_table_row(file_path)
	
	def get_item_data(self, file_path):
		""" Returns the row of the given song from the library database.

		Library.get_item_data(str) -> tuple
		"""	
		select_query = self.build_select_query(self._columns)
		connection = sqlite3.connect(DATABASE_NAME)

		with connection:
			cursor = connection.cursor()
			query_result = cursor.execute('SELECT ' + select_query + \
				' FROM songs WHERE path = "' + file_path + '"')
		return query_result.fetchone() #path is primary key so only 1 result

	def create_library_database(self):
		""" Creates the library database.

		Library.create_library_database() -> None
		"""
		connection = sqlite3.connect(DATABASE_NAME)
		with connection:
			cursor = connection.cursor()
			cursor.execute("DROP TABLE IF EXISTS Songs")

			cursor.execute("CREATE TABLE Songs(path TEXT PRIMARYKEY, \
				artist TEXT, title TEXT, album TEXT, year TEXT, genre TEXT, \
				track_number INT, total_tracks INT, disc_number INT, \
				total_discs INT, album_artist TEXT, publisher TEXT, time REAL, \
				plays INT, comment TEXT, date_added TEXT, composer TEXT, \
				bpm TEXT, date_modified TEXT, size TEXT, bit_rate TEXT, \
				sample_rate TEXT, format TEXT, channels TEXT)")

	def get_library_files(self):
		""" Returns all file paths from the library database.

		Library.get_library_files() -> list(tuple)
		"""
		connection = sqlite3.connect(DATABASE_NAME)
		with connection:
			cursor = connection.cursor()
			rows = [row[0] for row in cursor.execute('SELECT path FROM songs')]
		return rows

	def update_library(self):
		""" Scans all the directories and checks them against the current
		library, and adds any new files. Returns a list of all items added
		successfully.

		Library.update_library() -> list(str)
		"""
		all_files = self.scan_all_directories(self.directories)
		current_library = self.get_library_files()
		new_files = [f for f in all_files if f not in current_library]
		successful_files = self.add_files_to_library(new_files)
		return successful_files

	def update_file(self, track):
		""" Updates the given track in the library.

		Library.update_file(Track) -> None
		"""
		connection = sqlite3.connect(DATABASE_NAME)
		with connection:
			cursor = connection.cursor()
			## Need to get date added and plays as they're Beatbox specific
			query_result = cursor.execute('SELECT plays, date_added FROM\
			 songs WHERE path = "' + track.file_path + '"')
			row = query_result.fetchone()
			play_count = row[0]
			date_added = row[1]
			cursor.execute("UPDATE songs SET path=?, artist=?, title=?, \
				album=?, year=?, genre=?, track_number=?, total_tracks=?, \
				disc_number=?, total_discs=?, album_artist=?, publisher=?, \
				time=?, plays=?, comment=?, date_added=?, composer=?, bpm=?, \
				date_modified=?, size=?, bit_rate=?, sample_rate=?, format=?, \
				channels=? WHERE path = ?", (track.file_path, track.artist, 
					track.title, track.album, 
				 	track.year, track.genre, track.track_number, 
				 	track.total_tracks, track.disc_number, track.total_discs, 
				 	track.album_artist, track.publisher, track.time, play_count, 
				 	track.comment, date_added, track.composer, track.bpm,
				 	track.date_modified, track.size, track.bit_rate, 
				 	track.sample_rate, track.format, track.channels,
				 	track.file_path))
		self.parent.update_table_row(track.file_path)

	def file_in_library(self, file_path):
		connection = sqlite3.connect(DATABASE_NAME)
		cursor = connection.cursor()
		with connection:
			query_result = cursor.execute(
				'SELECT * FROM songs WHERE path = "' + file_path + '"')
		if query_result.fetchone() == None:
			return False
		else:
			return True

	def add_files_to_library(self, file_paths):
		""" Adds the given file paths to the library. Returns a list of all
		files that were successfully to be added to the library.

		Library.add_files_to_library(list(str)) -> list(str)
		"""
		progress_dialog = self.parent.get_add_files_progress_dialog()
		tracks_added = 0
		progress_dialog.setValue(tracks_added)
		progress_dialog.setLabelText(self.localisation.ADDING_FILES_STRING)
		progress_dialog.setMaximum(len(file_paths))

		connection = sqlite3.connect(DATABASE_NAME)
		current_date = datetime.datetime.now()
		successful_files = []
		with connection:
			cursor = connection.cursor()
			for file_path in file_paths:
				try:
					track = metadata.Track(file_path)
					cursor.execute("INSERT INTO Songs VALUES(?, ?, ?, ?, ?, ?,\
					 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
					 (track.file_path, track.artist, track.title, track.album, 
					 	track.year, track.genre, track.track_number, 
					 	track.total_tracks, track.disc_number,
					 	track.total_discs, track.album_artist, track.publisher,
					 	track.time, 0 , track.comment, current_date,
					 	track.composer, track.bpm,
					 	track.date_modified, track.size, track.bit_rate, 
					 	track.sample_rate, track.format, track.channels))

					successful_files.append(file_path)

				except:					
					print file_path + " could not be added to the library."
				tracks_added += 1
				progress_dialog.setValue(tracks_added)
		return successful_files

	def remove_items(self, file_paths):
		""" Remove the given files from the library.

		Library.remove_items(list(str)) -> None
		"""
		connection = sqlite3.connect(DATABASE_NAME)
		with connection:
			cursor = connection.cursor()
			for file_path in file_paths:
				cursor.execute(
					'DELETE FROM Songs WHERE path = "' + file_path + '"')

if __name__ == "__main__":
    pass