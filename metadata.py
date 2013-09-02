from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen import *

class Metadata():

	def get_metadata(self, path):

		if path.endswith(".mp3"):
			audio = MP3(path)
			format = "mp3"
		elif path.endswith(".flac"):
			audio = FLAC(path)
			format = "flac"
		elif path.endswith(".ogg"):
			audio = OggVorbis(path)
			format = "ogg"

		artist = self.get_artist(audio, format)
		title = self.get_title(audio, format)
		album = self.get_album(audio, format)
		date = self.get_date(audio, format)
		genre = self.get_genre(audio, format)
		track_number = self.get_track_number(audio, format)
		total_tracks = self.get_total_tracks(audio, format)
		disc_number = self.get_disc_number(audio, format)
		total_discs = self.get_total_discs(audio, format)
		album_artist = self.get_album_artist(audio, format)
		publisher = self.get_publisher(audio, format)

		metadata = {'Artist':artist,
			'Title':title,
			'Album':album,
			'Year':date,
			'Genre':genre,
			'Track Number':track_number,
			'Total Tracks':total_tracks,
			'Disc Number':disc_number,
			'Total Discs':total_discs,
			'Album Artist':album_artist,
			'Publisher':publisher,
			'File Path': path}
		
		return metadata
		

	def get_now_playing_metadata(self, path):
		##Only mp3 and ogg for now until i work out a way to get other formats to playback.
		if path.endswith(".mp3"):
			audio = MP3(path)
			format = "mp3"
		elif path.endswith(".ogg"):
			audio = OggVorbis(path)
			format = "ogg"
		elif path.endswith(".flac"):
			audio = FLAC(path)
			format = "flac"
		artist = self.get_artist(audio, format)
		title = self.get_title(audio, format)
		album = self.get_album(audio, format)
		return (artist, title, album)

	def get_playlist_metadata(self, path):
		##Only mp3 and ogg for now until i work out a way to get other formats to playback.
		if path.endswith(".mp3"):
			audio = MP3(path)
			format = "mp3"
		elif path.endswith(".ogg"):
			audio = OggVorbis(path)
			format = "ogg"
		elif path.endswith(".flac"):
			audio = FLAC(path)
			format = "flac"
		artist = self.get_artist(audio, format)
		title = self.get_title(audio, format)
		return (artist, title)

	def get_artist(self, audio, format):
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

	def get_title(self, audio, format):
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

	def get_album(self, audio, format):
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

	def get_date(self, audio, format):
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

	def get_genre(self, audio, format):
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

	def get_track_number(self, audio, format):
		if format == "mp3":
			try:
				return audio["TRCK"][0]
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

	def get_total_tracks(self, audio, format):
		if format == "mp3":
			try:
				return audio["TRCK"][1]
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

	def get_disc_number(self, audio, format):
		if format == "mp3":
			return ""
		elif format == "flac":
			try:
				return audio["discnumber"][0]
			except:
				return ""
		elif format == "ogg":
			return ""

	def get_total_discs(self, audio, format):
		if format == "mp3":
			return ""
		elif format == "flac":
			try:
				return audio["disctotal"][0]
			except:
				return ""
		elif format == "ogg":
			return ""

	def get_album_artist(self, audio, format):
		if format == "mp3":
			return ""
		elif format == "flac":
			try:
				return audio["album artist"][0]
			except:
				return ""
		elif format == "ogg":
			return ""

	def get_publisher(self, audio, format):
		if format == "mp3":
			try:
				return audio["TPUB"][0]
			except:
				return ""
		elif format == "flac":
			try:
				return audio["publisher"][0]
			except:
				return ""
		elif format == "ogg":
			return ""

	def get_album_cover(self, path):
		md = mutagen.File(path)
		try:
			return md.tags['APIC:'].data
		except:
			return None