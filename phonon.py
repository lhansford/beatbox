from PySide.phonon import Phonon

class PhononInstance():
	def __init__(self, parent):
		self.parent = parent

	def create_media_object(self):
		""" Creates an instance of Phonon for playing songs in the parent
		application.

		create_media_object(self) -> Phonon.MediaObject
		"""
		media_object = Phonon.MediaObject(self.parent)
		audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self.parent)
		Phonon.createPath(media_object, audio_output)
		return media_object