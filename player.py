from PySide import QtGui, QtCore
from PySide.phonon import Phonon
import sys
import metadata

playlist = []

### Settings variables
PLAYER_ICON_SIZE = 32
PLAYER_TEXT_SIZE = 12
PLAYER_COVER_SIZE = 100
MARGIN_SIZE = 10
FONT = 'Helvetica'

class PlayerGui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlayerGui, self).__init__(parent)

        self.metadata = metadata.Metadata()
        self.initUI()
        

    def initUI(self):

        self.current_song = None

        self.mediaObject = Phonon.MediaObject(self)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        pixel_map_cover = QtGui.QPixmap("Cover.jpg")
        self.album_art = QtGui.QLabel(self)
        self.album_art.setPixmap(pixel_map_cover.scaled(PLAYER_COVER_SIZE, PLAYER_COVER_SIZE, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation ))

        self.track_name = QtGui.QLabel("", self)
        self.track_name.move(2 * MARGIN_SIZE + PLAYER_COVER_SIZE, MARGIN_SIZE)
        self.track_name.setFont(QtGui.QFont(FONT, PLAYER_TEXT_SIZE))

        self.album_name = QtGui.QLabel("", self)
        self.album_name.move(2 * MARGIN_SIZE + PLAYER_COVER_SIZE, MARGIN_SIZE + 35)
        self.album_name.setFont(QtGui.QFont(FONT, PLAYER_TEXT_SIZE))

        self.artist_name = QtGui.QLabel("", self)
        self.artist_name.move(2 * MARGIN_SIZE + PLAYER_COVER_SIZE, MARGIN_SIZE + 70)
        self.artist_name.setFont(QtGui.QFont(FONT, PLAYER_TEXT_SIZE))

        self.track_slider = Phonon.SeekSlider(self)
        self.track_slider.setGeometry(-10, 90, 310, 20)

        self.load_button = PlayerButton(self)
        self.load_button.setImage("images/load.png")
        self.load_button.setGeometry (MARGIN_SIZE/2, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)
        self.load_button.released.connect(self.choose_song)

        self.back_button = PlayerButton(self)
        self.back_button.setImage("images/back.png")
        self.back_button.setGeometry (MARGIN_SIZE + 2*PLAYER_ICON_SIZE, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)
        self.back_button.pressed.connect(self.back_button_pressed)
        self.back_button.released.connect(self.back_button_released)

        self.play_button = PlayerButton(self)
        self.play_button.setImage("images/play.png")
        self.play_button.setGeometry (MARGIN_SIZE + 4*PLAYER_ICON_SIZE, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)
        self.play_button.pressed.connect(self.handlePlayPauseButtonPressed)
        self.play_button.released.connect(self.handlePlayPauseButtonReleased)
        self.play_button.released.connect(self.handlePlayPauseButton)

        self.forward_button = PlayerButton(self)
        self.forward_button.setImage("images/forward.png")
        self.forward_button.setGeometry (MARGIN_SIZE + 6*PLAYER_ICON_SIZE, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.volume_button = PlayerButton(self)
        self.volume_button.setImage("images/volume3.png")
        self.volume_button.setGeometry (MARGIN_SIZE + 8*PLAYER_ICON_SIZE, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.setGeometry(MARGIN_SIZE, MARGIN_SIZE, 400, 180)


    def choose_song(self):
        self.load_song(QtGui.QFileDialog.getOpenFileName(self, "Choose a song")[0])
        
    def load_song(self, file):
        if file != "": ##If the user cancels the file dialog it returns as an empty string.
            self.mediaObject.setCurrentSource(Phonon.MediaSource(self.current_song))
            self.track_slider.setMediaObject(self.mediaObject)
            self.setPlayButtonState("paused")
            self.loadMetadata()

    def getAlbumArt(self):
        artwork = self.metadata.get_album_cover(self.current_song)
        if artwork:
            print "writing image"
            with open('temp/cover.jpg', 'wb') as img:
                img.write(artwork) # write artwork to new image
            self.setAlbumArt(True)
        else:
            self.setAlbumArt(False)
    
    def setAlbumArt(self, album_art_exists):

        if album_art_exists:
            pixel_map = QtGui.QPixmap("temp/cover.jpg")
        else:
            pixel_map = QtGui.QPixmap("Cover.jpg")

        self.album_art.setPixmap(pixel_map.scaled(PLAYER_COVER_SIZE, PLAYER_COVER_SIZE, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation ))


    def loadMetadata(self):
        md = self.metadata.get_now_playing_metadata(self.current_song)
        self.setArtistText(md[0])
        self.setTrackText(md[1])
        self.setAlbumText(md[2])
        self.getAlbumArt()

    def setArtistText(self, artist):
        self.artist_name.setText(artist)
        self.artist_name.adjustSize()

    def setTrackText(self, track):
        self.track_name.setText(track)
        self.track_name.adjustSize()

    def setAlbumText(self, album):
        self.album_name.setText(album)
        self.album_name.adjustSize()

    def handlePlayPauseButton(self):

        if self.mediaObject.state() == Phonon.PlayingState:
            state = self.pauseSong()
        else:
            state = self.playSong()
        # self.setPlayButtonState(state)

    def handlePlayPauseButtonPressed(self):

        if self.mediaObject.state() == Phonon.PlayingState:
            self.play_button.setImage('images/pause_pressed.png')
        else:
            self.play_button.setImage('images/play_pressed.png')

    def handlePlayPauseButtonReleased(self):

        if self.mediaObject.state() == Phonon.PlayingState:
            self.play_button.setImage('images/play.png')
        else:
            self.play_button.setImage('images/pause.png')


    def playSong(self):
        if self.mediaObject.state() == Phonon.PausedState:
            self.mediaObject.play()
            return "playing"
        elif self.current_song != None:
            self.mediaObject.play()
            return "playing"
        else:
            return "paused"

    def pauseSong(self):
        self.mediaObject.pause()
        return "paused"

    def setPlayButtonState(self, state):
        if state == "paused":
            self.play_button.setImage("images/play.png")
        else:
            self.play_button.setImage("images/pause.png")

    def back_button_pressed(self):
        self.back_button.setImage('images/back_pressed.png')

    def back_button_released(self):
        self.back_button.setImage('images/back.png')
        if self.mediaObject.state() == Phonon.PausedState:
            self.mediaObject.stop()
        if self.mediaObject.state() == Phonon.PlayingState:
            self.mediaObject.stop()
            self.mediaObject.play()

    def trackSliderMoved(self):
        position = self.track_slider.value()

class PlayerButton(QtGui.QAbstractButton):
    """
    This is a subclass of PyQt's Button widget that displays a card and text.
    The paintEvent will check the button text to see if it should display the 
    back or front of the card.
    """

    def __init__(self, parent=None):
        super(PlayerButton, self).__init__(parent)

    def setImage(self, image):
        """ Set the image of the button
        setImage(self, str) -> None
        """       
        self.image = image
        self.repaint()

    def paintEvent(self, event):
        """ The function called when self.repaint() is called. Updates the
        widget with the new image.
        paintEvent(self, event) -> None
        """
        painter = QtGui.QPainter(self)
        pm = QtGui.QPixmap(self.image)
        painter.drawPixmap(event.rect(), pm)
