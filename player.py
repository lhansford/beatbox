import metadata

class Player():

    def __init__(self, parent):
        self.parent = parent
        self.metadata = metadata.Metadata()

    def load_metadata(self, song_file):
        md = self.metadata.get_now_playing_metadata(song_file)
        self.parent.set_artist_name(md[0])
        self.parent.set_track_name(md[1])
        self.parent.set_album_name(md[2])
        self.get_album_art(song_file)

    def get_album_art(self, song_file):
        artwork = self.metadata.get_album_cover(song_file)
        if artwork:
            with open('temp/cover.jpg', 'wb') as img:
                img.write(artwork) # write artwork to new image
            self.parent.set_album_art("temp/cover.jpg")
        # elif:
        #     ### Implement a .jpg search here and return that file
        #     self.parent.set_album_art('')
        else:
            self.parent.set_album_art('')
