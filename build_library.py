# -◊- coding: utf-8 -◊-

import os.path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
import mutagen
import sqlite3
from mutagen.oggvorbis import OggVorbis
from mutagen.easyid3 import EasyID3

import metadata



class Library():
	def __init__(self):
		# self.directories = [u"/Volumes/Macintosh HD/Users/luke/Downloads/"]
	# directories = [u"/Volumes/Seagate Backup Plus Drive/Music/"]
		self.metadata = metadata.Metadata()

	def scan_directory(self, directory):
		song_list = []
		for dirpath,dirnames,filenames in os.walk(directory):
		    for f in filenames:
		        if f.endswith(".flac"):
		             song_list.append(dirpath+'/'+f)
		        elif f.endswith(".mp3"):
		             song_list.append(dirpath+'/'+f)
		        elif f.endswith(".ogg"):
		             song_list.append(dirpath+'/'+f)  
		return song_list

	def scan_all_directories(self, directories):
		library = []
		for directory in directories:
			library += self.scan_directory(directory)
		return library

	def create_library_database(self, library):

		connection = sqlite3.connect('library.db')
		with connection:
			cursor = connection.cursor()
			cursor.execute("DROP TABLE IF EXISTS Songs")
			cursor.execute("CREATE TABLE Songs(id INT, path TEXT, artist TEXT, title TEXT, album TEXT, year TEXT, genre TEXT, track_number INT, total_tracks INT, disc_number INT, total_discs INT, album_artist TEXT, publisher TEXT)")
			i = 1
			for path in library:
				md = metadata.get_metadata(path)
				cursor.execute("INSERT INTO Songs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
				 (i, path, md['Artist'], md['Track'], md['Album'], md['Year'],
				  md['Genre'], md['Track Number'], md['Total Tracks'], md['Disc Number'],
				  md['Total Discs'], md['Album Artist'], md['Publisher']))
				i += 1

# library = scan_all_directories(directories)
# create_library_database(library)

# for song in library:
# 	print "~~~~~~~~~~~~~~~~~~~~~~~~"
# 	md = mutagen.File(song)
# 	# print md.pprint()
# 	try:
# 		print md.tags['APIC:']
# 	except:
# 		print "NA"
# 	# if song.endswith(".ogg"):
# 	# 	audio = mutagen.oggvorbis.OggVorbis(song)
# 	# 	print audio.pprint()
# 	# 	a2 = mutagen.File(song)
# 	# 	print a2.pprint()
# 	# elif song.endswith(".flac"):
# 	# 	audio = FLAC(csong)
# 	# 	try:
# 	# 		print audio['totaltracks']
	# 	except:
	# 		try:
	# 			print audio['tracktotal']
	# 		except:
	# 			print "fail"
