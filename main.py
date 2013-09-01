from PySide import QtGui, QtCore
from PySide.phonon import Phonon
import sys
import metadata
import phonon
import player



### FOR TESTING ###
playlist = ['/Users/luke/Downloads/King Krule/03 Portrait in Black and Blue.mp3', '/Users/luke/Downloads/King Krule/04 Lead Existence.mp3']
MAIN_WINDOW_MARGIN = 50
MAIN_WINDOW_WIDTH = 1000
MAIN_WINDOW_HEIGHT = 700
PLAYER_WINDOW_WIDTH = 320
PLAYER_WINDOW_HEIGHT = 180
PLAYER_ICON_SIZE = 32
PLAYER_TEXT_SIZE = 12
PLAYER_COVER_SIZE = 100
MARGIN_SIZE = 10
FONT = 'Helvetica'
### ----------- ###


class MainGui(QtGui.QMainWindow):
    def __init__(self):
        super(MainGui, self).__init__()
        self.phonon = phonon.PhononInstance(self)
        self.media_object = self.phonon.create_media_object()
        self.metadata = metadata.Metadata()
        self.player_gui = PlayerGui(self)
        self.playlist_gui = PlaylistGui(self)
        self.create_main_window()
        
    def create_main_window(self):
        """ Creates the main window of the application, sets the size and
        position and brings it to the front.

        create_main_window(self) -> None
        """
        self.setGeometry(MAIN_WINDOW_MARGIN, MAIN_WINDOW_MARGIN,\
         MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.setWindowTitle('Beatbox')
        self.show()
        self.raise_()

class PlayerGui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlayerGui, self).__init__(parent)

        self.parent = parent
        self.media_object = self.parent.media_object
        self.metadata = self.parent.metadata
        self.player = player.Player(self)
        self.create_player_window()
        

    def create_player_window(self):

        cover_pm = QtGui.QPixmap("images/cover.jpg")
        self.album_art = QtGui.QLabel(self)
        self.album_art.setPixmap(cover_pm.scaled(PLAYER_COVER_SIZE, PLAYER_COVER_SIZE, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))

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

        self.load_button = ImageButton(self, "images/load.png", "images/load_pressed.png", self.open_file)
        self.load_button.setGeometry (0 , PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.back_button = ImageButton(self, "images/back.png", "images/back_pressed.png", self.back_button_clicked)
        self.back_button.setGeometry (PLAYER_WINDOW_WIDTH/7, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.play_button = ImageButton(self, "images/play.png", "images/play_pressed.png", self.play_button_clicked)
        self.play_button.setGeometry (PLAYER_WINDOW_WIDTH/7 * 2, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.forward_button = ImageButton(self, "images/forward.png", "images/forward_pressed.png", self.forward_button_clicked)
        self.forward_button.setGeometry (PLAYER_WINDOW_WIDTH/7 * 3, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.shuffle_button = ImageButton(self, "images/shuffle.png", "images/forward_pressed.png", self.shuffle_button_clicked)
        self.shuffle_button.setGeometry (PLAYER_WINDOW_WIDTH/7 * 4, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.repeat_button = ImageButton(self, "images/repeat.png", "images/forward_pressed.png", self.repeat_button_clicked)
        self.repeat_button.setGeometry (PLAYER_WINDOW_WIDTH/7 * 5, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.volume_button = ImageButton(self, "images/volume3.png", "images/load_pressed.png", self.volume_button_clicked)
        self.volume_button.setGeometry (PLAYER_WINDOW_WIDTH/7 * 6, PLAYER_COVER_SIZE + 2*MARGIN_SIZE, PLAYER_ICON_SIZE, PLAYER_ICON_SIZE)

        self.setGeometry(MARGIN_SIZE, MARGIN_SIZE, 400, 180)


    def open_file(self):
        """ Opens a file dialog where the user can select a song to play.

        """
        song_file = QtGui.QFileDialog.getOpenFileName(self, "Choose a song")[0]
        self.load_song(song_file)
        
    def load_song(self, song_file):
        if song_file != "": ##If the user cancels the file dialog it returns as an empty string.
            self.media_object.setCurrentSource(Phonon.MediaSource(song_file))
            self.track_slider.setMediaObject(self.media_object)
            self.player.load_metadata(song_file)

    def set_album_art(self, path):
        if path != '':
            pixel_map = QtGui.QPixmap(path)
        else:
            pixel_map = QtGui.QPixmap("Cover.jpg")

        self.album_art.setPixmap(pixel_map.scaled(PLAYER_COVER_SIZE, PLAYER_COVER_SIZE, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation ))

    def set_artist_name(self, artist):
        self.artist_name.setText(artist)
        self.artist_name.adjustSize()

    def set_track_name(self, track):
        self.track_name.setText(track)
        self.track_name.adjustSize()

    def set_album_name(self, album):
        self.album_name.setText(album)
        self.album_name.adjustSize()

    def play_button_clicked(self):
        if self.media_object.state() == Phonon.PlayingState:
            self.pauseSong()
            self.play_button.setImage('images/play.png')
            self.play_button.set_pressed_image('images/play_pressed.png')  
        else:
            self.playSong()
            self.play_button.setImage('images/pause.png')
            self.play_button.set_pressed_image('images/pause_pressed.png')

    def playSong(self):
        if self.media_object.state() == Phonon.PausedState:
            self.media_object.play()
        elif self.media_object.currentSource != None:
            self.media_object.play()

    def pauseSong(self):
        self.media_object.pause()

    def back_button_clicked(self):
        if self.media_object.state() == Phonon.PausedState:
            self.media_object.stop()
        if self.media_object.state() == Phonon.PlayingState:
            self.media_object.stop()
            self.media_object.play()

    def trackSliderMoved(self):
        position = self.track_slider.value()

    def forward_button_clicked(self):
        pass

    def shuffle_button_clicked(self):
        pass

    def repeat_button_clicked(self):
        pass

    def volume_button_clicked(self):
        pass


class PlaylistGui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlaylistGui, self).__init__(parent)
        self.parent = parent
        self.create_playlist_window()
        

    def create_playlist_window(self):

        self.playlist_widget = QtGui.QListWidget(self)
        self.playlist_widget.resize(300, 300)
        self.load_playlist(playlist)
        self.playlist_widget.doubleClicked.connect(self.playlist_item_double_clicked)
        self.setGeometry(10, 190, 400, 400) ### WHY THE LAST TWO VALS?


    def load_playlist(self, playlist):
        """ Loads playlist into the playlist listview"""
        for item in playlist:
           self.playlist_widget.addItem(item)

    def playlist_item_double_clicked(self, item):
        print item.data()
        self.parent.player_gui.load_song(item.data())
        self.parent.player_gui.playSong()

class ImageButton(QtGui.QAbstractButton):
    """
    This is a subclass of PyQt's Button widget that displays a card and text.
    The paintEvent will check the button text to see if it should display the 
    back or front of the card.
    """

    def __init__(self, parent, image, pressed_image, function):
        super(ImageButton, self).__init__(parent)
        self.image = image
        self.released_image = image
        self.pressed_image = pressed_image
        self.setImage(image)
        self.function = function

    def setImage(self, image):
        """ Set the image of the button
        setImage(self, str) -> None
        """       
        self.image = image
        self.repaint()

    def set_pressed_image(self, image):
        self.pressed_image = image

    def paintEvent(self, event):
        """ The function called when self.repaint() is called. Updates the
        widget with the new image.
        paintEvent(self, event) -> None
        """
        painter = QtGui.QPainter(self)
        pm = QtGui.QPixmap(self.image)
        painter.drawPixmap(event.rect(), pm)

    def mousePressEvent(self, event):
        self.setImage(self.pressed_image)

    def mouseReleaseEvent(self, event):
        self.setImage(self.released_image)
        self.function()



def main():

    application = QtGui.QApplication(sys.argv)
    ex = MainGui()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()