from PySide.phonon import Phonon

class PhononInstance():
	def __init__(self, application):
		self.application = application

	def create_media_object(self):
		""" Creates an instance of Phonon for playing songs in the parent
		application.

		create_media_object(self) -> Phonon.MediaObject
		"""
		media_object = Phonon.MediaObject(self.application)
		audio_output = Phonon.AudioOutput(Phonon.MusicCategory, self.application)
		Phonon.createPath(media_object, audio_output)
		return media_object