from PySide import QtGui, QtCore
from PySide.phonon import Phonon
import sys
import metadata
import player

playlist = ['/Users/luke/Downloads/King Krule/03 Portrait in Black and Blue.mp3', '/Users/luke/Downloads/King Krule/04 Lead Existence.mp3']

class PlaylistGui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlaylistGui, self).__init__(parent)

        self.metadata = metadata.Metadata()
        self.initUI()
        

    def initUI(self):

        self.playlist_widget = QtGui.QListWidget(self)
        self.playlist_widget.resize(300, 200)
        self.load_playlist(playlist)
        self.playlist_widget.doubleClicked.connect(self.playlist_item_double_clicked)
        self.setGeometry(10, 190, 400, 400) ### WHY THE LAST TWO VALS?


    def load_playlist(self, playlist):
        """ Loads playlist into the playlist listview"""

        for item in playlist:
           self.playlist_widget.addItem(item)

    def playlist_item_double_clicked(self, item):
        print item.data()
        self.player.load_song(item.data())



### NEED THIS?!
class PlayerButton(QtGui.QAbstractButton):
    """
    This is a subclass of PyQt's Button widget that displays a card and text.
    The paintEvent will check the button text to see if it should display the 
    back or front of the card.
    """

    def __init__(self, parent=None):
        super(PlayerButton, self).__init__(parent)

    def setImage(self, image):
        self.image = image
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pm = QtGui.QPixmap(self.image)
        painter.drawPixmap(event.rect(), pm)
