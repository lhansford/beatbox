#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
Beatbox 1.0

Copyright (C) 2013 Luke Hansford - l.s.hansford@gmail.com

DESCRIPTION

This module contains all functions relating to the collection of metadata for 
songs in Beatbox.

LICENSE

I, Luke Hansford, Hereby grant the rights to distribute, modify, and edit the
source to Beatbox 1.0, on the condition that this agreement, and my ownership
of the code contained herewithin be maintained.

Furthurmore, I grant the right to use excerpts from the source to Beatbox 1.0
without express permission, with exclusion of commercial application.
"""

# Standard libraries
from os import listdir
import os.path
import time

# 3rd party libraries
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TRCK, TIT2, TPE1, TALB, TDRC, TCON, COMM, TPE2, TPUB, TCOM, TPOS
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.asf import ASF
from mutagen.oggvorbis import OggVorbis
from mutagen import *


class Metadata(object):
	"""This class contains all the functions for retrieving song metadata."""

	def isValidFile(self, path):
		""" Checks if a path is a valid audio file.

		Metadata.isValidFile(str) -> boolean
		"""
		if path.endswith(".mp3"):
			return True
		elif path.endswith(".flac"):
			return True
		elif path.endswith(".ogg"):
			return True
		elif path.endswith(".m4a"):
			return True
		elif path.endswith(".wma"):
			return True
		else:
			return False

	def get_mutagen_parser(self, file_path):
		""" Gets the correct audio parser and file format for the given path.

		Metadata.get_mutagen_parser(str) -> Mutagen, str
		"""

		if file_path.endswith(".mp3"):
			audio = MP3(file_path)
			format = "mp3"
		elif file_path.endswith(".flac"):
			audio = FLAC(file_path)
			format = "flac"
		elif file_path.endswith(".ogg"):
			audio = OggVorbis(file_path)
			format = "ogg"
		elif file_path.endswith(".m4a"):
			audio = MP4(file_path)
			format = "m4a"
		elif file_path.endswith(".wma"):
			audio = ASF(file_path)
			format = "wma"
		return audio, format
		
	def get_now_playing_metadata(self, path):
		""" Gets the metadata relevant from a song loaded in the player (i.e 
			artist name, song title, album name). Returns it as a Track object.
		
		Metadata.get_now_playing_metadata(str) -> Track
		"""
		track = Track(path)
		return track

	def get_playlist_metadata(self, path):
		""" Gets the artist and title of a track to add to the playlist.
		"""
		audio, format = self.get_mutagen_parser(path)
		artist = self.get_artist(audio, format)
		title = self.get_title(audio, format)
		return (artist, title)

	def get_artist(self, audio, format):
		""" Get the artist name from the metadata created by the Mutagen module. 

		Metadata.get_artist(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TPE1"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["artist"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["artist"][0]
			except:
				return ""
		elif format == "m4a":
			if audio["\xa9ART"]:
				return audio["\xa9ART"][0]
			else:
				return ""
		elif format == "wma":
			if audio["Author"]:
				return audio["Author"][0]
			else:
				return ""

	def get_title(self, audio, format):
		""" Get the song name from the metadata created by the Mutagen module. 

		Metadata.get_title(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TIT2"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["title"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["title"][0]
			except:
				return ""
		elif format == "m4a":
			if audio["\xa9nam"]:
				return audio["\xa9nam"][0]
			else:
				return ""
		elif format == "wma":
			if audio["Title"]:
				return audio["Title"][0]
			else:
				return ""

	def get_album(self, audio, format):
		""" Get the album name from the metadata created by the Mutagen module. 

		Metadata.get_album(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TALB"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["album"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["album"][0]
			except:
				return ""
		elif format == "m4a":
			if audio["\xa9alb"]:
				return audio["\xa9alb"][0]
			else:
				return ""
		elif format == "wma":
			if audio["WM/AlbumTitle"]:
				return str(audio["WM/AlbumTitle"][0])
			else:
				return ""

	def get_date(self, audio, format):
		""" Get the year/date of the song's creation from the metadata 
		created by the Mutagen module. 

		Metadata.get_date(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return str(audio["TDRC"][0])
			except:
				return ""
		elif format == "flac":
			try:
				return audio["date"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["date"][0]
			except:
				return ""
		elif format == "m4a":
			if audio["\xa9day"]:
				return audio["\xa9day"][0][:4] 
				#M4a stores as YYYY-MM-DD-HH-SS, only want the year so slice it.
			else:
				return ""
		elif format == "wma":
			if audio["WM/Year"]:
				return str(audio["WM/Year"][0])[:4]
			else:
				return ""

	def get_genre(self, audio, format):
		""" Get the song genre from the metadata created by the Mutagen module. 

		Metadata.get_genre(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TCON"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["genre"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["genre"][0]
			except:
				return ""
		elif format == "m4a":
			try:
				return audio["\xa9gen"][0]
			except:
				return ""
		elif format == "wma":
			try:
				return str(audio["WM/Genre"][0])
			except:
				return ""

	def get_track_number(self, audio, format):
		""" Get the track no. from the metadata created by the Mutagen module. 

		Metadata.get_track_number(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				track_number = audio["TRCK"][0]
				return track_number.split('/')[0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio['tracknumber'][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["tracknumber"][0]
			except:
				return ""
		elif format == "m4a":
			try:
				return str(audio["trkn"][0][0])
			except:
				return ""
		elif format == "wma":
			try:
				track_number = str(audio["WM/TrackNumber"][0])
				return track_number.split('/')[0]
			except:
				return ""

	def get_total_tracks(self, audio, format):
		""" Get the total number of tracks from the metadata created by the 
		Mutagen module. 

		Metadata.get_total_tracks(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				track_number = audio["TRCK"][0]
				return track_number.split('/')[1]
			except:
				return ""
		elif format == "flac":
			try:
				return audio['totaltracks'][0]
			except:
				try:
					return audio['tracktotal'][0]
				except:
					return ""
		elif format == "ogg":
			try:
				return audio["totaltracks"][0]
			except:
				return ""
		elif format == "m4a":
			try:
				return str(audio["trkn"][0][1])
			except:
				return ""
		elif format == "wma":
			try:
				track_number = str(audio["WM/TrackNumber"][0])
				return track_number.split('/')[1]
			except:
				return ""

	def get_disc_number(self, audio, format):
		""" Get the disc number from the metadata created by the Mutagen module. 

		Metadata.get_disc_number(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				disc_number = audio["TPOS"][0]
				return disc_number.split('/')[0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["discnumber"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["discnumber"][0]
			except:
				return ""
		elif format == "m4a":
			try:
				return str(audio["disk"][0][0])
			except:
				return ""
		elif format == "wma":
			try:
				disc_number = str(audio["WM/PartOfSet"][0])
				return disc_number.split('/')[0]
			except:
				return ""

	def get_total_discs(self, audio, format):
		""" Get the total number of discs from the metadata created by the
		Mutagen module. 

		Metadata.get_total_discs(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				disc_number = audio["TPOS"][0]
				return disc_number.split('/')[1]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["disctotal"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["disctotal"][0]
			except:
				return ""
		elif format == "m4a":
			try:
				return str(audio["disk"][0][1])
			except:
				return ""
		elif format == "wma":
			try:
				disc_number = str(audio["WM/PartOfSet"][0])
				return disc_number.split('/')[1]
			except:
				return ""

	def get_album_artist(self, audio, format):
		""" Get the album artist name from the metadata created by the Mutagen 
		module. 

		Metadata.get_album_artist(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TPE2"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["album artist"][0]
			except:
				try:
					return audio["albumartist"][0]
				except:
					return ""
		elif format == "ogg":
			try:
				return audio["album artist"][0]
			except:
				try:
					return audio["albumartist"][0]
				except:
					return ""
		elif format == "m4a":
			try:
				return audio["aART"][0]
			except:
				return ""
		elif format == "wma":
			try:
				return str(audio["WM/AlbumArtist"][0])
			except:
				return ""

	def get_bpm(self, audio, format):
		""" Get the BPM from the metadata created by the Mutagen 
		module. 

		Metadata.get_bpm(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TBPM"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["TBPM"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["TBPM"][0]
			except:
				return ""
		elif format == "m4a":
			try:
				return str(audio['tmpo'][0])
			except:
				return "" 
		elif format == "wma":
			try:
				return str(audio["WM/BeatsPerMinute"][0])
			except:
				return ""

	def get_composer(self, audio, format):
		""" Get the composer of the song from the metadata created by 
		the Mutagen module. 

		Metadata.get_bpm(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TCOM"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["composer"][0]
			except:
				try:
					return audio["TCOM"][0]
				except:
					return ""
		elif format == "ogg":
			try:
				return audio["composer"][0]
			except:
				try:
					return audio["TCOM"][0]
				except:
					return ""
		elif format == "m4a":
			try:
				return audio["\xa9wrt"][0]
			except:
				return ""
		elif format == "wma":
			try:
				return '/'.join([str(c) for c in audio["WM/Composer"]])
			except:
				return ""

	def get_publisher(self, audio, format):
		""" Get the publisher name from the metadata created by the Mutagen 
		module. 

		Metadata.get_publisher(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["TPUB"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["publisher"][0]
			except:
				try:
					return audio["label"][0]
				except:
					return ""
		elif format == "ogg":
			try:
				return audio["publisher"][0]
			except:
				try:
					return audio["label"][0]
				except:
					return ""
		elif format == "m4a":
			try:
				return audio["----:com.apple.iTunes:LABEL"][0]
			except:
				try:
					return audio["----:com.apple.iTunes:Label"][0]
				except:
					return ""
		elif format == "wma":
			try:
				return '/'.join([str(p) for p in audio["WM/Publisher"]])
			except:
				return ""

	def get_track_time(self, audio):
		""" Get the track length from the metadata created by the Mutagen
		module. 

		Metadata.get_track_time(Mutagen, str) -> str
		"""

		return self.format_time(audio.info.length)

	def get_date_modified(self, file_path):
		""" Get the date of last modification of the given path.

		Metadata.get_date_modified(str) -> time
		"""
		date_mod = time.ctime(os.path.getmtime(file_path))
		return date_mod

	def get_size(self, file_path):
		""" Get the size in Mb for the given path.

		Metadata.get_size(str) -> str
		"""
		size = float(os.path.getsize(file_path))
		mb = (size/1024)/1024
		return '%.2f MB' %mb

	def get_comment(self, audio, format):
		""" Get the comments from the metadata created by the Mutagen module. 

		Metadata.get_comment(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["COMM::'eng'"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["comment"][0]
			except:
				return ""
		elif format == "ogg":
			try:
				return audio["comment"][0]
			except:
				return ""
		elif format == "m4a":
			try:
				return audio["\xa9cmt"][0]
			except:
				return ""
		elif format =='wma':
			try:
				return str(audio["WM/Comments"][0])
			except:
				return ""

	def get_bit_rate(self, audio):
		""" Get the bit rate of the given song

		Metadata.get_bit_rate(Mutagen) -> str
		"""
		try:
			bit_rate = audio.info.bitrate/1000
			if bit_rate == 0:
				return "Unknown"
			return str(bit_rate) + " kbps"
		except:
			return "N/A"

	def get_sample_rate(self, audio):
		""" Get the sample rate of the given song

		Metadata.get_sample_rate(Mutagen) -> str
		"""
		if audio.info.sample_rate == 0:
			return "Unknown"
		else:
			return str(audio.info.sample_rate) + " kHz"

	def get_channels(self, audio):
		""" Get the number of channels of the given song

		Metadata.get_channels(Mutagen) -> str
		"""
		try:
			ch = audio.info.mode
			if ch == 0:
				return "Stereo"
			elif ch == 1:
				return "Joint Stereo"
			elif ch == 2:
				return "Dual Channel"
			elif ch == 3:
				return "Mono"
		except:
			try:
				ch = audio.info.channels
				if ch == 0:
					return "Unknown"
				elif ch == 1:
					return "Mono"
				elif ch == 2:
					return "Stereo"
				else:
					return str(ch)
			except:
				return "Unknown"

	def get_rating(self, audio, format):
		""" Get the rating of the track from the metadata 
		created by the Mutagen module. 

		Metadata.get_rating(Mutagen, str) -> str
		"""
		if format == "mp3":
			try:
				return audio["POPM"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["rating"][0]
			except:
				try:
					return audio["POPM"][0]
				except:
					return ""
		elif format == "ogg":
			try:
				return audio["rating"][0]
			except:
				try:
					return audio["POPM"][0]
				except:
					return ""
		elif format == "m4a":
			try:
				return audio["----:com.apple.iTunes:Rating"][0]
			except:
				return ""
		elif format == "wma":
			try:
				return audio["WM/Rating"][0]
			except:
				return ""

	def get_album_cover(self, file_path):
		""" Gets the album cover of the given track. Returns it as a string
		of bytes.

		Metadata.get_album_cover(str) -> str
		"""
		audio, format = self.get_mutagen_parser(file_path)
		if format == "mp3":
			try:
				image = audio["APIC:"].data
			except:
				image = ""
		elif format == "m4a":
			try:
				image = audio["covr"][0]
			except:
				image = ""
		elif format == "wma":
			try:
				image = unicode(str(audio["WM/Picture"][0]))
			except:
				image = ""
		else:
			image = ""
		if image == "":
			folder = file_path.rsplit('/', 1)[0]
			files = [f for f in listdir(folder) if os.path.isfile(
				os.path.join(folder,f))]
			for i, item in enumerate(files):
				files[i] = item.lower()
			for f in files:
				if f == 'cover.jpg':
					return self.convert_image(folder +'/cover.jpg')
				elif f == 'front.jpg':
					return self.convert_image(folder +'/front.jpg')
				elif f == 'folder.jpg':
					return self.convert_image(folder +'/folder.jpg')
		else:
			return image

	def convert_image(self, file_path):
		""" Opens a given image file and returns the bytes of it.

		Metadata.convert_image(str) -> str
		"""
		f = open(file_path, 'rb')
		image = f.read()
		f.close()
		return image

	def format_time(self, time):
		""" Formats a time given in milliseconds to a format of HH:MM:SS.

		Metadata.format_time(int) -> str
		"""
		time = int(time)
		hours = time / 3600
		if hours < 1:
			hours = ""
		elif hours < 10:
			hours = str(0) + str(hours) + ':'
		else:
			hours = str(hours) + ":"
		minutes = time / 60
		if minutes > 10 or hours == '':
			minutes = str(minutes) + ':'
		else:
			minutes = str(0) + str(minutes) + ':'
		seconds = time % 60
		if seconds < 10:
			seconds = str(0) + str(seconds)
		else:
			seconds = str(seconds)

		return hours + minutes + seconds

	def save_mp3_metadata(self, file_path, data):
		""" Saves the given metadata for an MP3 file.

		Metadata.save_mp3_metadata(str, dict)
		"""
		audio = ID3(file_path) # Writing MP3 tags needs ID3
		mp3_audio, format = self.get_mutagen_parser(file_path)

		if data.get("title"):
			audio.add(TIT2(encoding=3, text=unicode(data['title'])))
		if data.get("artist"):
			audio.add(TPE1(encoding=3, text=unicode(data['artist'])))
		if data.get("album"):
			audio.add(TALB(encoding=3, text=unicode(data['album'])))
		if data.get("genre"):
			audio.add(TCON(encoding=3, text=unicode(data['genre'])))
		if data.get("year"):
			audio.add(TDRC(encoding=3, text=unicode(data['year'])))
		if data.get("album_artist"):
			audio.add(TPE2(encoding=3, text=unicode(data['album_artist'])))

		if data.get("track_number", False) and data.get("total_tracks", False):
			audio.add(TRCK(encoding=3, text=unicode(
				data['track_number'] + '/' + data['total_tracks'])))
		elif data.get("track_number"):
			total_tracks = self.get_total_tracks(mp3_audio, format)
			if total_tracks == None:
				audio.add(TRCK(encoding=3, text=unicode(data['track_number'])))
			else:
				audio.add(TRCK(encoding=3, text=unicode(
					data['track_number'] + '/' + total_tracks)))
		elif data.get("total_tracks"):
			t_no = self.get_track_number(mp3_audio, format)
			if t_no == None:
				audio.add(TRCK(encoding=3, text=unicode(
					" /" + data["total_tracks"])))
			else:
				audio.add(TRCK(encoding=3, text=unicode(
					t_no + '/' + data["total_tracks"])))

		if data.get("disc_number", False) and data.get("total_discs", False):
			audio.add(TPOS(encoding=3, text=unicode(
				data['disc_number'] + '/' + data['total_discs'])))
		elif data.get("disc_number"):
			total_discs = self.get_total_discs(mp3_audio, format)
			if total_discs == None:
				audio.add(TPOS(encoding=3, text=unicode(data['disc_number'])))
			else:
				audio.add(TPOS(encoding=3, text=unicode(
					data['disc_number'] + '/' + total_discs)))
		elif data.get("total_discs"):
			d_no = self.get_disc_number(mp3_audio, format)
			if d_no == None:
				audio.add(TPOS(encoding=3, text=unicode(
					" /" + data["total_discs"])))
			else:
				audio.add(TPOS(encoding=3, text=unicode(
					d_no + '/' + data["total_discs"])))

		if data.get("composer"):
			audio.add(TCOM(encoding=3, text=unicode(data['composer'])))
		if data.get("publisher"):
			audio.add(TPUB(encoding=3, text=unicode(data['publisher'])))
		if data.get("comments"):
			audio.add(COMM(encoding=3, lang="eng", desc="", text=unicode(
				data['comments'])))
		audio.save()

	def save_flac_metadata(self, audio, data):
		""" Saves the given metadata for a FLAC or OGG file.

		Metadata.save_flac_metadata(Mutagen, dict)
		"""

		if data.get("title"):
			audio["title"] = data["title"]
		if data.get("artist"):
			audio["artist"] = data["artist"]
		if data.get("album"):
			audio["album"] = data["album"]
		if data.get("genre"):
			audio["genre"] = data["genre"]
		if data.get("year"):
			audio["date"] = data["year"]
		if data.get("track_number"):
			audio["tracknumber"] = data["track_number"]
		if data.get("total_tracks"):
			audio["totaltracks"] = data["total_tracks"]
		if data.get("disc_number"):
			audio["discnumber"] = data["disc_number"]
		if data.get("total_discs"):
			audio["disctotal"] = data["total_discs"]
		if data.get("album_artist"):
			audio["album artist"] = data["album_artist"]
		if data.get("composer"):
			audio["composer"] = data["composer"]
		if data.get("publisher"):
			audio["publisher"] = data["publisher"]
		if data.get("comments"):
			audio["comment"] = data["comments"]
		audio.save()

	def save_asf_metadata(self, audio, data):
		""" Saves the given metadata for a WMA file.

		Metadata.save_asf_metadata(Mutagen, dict)
		"""

		if data.get("title"):
			audio["Title"] = data["title"]
		if data.get("artist"):
			audio["Author"] = data["artist"]
		if data.get("album"):
			audio["WM/AlbumTitle"] = data["album"]
		if data.get("genre"):
			audio["WM/Genre"] = data["genre"]
		if data.get("year"):
			audio["WM/Year"] = data["year"]

		if data.get("track_number", False) and data.get("total_tracks", False):
			audio["WM/TrackNumber"] = unicode(
				data['track_number'] + '/' + data['total_tracks'])
		elif data.get("track_number"):
			total_tracks = self.get_total_tracks(audio, 'wma')
			if total_tracks == None:
				audio["WM/TrackNumber"] = unicode(data['track_number'])
			else:
				audio["WM/TrackNumber"] = unicode(
					data['track_number'] + '/' + total_tracks)
		elif data.get("total_tracks"):
			t_no = self.get_track_number(audio, 'wma')
			if t_no == None:
				audio["WM/TrackNumber"] = unicode(' /' + data['total_tracks'])
			else:
				audio["WM/TrackNumber"] = unicode(
					t_no + '/' + data['total_tracks'])

		if data.get("disc_number", False) and data.get("total_discs", False):
			audio["WM/PartOfSet"] = unicode(
				data['disc_number'] + '/' + data['total_discs'])
		elif data.get("disc_number"):
			total_discs = self.get_total_discs(audio, 'wma')
			if total_discs == None:
				audio["WM/PartOfSet"] = unicode(data['disc_number'])
			else:
				audio["WM/PartOfSet"] = unicode(
					data['disc_number'] + '/' + total_discs)
		elif data.get("total_discs"):
			d_no = self.get_disc_number(audio, 'wma')
			if d_no == None:
				audio["WM/PartOfSet"] = unicode(' /' + data['total_discs'])
			else:
				audio["WM/PartOfSet"] = unicode(
					d_no + '/' + data['total_discs'])

		if data.get("album_artist"):
			audio["WM/AlbumArtist"] = data["album_artist"]
		if data.get("composer"):
			audio["WM/Composer"] = data["composer"]
		if data.get("publisher"):
			audio["WM/Publisher"] = data["publisher"]
		if data.get("comments"):
			audio["WM/Comments"] = data["comments"]
		audio.save()

	def save_m4a_metadata(self, audio, data):
		""" Saves the given metadata for an M4A, AAC, or MP4 file.

		Metadata.save_m4a_metadata(Mutagen, dict)
		"""

		if data.get("title"):
			audio["\xa9nam"] = data["title"]
		if data.get("artist"):
			audio["\xa9ART"] = data["artist"]
		if data.get("album"):
			audio["\xa9alb"] = data["album"]
		if data.get("genre"):
			audio["\xa9gen"] = data["genre"]
		if data.get("year"):
			audio["\xa9day"] = data["year"]
		if data.get("track_number"):
			audio["trkn"] = [data["track_number"],data['total_tracks']]
		if data.get("album_artist"):
			audio["aART"] = data["album_artist"]
		if data.get("composer"):
			audio["\xa9wrt"] = data["composer"]
		if data.get("publisher"):
			audio["----:com.apple.iTunes:LABEL"] = data["publisher"]
		if data.get("comments"):
			audio["\xa9cmt"] = data["comments"]
		audio.save()

class Track(object):
	"""This serves as a container for the metadata of a song. It can be 
	passed around Beatbox so metadata can be easily accessed.
	"""

	def __init__(self, file_path):
		self.file_path = file_path
		self.set_all()

	def set_all(self):
		""" Gets all the metadata for the Track

		Track.set_all() -> None
		"""
		md = Metadata()
		audio, format = md.get_mutagen_parser(self.file_path)
		self.set_title(md.get_title(audio, format))
		self.set_artist(md.get_artist(audio, format))
		self.set_album(md.get_album(audio, format))
		self.set_year(md.get_date(audio, format))
		self.set_genre(md.get_genre(audio, format))
		self.set_album_artist(md.get_album_artist(audio, format))
		self.set_track_number(md.get_track_number(audio, format))
		self.set_total_tracks(md.get_total_tracks(audio, format))
		self.set_disc_number(md.get_disc_number(audio, format))
		self.set_total_discs(md.get_total_discs(audio, format))
		self.set_bpm(md.get_bpm(audio, format))
		self.set_composer(md.get_composer(audio, format))
		self.set_comment(md.get_comment(audio, format))
		self.set_publisher(md.get_publisher(audio, format))
		self.set_time(md.get_track_time(audio))
		self.set_date_modified(md.get_date_modified(self.file_path))
		self.set_size(md.get_size(self.file_path))
		self.set_bit_rate(md.get_bit_rate(audio))
		self.set_sample_rate(md.get_sample_rate(audio))
		self.set_format(format)
		self.set_channels(md.get_channels(audio))
		self.set_rating(md.get_rating(audio, format))

	def save_metadata(self, data):
		""" Saves the given metadata.

		Track.save_metadata(dict) -> boolean
		"""
		md = Metadata()
		audio, format = md.get_mutagen_parser(self.file_path)
		if format == 'mp3':
			md.save_mp3_metadata(self.file_path, data)
		elif format == 'flac' or format == 'ogg':
			md.save_flac_metadata(audio, data)
		elif format == 'wma':
			md.save_asf_metadata(audio, data)
		elif format == 'm4a':
			md.save_m4a_metadata(audio, data)
		self.set_all()
		return True

	def set_title(self, title):
		""" Sets title of the Track.

		Track.set_title(str) -> None
		"""
		if title == "":
			self.title = self.file_path.rsplit('/')[-1]
		else:
			self.title = title

	def set_artist(self, artist):
		""" Sets artist of the Track.

		Track.set_artist(str) -> None
		"""
		self.artist = artist

	def set_album(self, album):
		""" Sets album of the Track.

		Track.set_album(str) -> None
		"""
		self.album = album

	def set_year(self, year):
		""" Sets year of the Track.

		Track.set_year(str) -> None
		"""
		self.year = year

	def set_genre(self, genre):
		""" Sets genre of the Track.

		Track.set_genre(str) -> None
		"""
		self.genre = genre

	def set_album_artist(self, album_artist):
		""" Sets album artist of the Track.

		Track.set_album_artist(str) -> None
		"""
		self.album_artist = album_artist

	def set_track_number(self, track_number):
		""" Sets track number of the Track.

		Track.set_track_number(str) -> None
		"""
		self.track_number = track_number

	def set_total_tracks(self, total_tracks):
		""" Sets total number of tracks of the Track.

		Track.set_total_tracks(str) -> None
		"""
		self.total_tracks = total_tracks

	def set_disc_number(self, disc_number):
		""" Sets disc number of the Track.

		Track.set_disc_number(str) -> None
		"""
		self.disc_number = disc_number

	def set_total_discs(self, total_discs):
		""" Sets total number of discs of the Track.

		Track.set_total_discs(str) -> None
		"""
		self.total_discs = total_discs

	def set_bpm(self, bpm):
		""" Sets tehe beats per minute of the Track.

		Track.set_bpm(str) -> None
		"""
		self.bpm = bpm

	def set_composer(self, composer):
		""" Sets composer of the Track.

		Track.set_composer(str) -> None
		"""
		self.composer = composer

	def set_comment(self, comment):
		""" Sets the comment of the Track.

		Track.set_comment(str) -> None
		"""
		self.comment = comment

	def set_publisher(self, publisher):
		""" Sets publisher of the Track.

		Track.set_publisher(str) -> None
		"""
		self.publisher = publisher

	def set_date_modified(self, date_modified):
		""" Sets date modified of the Track.

		Track.set_date_modified(str) -> None
		"""
		self.date_modified = date_modified

	def set_size(self, size):
		""" Sets size of the Track.

		Track.set_size(str) -> None
		"""
		self.size = size

	def set_bit_rate(self, bit_rate):
		""" Sets bit rate of the Track.

		Track.set_bit_rate(str) -> None
		"""
		self.bit_rate = bit_rate

	def set_sample_rate(self, sample_rate):
		""" Sets sample rate of the Track.

		Track.set_sample_rate(str) -> None
		"""
		self.sample_rate = sample_rate

	def set_format(self, format):
		""" Sets format of the Track.

		Track.set_format(str) -> None
		"""
		self.format = format

	def set_channels(self, channels):
		""" Sets channels of the Track.

		Track.set_channels(str) -> None
		"""
		self.channels = channels

	def set_rating(self, rating):
		""" Sets rating of the Track.

		Track.set_rating(str) -> None
		"""
		self.rating = rating

	def set_time(self, time):
		""" Sets length of the Track.

		Track.set_time(str) -> None
		"""
		self.time = time

	def __str__(self):
		return "Title: " + self.title + "\nArtist: " + self.artist + \
		"\nAlbum: "\
		+ self.album + "\nYear: " + self.year + "\nGenre: " + self.genre + \
		"\nAlbum Artist: " + self.album_artist + "\nTrack Number: " \
		+ self.track_number + "\nTotal Tracks: " + self.total_tracks  + \
		"\nDisc Number: " + self.disc_number  + "\nTotal Discs: " \
		+ self.total_discs  + "\nBPM: " + self.bpm + "\nComposer: " + \
		self.composer + "\nPublisher: " + self.publisher + "\nTime: " + \
		self.time + "\nDate modified: " + self.date_modified + \
		"\nComment: " + self.comment + "\nSize: " + self.size + "\nBit Rate: " \
		+ self.bit_rate + "\nSample Rate: " + self.sample_rate + "\nFormat: "\
		 + self.format + "\nChannels: " + self.channels + \
		"\nRating: " + self.rating


if __name__ == "__main__":
	pass
