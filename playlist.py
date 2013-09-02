class Playlist(object):

	def __init__(self, parent):
		self.parent = parent
		self.playlist = []

	def insert_in_playlist(self, file_name, index):
		self.playlist.insert(index, file_name)

	def append_to_playlist(self, file_name):
		self.playlist.append(file_name)

	def get_playlist_length(self):
		return len(self.playlist)

	def get_playlist_item(self, index):
		return self.playlist[index]

	def set_current_position(self, index):
		self.current_position = index

	def get_current_position(self):
		return self.current_position