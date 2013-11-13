# -◊- coding: utf-8 -◊-
"""
Beatbox 1.0

Copyright (C) 2013 Luke Hansford - l.s.hansford@gmail.com

DESCRIPTION

Beatbox is a multi-platform music player developed in Python. It's capable
of playing files in the formats MP3, FLAC, OGG, M4A, MP4, AAC and WMA, as long 
as the codecs are installed on the system running the application.

LICENSE

I, Luke Hansford, Hereby grant the rights to distribute, modify, and edit the
source to Beatbox 1.0, on the condition that this agreement, and my ownership
of the code contained herewithin be maintained.

Furthurmore, I grant the right to use excerpts from the source to Beatbox 1.0
without express permission, with exclusion of commercial application.
"""

#Standard libraries
import sys
import os.path

#3rd party libraries
import requests
from bs4 import BeautifulSoup
from PySide import QtGui, QtCore, QtWebKit
from PySide.phonon import Phonon

#Beatbox libraries
import metadata
import phonon
import player
import playlist
import library
import preferences
import localisation_en
import localisation_zh


### ----------- ###
MAIN_WINDOW_MARGIN = 50
MAIN_WINDOW_WIDTH = 1150
MAIN_WINDOW_HEIGHT = 720
PLAYER_WINDOW_WIDTH = 320
PLAYER_WINDOW_HEIGHT = 160
PLAYER_ICON_SIZE = 32
PLAYER_TEXT_SIZE = 12
PLAYER_COVER_SIZE = 100
MARGIN_SIZE = 10
## IMAGE PATHS ##
DEFAULT_ALBUM_COVER = os.path.abspath("images/cover.png")
SPLASH_IMAGE = os.path.abspath('images/splash.png')
LOAD_IMAGE = os.path.abspath('images/load.png')
LOAD_PRESSED_IMAGE = os.path.abspath('images/load_pressed.png')
PREV_IMAGE = os.path.abspath('images/back.png')
PREV_PRESSED_IMAGE = os.path.abspath('images/back_pressed.png')
PLAY_IMAGE = os.path.abspath('images/play.png')
PLAY_PRESSED_IMAGE = os.path.abspath('images/play_pressed.png')
PAUSE_IMAGE = os.path.abspath('images/pause.png')
PAUSE_PRESSED_IMAGE = os.path.abspath('images/pause_pressed.png')
NEXT_IMAGE = os.path.abspath('images/forward.png')
NEXT_PRESSED_IMAGE = os.path.abspath('images/forward_pressed.png')
SHUFFLE_IMAGE = os.path.abspath('images/shuffle.png')
SHUFFLE_PRESSED_IMAGE = os.path.abspath('images/shuffle_pressed.png')
REPEAT_IMAGE = os.path.abspath('images/repeat.png')
REPEAT_PRESSED_IMAGE = os.path.abspath('images/repeat_pressed.png')
VOLUME_IMAGE = os.path.abspath('images/volume3.png')
MUTE_IMAGE = os.path.abspath('images/mute.png')
####
FONT = 'Helvetica'
TABLE_FONT = 'Helvetica'
TABLE_FONT_SIZE = 12
SPLASH_TEXT_COLOUR = QtGui.QColor(255, 255, 255) #RGB
BACKGROUND_COLOUR = QtGui.QColor(176, 224, 245) #RGB
INVALID_FILE_FONT_COLOUR = QtGui.QColor(168, 168, 168) #RGB
### ----------- ###

class MainGui(QtGui.QMainWindow):
    def __init__(self, splash):
        super(MainGui, self).__init__()
        self.splash = splash
        self.create_main_window()
        self.splash.close()
        
        
    def create_main_window(self):
        """ Creates the main window of the application, sets the size and
        position and brings it to the front.

        create_main_window(self) -> None
        """
        self.preferences = preferences.Preferences(self)
        self.beatbox_gui = BeatboxGui(self)
        self.localisation = self.beatbox_gui.localisation
        
        self.setCentralWidget(self.beatbox_gui)

        self.setGeometry(MAIN_WINDOW_MARGIN, MAIN_WINDOW_MARGIN,\
         MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        self.setPalette(self.create_palette())
        self.menu_bar = QtGui.QMenuBar()
        self.create_menu(self.menu_bar)
        self.setMenuBar(self.menu_bar)
        self.setWindowTitle('Beatbox')
        self.show()
        self.raise_()

    def create_menu(self, menu_bar):
        """ Adds menus and items to the given QMenuBar.

        MainGui.create_menu(QMenuBar) -> None
        """
        file_menu = menu_bar.addMenu(self.localisation.FILE_STRING)
        open_file_action = self.create_menu_item(
            self.localisation.OPEN_FILE_STRING, 'Ctrl+O',
             self.beatbox_gui.player_gui.open_file)
        file_menu.addAction(open_file_action)

        # file_menu.addAction(self.localisation.ADD_TO_LIBRARY_STRING)

        edit_menu = menu_bar.addMenu(self.localisation.EDIT_STRING)
        # edit_menu.addAction(self.localisation.REMOVE_ITEM_STRING)
        self.edit_metadata_action = self.create_menu_item(
            self.localisation.EDIT_METADATA_STRING,
             'Ctrl+I', self.open_metadata_editor)
        edit_menu.addAction(self.edit_metadata_action)
        preferences_action = self.create_menu_item(
            self.localisation.PREFERENCES_STRING,
             'Ctrl+P', self.open_preferences_window)
        edit_menu.addAction(preferences_action)

        view_menu = menu_bar.addMenu(self.localisation.VIEW_STRING)

        view_library_action = self.create_menu_item(
            self.localisation.LIBRARY_STRING, 'Ctrl+1',
             self.beatbox_gui.tabview_gui.show_library_view)
        view_menu.addAction(view_library_action)
        view_artist_info_action = self.create_menu_item(
            self.localisation.ARTIST_INFO_STRING, 'Ctrl+2',
             self.beatbox_gui.tabview_gui.show_artist_info_view)
        view_menu.addAction(view_artist_info_action)
        view_lyrics_action = self.create_menu_item(
            self.localisation.LYRICS_STRING, 'Ctrl+3',
             self.beatbox_gui.tabview_gui.show_lyrics_view)
        view_menu.addAction(view_lyrics_action)
        controls_menu = menu_bar.addMenu(self.localisation.CONTROLS_STRING)
        play_action = self.create_menu_item(self.localisation.PLAY_PAUSE_STRING,
         'Space', self.beatbox_gui.player_gui.play_button_clicked)
        controls_menu.addAction(play_action)
        previous_action = self.create_menu_item(
            self.localisation.PREVIOUS_TRACK_STRING, 'Ctrl+Left',
             self.beatbox_gui.player_gui.back_button_clicked)
        controls_menu.addAction(previous_action)
        next_action = self.create_menu_item(self.localisation.NEXT_TRACK_STRING,
         'Ctrl+Right', self.beatbox_gui.player_gui.forward_button_clicked)
        controls_menu.addAction(next_action)
        # controls_menu.addAction(self.localisation.SHUFFLE_ON_STRING)
        # controls_menu.addAction(self.localisation.REPEAT_ON_STRING)
        # controls_menu.addAction(self.localisation.VOLUME_UP_STRING)
        # controls_menu.addAction(self.localisation.VOLUME_DOWN_STRING)

        window_menu = menu_bar.addMenu(self.localisation.WINDOW_STRING)
        minimise_action = self.create_menu_item(
            self.localisation.MINIMISE_STRING, 'Ctrl+M', self.minimise_window)
        window_menu.addAction(minimise_action)
        # help_menu = menu_bar.addMenu(self.localisation.HELP_STRING)
        
    def create_menu_item(self, name, shortcut, triggered_function):
        """ Creates a QAction to go in the menu. Receives a name, keyboard
        shortcut to call the action, and a function to run when the action is
        called.

        MainGui.create_menu_item(str, str/Qt.Shortcut, function) -> QAction
        """

        action = QtGui.QAction(name, self)
        action.setShortcut(shortcut)
        action.triggered.connect(triggered_function)
        return action

    def reset_menu(self):
        """ Deletes the menu and creates a new one. Called if the language is
        changed.

        MainGui.reset_menu() -> None
        """
        self.menu_bar.clear()
        self.create_menu(self.menu_bar)

    def create_palette(self):
        """ Creates a QPalette to change the colour of the application.

        MainGui.create_palette() -> QPalette
        """

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, BACKGROUND_COLOUR)
        return palette

    def minimise_window(self):
        """ Minimizes the main window.

        MainGui.minimise_window() -> None
        """
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def open_preferences_window(self):
        """ Creates a PreferencesDialog and opens it.

        MainGui.open_preferences_window() -> None
        """
        preferences_dialog = PreferencesDialog(self)
        preferences_dialog.exec_()

    def open_metadata_editor(self):
        """ Checks if songs are selected and then opens a window in which the
        songs' metadata can be edited.

        MainGui.open_metadata_editor() -> None
        """

        if self.beatbox_gui.playlist_gui.playlist_widget.hasFocus():
            if self.beatbox_gui.playlist_gui.playlist_widget.selectedIndexes\
             > 0:
                metadata_editor = MetadataEditor(self)
                metadata_editor.exec_()
        else:
            if self.beatbox_gui.tabview_gui.library_gui.selected_rows() > 0:
                metadata_editor = MetadataEditor(self)
                metadata_editor.exec_()

class BeatboxGui(QtGui.QWidget):
    """ This is the main widget of the app, which is situated in the main
    window. It's only function is to load the other widgets within it, and to
    control the splash screen as the app is loaded.
    """

    def __init__(self, parent=None):
        super(BeatboxGui, self).__init__(parent)
        self.parent = parent
        self.preferences = self.parent.preferences
        self.set_language(self.preferences.get_language_pref())
        self.splash = self.parent.splash

        self.splash.showMessage(
            self.localisation.LOADING_AUDIO_STRING, color=SPLASH_TEXT_COLOUR)
        QtCore.QCoreApplication.processEvents()

        self.phonon = phonon.PhononInstance(self)
        self.media_object = self.phonon.create_media_object()
        # self._media_object = Phonon.MediaObject()
        # self._media_object.setTickInterval(1000) # Set the tick time to 1 sec
        # self._media_object.tick.connect(self.on_tick)
        # self._media_object.prefinishMarkReached.connect(self.halfway_reached)
        # self.audio_output = Phonon.AudioOutput(
        #     Phonon.MusicCategory, self.parent)
        # Phonon.createPath(self._media_object, self.audio_output)

        self.playlist = playlist.Playlist(self)
        self.status_bar = StatusBar(self)
        self.splash.showMessage(
            self.localisation.LOADING_PLAYER_STRING, color=SPLASH_TEXT_COLOUR)
        QtCore.QCoreApplication.processEvents()

        self.player_gui = PlayerGui(self)
        self.splash.showMessage(
            self.localisation.LOADING_PLAYLIST_STRING, color=SPLASH_TEXT_COLOUR)
        QtCore.QCoreApplication.processEvents()
        self.playlist_gui = PlaylistGui(self)
        self.splash.showMessage(
            self.localisation.LOADING_LIBRARY_STRING, color=SPLASH_TEXT_COLOUR)
        QtCore.QCoreApplication.processEvents()
        self.tabview_gui = TabviewGui(self) 

        grid_layout = QtGui.QGridLayout()
        grid_layout.setColumnMinimumWidth(0, PLAYER_WINDOW_WIDTH)
        grid_layout.setRowMinimumHeight(0, PLAYER_WINDOW_HEIGHT)
        grid_layout.setColumnStretch(1,1)
        grid_layout.setRowStretch(1,1)
        grid_layout.addWidget(self.player_gui, 0, 0)
        grid_layout.addWidget(self.playlist_gui, 1, 0)
        grid_layout.addWidget(self.tabview_gui, 0, 1 , 2, 1)
        grid_layout.addWidget(self.status_bar, 2, 0, 1, 2 )
        self.setLayout(grid_layout)

    def get_language(self):
        """ Get the current language.

        BeatboxGui.get_language() -> str
        """
        return self._language

    def set_language(self, language):
        """ Set the language for Beatbox

        BeatboxGui.set_language(str) -> None
        """
        if language == 'English':
            self._language = 'English'
            self.localisation = localisation_en
        elif language == u"汉语":
            self._language = u"汉语"
            self.localisation = localisation_zh

    def reload_text(self):
        """ Reloads all strings in the app. Called when the language has been
        changed.

        BeatboxGui.reload_text() -> None
        """
        self.parent.localisation = self.localisation
        self.parent.reset_menu()

        self.playlist_gui.localisation = self.localisation
        self.player_gui.localisation = self.localisation

        self.tabview_gui.localisation = self.localisation
        self.tabview_gui.library_gui.localisation = self.localisation
        self.tabview_gui.library_gui.library_widget.localisation =\
         self.localisation

        self.tabview_gui.tabview_widget.setTabText(
            0, self.localisation.LIBRARY_STRING)
        self.tabview_gui.tabview_widget.setTabText(
            1, self.localisation.ARTIST_INFO_STRING)
        self.tabview_gui.tabview_widget.setTabText(
            2, self.localisation.LYRICS_STRING)
        self.tabview_gui.library_gui.set_library_status()

class PlayerGui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlayerGui, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.playlist = self.parent.playlist
        self.media_object = self.parent.media_object
        self.phonon = self.parent.phonon
        self.player = player.Player(self)
        self.media_object.aboutToFinish.connect(self.player.song_ended)
        self.create_player_window()
        self.load_preferences()
        
    def create_player_window(self):
        """ Creates the children widgets for PlayerGui and apllies settings to
        them. The widgets are - album_art(QLabel), track_name(QLabel),
        artist_name(QLabel), album_name(QLabel), track_time(QLabel),
        track_slider(Phonon.SeekSlider), load_button(ImageButton),
        back_button(ImageButton), play_button(ImageButton), 
        forward_button(ImageButton), shuffle_button(ToggleButton),
        repeat_button(ToggleButton), volume_button(ImageButton).

        PlayerGui.create_player_window() -> None
        """
        
        layout = QtGui.QVBoxLayout(self)

        player_layout = QtGui.QGridLayout()
        layout.addLayout(player_layout)
        player_layout.setColumnStretch(1,1)
        player_layout.setColumnMinimumWidth(0, PLAYER_COVER_SIZE)
        player_layout.setRowMinimumHeight(0, PLAYER_COVER_SIZE/3)
        player_layout.setRowMinimumHeight(1, PLAYER_COVER_SIZE/3)
        player_layout.setRowMinimumHeight(2, PLAYER_COVER_SIZE/3)

        self.album_art = QtGui.QLabel(self)
        pixel_map = QtGui.QPixmap(DEFAULT_ALBUM_COVER)
        self.album_art.setPixmap(pixel_map.scaled(PLAYER_COVER_SIZE,\
         PLAYER_COVER_SIZE, QtCore.Qt.KeepAspectRatio,\
          QtCore.Qt.SmoothTransformation))
        player_layout.addWidget(self.album_art, 0, 0, 3, 0)

        self.track_name = QtGui.QLabel("", self)
        self.track_name.setWordWrap(True)
        player_layout.addWidget(self.track_name, 0, 1)

        self.artist_name = QtGui.QLabel("", self)
        self.artist_name.setWordWrap(True)
        player_layout.addWidget(self.artist_name, 1, 1)

        self.album_name = QtGui.QLabel("", self)
        self.album_name.setWordWrap(True)
        player_layout.addWidget(self.album_name, 2, 1)

        self.set_font_settings(FONT, PLAYER_TEXT_SIZE)

        time_layout = QtGui.QHBoxLayout()
        layout.addLayout(time_layout)
        self.track_slider = Phonon.SeekSlider(self)
        time_layout.addWidget(self.track_slider)

        self.track_time = QtGui.QLabel("-00:00", self)
        self.track_time.setAlignment(QtCore.Qt.AlignRight)
        time_layout.addWidget(self.track_time)

        button_layout = QtGui.QHBoxLayout()
        layout.addLayout(button_layout)


        self.load_button = ImageButton(
            self, LOAD_IMAGE, LOAD_PRESSED_IMAGE, self.open_file)
        self.load_button.setFixedWidth(PLAYER_ICON_SIZE)
        self.load_button.setFixedHeight(PLAYER_ICON_SIZE)
        button_layout.addWidget(self.load_button)

        self.back_button = ImageButton(self, PREV_IMAGE, 
            PREV_PRESSED_IMAGE, self.back_button_clicked)
        self.back_button.setFixedWidth(PLAYER_ICON_SIZE)
        self.back_button.setFixedHeight(PLAYER_ICON_SIZE)
        button_layout.addWidget(self.back_button)

        self.play_button = ImageButton(self, PLAY_IMAGE,
         PLAY_PRESSED_IMAGE, self.play_button_clicked)
        self.play_button.setFixedWidth(PLAYER_ICON_SIZE)
        self.play_button.setFixedHeight(PLAYER_ICON_SIZE)
        button_layout.addWidget(self.play_button)

        self.forward_button = ImageButton(self, NEXT_IMAGE,
         NEXT_PRESSED_IMAGE, self.forward_button_clicked)
        self.forward_button.setFixedWidth(PLAYER_ICON_SIZE)
        self.forward_button.setFixedHeight(PLAYER_ICON_SIZE)
        button_layout.addWidget(self.forward_button)

        self.shuffle_button = ToggleButton(self, SHUFFLE_IMAGE,
         SHUFFLE_PRESSED_IMAGE, self.shuffle_button_clicked)
        self.shuffle_button.setFixedWidth(PLAYER_ICON_SIZE)
        self.shuffle_button.setFixedHeight(PLAYER_ICON_SIZE)
        button_layout.addWidget(self.shuffle_button)

        self.repeat_button = ToggleButton(self, REPEAT_IMAGE,
         REPEAT_PRESSED_IMAGE, self.repeat_button_clicked)
        self.repeat_button.setFixedWidth(PLAYER_ICON_SIZE)
        self.repeat_button.setFixedHeight(PLAYER_ICON_SIZE)
        button_layout.addWidget(self.repeat_button)

        self.volume_button = ToggleButton(self, VOLUME_IMAGE,
         MUTE_IMAGE, self.volume_button_clicked)
        self.volume_button.setFixedWidth(PLAYER_ICON_SIZE)
        self.volume_button.setFixedHeight(PLAYER_ICON_SIZE)
        button_layout.addWidget(self.volume_button)

    def open_file(self):
        """ Opens a file dialog where the user can select a song to play. If the
        user cancels the dialog then file_path will be an empty string, so we
        check for this before trying to load the song.

        PlayerGui.open_file() -> None
        """
        file_path = QtGui.QFileDialog.getOpenFileName(
            self, self.localisation.CHOOSE_SONG_STRING)[0]
        if file_path != "": 
            self.load_song(file_path)
        
    def load_song(self, file_path):
        """ Loads a song into the media_object, attaches that song to the 
        slider, and loads the song's metadata. Also loads the lyrics and artist
        info pages.

        PlayerGui.load_song(str) -> None
        """
        if os.path.exists(file_path):
            self.media_object.setCurrentSource(Phonon.MediaSource(file_path))
            self.phonon.set_halfway_mark()
            self.track_slider.setMediaObject(self.media_object)
            self.set_track_time(self.media_object.remainingTime())
            self.player.load_metadata(file_path)

            if self.parent.tabview_gui.artist_info_gui.get_artist\
             != self.player.get_current_artist():
                self.parent.tabview_gui.artist_info_gui.set_artist(
                    self.player.get_current_artist)
                self.get_artist_info_thread = GetArtistInfoThread(
                    self.player.get_current_artist(), self)
                self.get_artist_info_thread.start()
                self.connect(self.get_artist_info_thread,
                 QtCore.SIGNAL("thread_done(QString)"),
                  self.parent.tabview_gui.artist_info_gui.setHtml)

            if self.parent.tabview_gui.lyrics_gui.get_track_and_artist() != \
            (self.player.get_current_track(), self.player.get_current_artist()):
                self.parent.tabview_gui.lyrics_gui.set_track_and_artist(
                    (self.player.get_current_track(),
                     self.player.get_current_artist()))
                self.get_lyrics_thread = GetLyricsThread(
                    self.player.get_current_artist(),
                     self.player.get_current_track(), self)
                self.get_lyrics_thread.start()
                self.connect(self.get_lyrics_thread,
                 QtCore.SIGNAL("thread_done(QString)"),
                  self.parent.tabview_gui.lyrics_gui.setHtml)
                
        else:
            row = self.parent.tabview_gui.library_gui.get_library_row(file_path)
            self.parent.tabview_gui.library_gui.set_row_unavailable(row)

    def load_preferences(self):
        """ Gets the saved preferences for the Player (i.e. shuffle and repeat
         settings)

        PlayerGui.load_preferences() -> None
        """
        if self.parent.preferences.get_repeat_pref():
            self.repeat_button.toggle()

        if self.parent.preferences.get_shuffle_pref():
            self.shuffle_button.toggle()

    def set_font_settings(self, font, text_size):
        """Sets the font and text size for the labels in the player frame.

        PlayerGui.set_font_settings(str, int) -> None
        """

        player_widgets = [self.album_name, self.artist_name, self.track_name]
        for widget in player_widgets:
            widget.setFont(QtGui.QFont(font, text_size))

    def set_album_art(self, image_bytes):
        """Changes the image for the album_art widget to the given image.

        PlayerGui.set_album_art(str) -> None
        """
        pixel_map = QtGui.QPixmap()
        pixel_map.loadFromData(image_bytes)
        self.album_art.setPixmap(pixel_map.scaled(PLAYER_COVER_SIZE,\
         PLAYER_COVER_SIZE, QtCore.Qt.KeepAspectRatio,\
          QtCore.Qt.SmoothTransformation))

    def set_artist_name(self, artist):
        """ Changes the text in artist_name.

        PlayerGui.set_artist_name(str) -> None
        """
        self.artist_name.setText(artist)

    def set_track_name(self, track):
        """ Changes the text in track_name.

        PlayerGui.set_track_name(str) -> None
        """
        self.track_name.setText(track)

    def set_album_name(self, album):
        """ Changes the text in album_name.

        PlayerGui.set_album_name(str) -> None
        """
        self.album_name.setText(album)

    def set_track_time(self, time):
        """ Sets the remaining time left in a track for the track_time label.

        PlayerGui.set_track_time(int) -> None
        """
        ftime = self.player.format_time(time)
        self.track_time.setText(str(ftime))

    def play_button_clicked(self):
        """ Called when the play button is clicked. Checks if the media_object
        is playing or not and pauses/plays the song according to the result.
        Also changes the button image to reflect the current playback state.

        play_button_clicked(self) -> None
        """
        if self.phonon.is_playing():
            self.player.pause_song()
        else:
            self.player.play_song()

    def set_play_button_play(self):
        """ Changes the play button's image to play

        PlayerGui.set_play_button_play() -> None
        """
        self.play_button.setImage('images/play.png')
        self.play_button.set_pressed_image('images/play_pressed.png') 

    def set_play_button_pause(self):
        """ Changes the play button's image to pause

        PlayerGui.set_play_button_pause() -> None
        """
        self.play_button.setImage('images/pause.png')
        self.play_button.set_pressed_image('images/pause_pressed.png')  

    def back_button_clicked(self):
        """Called when the back button is clicked. If the current play time is
        less than 5 seconds the previous track is loaded, otherwise the song
        resets to the start and either continues playing or stays pause 
        depending on what the playback state was.

        PlayerGui.back_button_clicked() -> None
        """
        if self.media_object.state() == Phonon.PausedState or\
         self.media_object.state() == Phonon.StoppedState:
            if self.media_object.currentTime() < 5000: ##i.e. 5 secs
                self.player.previous_song()
            else:
                self.media_object.stop()
        elif self.media_object.state() == Phonon.PlayingState:
            if self.media_object.currentTime() < 5000: ##i.e. 5 secs
                self.player.previous_song()
            else:
                self.media_object.stop()
                self.media_object.play()

    def forward_button_clicked(self):
        """Called when the forward button is clicked. Calls the song_ended
        function.

        PlayerGui.forward_button_clicked() -> None
        """
        self.player.song_ended()

    def shuffle_button_clicked(self):
        """ Changes the shuffle mode to the opposite (boolean) of what it 
        currently is.

        PlayerGui.shuffle_button_clicked() -> None
        """
        self.player.set_shuffle_mode()

    def repeat_button_clicked(self):
        """ Changes the repeat mode to the opposite (boolean) of what it 
        currently is.

        PlayerGui.repeat_button_clicked() -> None
        """
        self.player.set_repeat_mode()

    def volume_button_clicked(self):
        """ Sets the volume of playback.

        PlayerGui.volume_button_clicked() -> None
        """
        self.player.toggle_mute()

class PlaylistGui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PlaylistGui, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.status_bar = self.parent.status_bar
        self.playlist = self.parent.playlist
        self.create_playlist_window()

        
    def create_playlist_window(self):
        """ Creates a PlaylistListView (which is a subclass of QListView) in the
        PlaylistGui widget. The PlaylistListView has a PlaylistItemModel (which
        is a subclass of QStandardItemModel) applied to it and is loaded with
        a saved playlist.

        PlaylistGui.create_playlist_window() -> None
        """
        self.layout = QtGui.QVBoxLayout(self)
        self.playlist_widget = PlaylistListView(self)
        self.playlist_model = PlaylistItemModel(self.playlist_widget)
        self.load_playlist(self.playlist.load_playlist_pickle())
        self.playlist_widget.setModel(self.playlist_model)
        self.playlist_widget.doubleClicked.connect(
            self.playlist_item_double_clicked)
        self.layout.addWidget(self.playlist_widget)
        self.layout.setContentsMargins(0,0,0,0)

    def load_playlist(self, playlist):
        """ Loads a playlist into the playlist listview from a list of 
        dictionaries containing file paths, artist name, song name and 
        playlist position. This would usally be run on startup to load 
        the playlist from the users last session.

        PlaylistGui.load_playlist(list(dict)) -> None
        """
        new_items = []
        for pl_dict in playlist:
            file_path = pl_dict['file_path']
            artist = pl_dict['artist']
            title = pl_dict['title']
            playlist_item = self.playlist_widget.create_playlist_item(
                file_path, title, artist)
            new_items.append(playlist_item)
            self.parent.playlist.append_to_playlist(file_path)
            self.playlist_model.appendRow(playlist_item)
        self.get_album_covers(new_items)

    def get_album_covers(self, items):
        """ Receives a list of newly created playlist items. Starts a thread to
        find the album covers for them and then calls the method 
        load_album_covers once the thread completes.

        PlaylistGui.get_album_covers(list[QStandardItem]) -> None
        """

        self.status_bar.set_left_message(
            self.localisation.LOADING_ALBUM_COVERS_STRING)
        self.add_covers_thread = PlaylistItemCoverThread(items, self)
        self.add_covers_thread.thread_done.connect(
            self.load_album_covers, QtCore.Qt.QueuedConnection)
        self.add_covers_thread.start()

    def load_album_covers(self, items, images):
        """ Receives a list of items and image bytes. Adds the images to each
        item.

        PlaylistGui.load_album_covers(list(PlaylistItem), list(str)) -> None
        """
        for index, item in enumerate(items):
            image = images[index]
            if image != '':
                try:
                    item.set_item_icon(image)
                except:
                    print 'Playlist item deleted.'
        self.status_bar.set_left_message('')

    def playlist_item_double_clicked(self, item):
        """ Called when a playlist item is double clicked. Gets the file path of
        the clicked item, loads it and plays it.

        PlaylistGui.playlist_item_double_clicked(QModelIndex) -> None
        """
        file_path = self.playlist_model.get_item_file_path(item.row())
        self.playlist.set_current_position(item.row())
        self.parent.player_gui.load_song(file_path)
        self.parent.player_gui.player.play_song()

    def remove_from_playlist(self):
        """ Removes the selected items form the playlist.

        PlaylistGui.remove_from_playlist() -> None
        """
        items_removed_before_current_position = 0
        indices = self.playlist_widget.selectedIndexes()
        indices.sort() 
        #If the user makes a selection going up the indexes will need to 
        #be sorted from small to big
        indices.reverse()
        for item in indices:
            if item.row() <= self.playlist.get_current_position():
                self.playlist.set_current_position(
                    self.playlist.get_current_position() - 1)
            self.playlist_model.removeRow(item.row())
            self.playlist.remove_item(item.row())

    def keyPressEvent(self, event):
        """ Called when a key is pressed while the PlaylistGui is the view being
        used. If the key pressed is backspace then the selected songs are 
        removed from the playlist.

        PlaylistGui.keyPressEvent(QEvent) -> None
        """
        if event.key() == QtCore.Qt.Key_Backspace:
            self.remove_from_playlist()

class TabviewGui(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(TabviewGui, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.status_bar = self.parent.status_bar
        self.preferences = self.parent.preferences
        self.library_gui = LibraryGui(self)
        self.artist_info_gui = ArtistInfoGui(self)
        self.lyrics_gui = LyricsGui(self)
        self.create_tabview_window()

    def create_tabview_window(self):
        """ Creates a QTabWidget widget and adds three widgets as tabs -
        LibraryGui, LastfmGui, and LyricsGui.

        TabviewGui.create_tabview_window() -> None
        """
        self.layout = QtGui.QVBoxLayout(self)
        self.tabview_widget = QtGui.QTabWidget(self)
        self.tabview_widget.setTabPosition(QtGui.QTabWidget.West)
        self.tabview_widget.addTab(
            self.library_gui, self.localisation.LIBRARY_STRING)
        self.tabview_widget.addTab(
            self.artist_info_gui, self.localisation.ARTIST_INFO_STRING)
        self.tabview_widget.addTab(
            self.lyrics_gui, self.localisation.LYRICS_STRING)
        self.layout.addWidget(self.tabview_widget)
        self.layout.setContentsMargins(0,0,0,0)

    def show_library_view(self):
        """ Sets the currently displayed tab as LibraryGui.

        TabviewGui.show_library_view() -> None
        """
        self.tabview_widget.setCurrentWidget(self.library_gui)

    def show_artist_info_view(self):
        """ Sets the currently displayed tab as LastfmGui.

        TabviewGui.show_artist_info_view() -> None
        """
        self.tabview_widget.setCurrentWidget(self.artist_info_gui)

    def show_lyrics_view(self):
        """ Sets the currently displayed tab as LyricsGui.

        TabviewGui.show_lyrics_view() -> None
        """
        self.tabview_widget.setCurrentWidget(self.lyrics_gui)

class LibraryGui(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LibraryGui, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.status_bar = self.parent.status_bar
        self.preferences = self.parent.preferences
        self.library_columns = self.preferences.get_library_columns_pref()
        self.main_gui = self.parent.parent
        self.library = library.Library(self, self.library_columns)
        self.create_library_window()
        self.set_library_status()

    def create_library_window(self):
        """ Creates a QTableView widget within the parent LibraryGui widget and
        applies all the necessary setting for it. A QItemModel for the 
        QTableView widget is applied and the library is loaded.

        LibraryGui.create_library_window() -> None
        """
        self.layout = QtGui.QVBoxLayout(self)
        self.library_widget = LibraryTableView(self)
        self.library_widget.doubleClicked.connect(
            self.library_item_double_clicked)
        self.model = QtGui.QStandardItemModel(self.library_widget)
        self.library_widget.setModel(self.model)
        self.load_library()
        self.layout.addWidget(self.library_widget)
        self.layout.setContentsMargins(0,0,0,0)

    def load_library(self):
        """ Gets a list of database rows from the Library class and for each
        row creates a QStandardItem and inserts it into the LibraryGui's
        QTableView.

        LibraryGui.load_library() -> None
        """
        self.set_column_headers(self.library_columns)
        library = self.library.get_library()
        for track in library:
            row = [self.create_table_item(unicode(tag)) for tag in track]
            self.model.appendRow(row)
        self.set_row_heights(TABLE_FONT_SIZE)
        self.set_visible_columns(self.library_columns)

    def refresh_library(self):
        """ Removes the current library model and reloads the library. Used
        when adding new directories to the library as it's faster than 
        individually adding each new file.

        LibraryGui.refresh_library() -> None
        """
        self.model = QtGui.QStandardItemModel(self.library_widget)
        self.library_widget.setModel(self.model)
        self.load_library()

    def check_library_status(self):
        """ Checks each item in the library to see if the file path exists. If
        not the item text changes to gray. Items are not deleted in case they
        exist on external media which might be plugged in at a later time.

        LibraryGui.check_library_status() -> None
        """
        for row in range(self.model.rowCount()):
            file_path =  self.model.item(
                row, self.get_file_path_column()).text()
            if not os.path.exists(file_path):
                self.set_row_unavailable(row)

    def add_items(self, items):
        """ Adds the given items to the library.

        LibraryGui.add_items(list(list(str))) -> None
        """
        row_counter = 0
        self.progress_dialog.setValue(row_counter)
        self.progress_dialog.setMaximum(len(items))
        self.progress_dialog.setLabelText(
            self.localisation.REFRESH_LIBRARY_STRING)
        for track in items:
            row = [self.create_table_item(unicode(tag)) for tag in track]
            self.model.appendRow(row)
            row_counter += 1
            self.progress_dialog.setValue(row_counter)
        self.set_row_heights(TABLE_FONT_SIZE)
        self.progress_dialog.reset()

    def set_column_headers(self, columns):
        """ Receives a dictionary containing the settings for libary columns. 
        Sets the text of each column header in LibraryGui's QTableView according
        to the names specified in the settings dictionary.

        LibraryGui.set_column_headers(dict) -> None
        """
        for index, column in enumerate(columns):
            item = QtGui.QStandardItem()
            item.setText(column['Name'])
            self.model.setHorizontalHeaderItem(index, item)

    def set_visible_columns(self, columns):
        """ Receives a dictionary containing the settings for libary columns. 
        Sets the visibility of each column  in LibraryGui's QTableView according
        to the boolean specified in the settings dictionary.
        
        LibraryGui.set_visible_columns(dict) -> None
        """
        for index, column in enumerate(columns):
            if not column['Activated']:
                self.library_widget.setColumnHidden(index, True)

    def get_library_row(self, file_path):
        """
        Returns the index of the row containing the given file path.

        LibraryGui.get_library_row(str) -> int
        """
        item = self.model.findItems(
            file_path, column=self.get_file_path_column())
        return item[0].row()

    def get_file_path(self, row):
        """ Returns the file_path of the item in the given row.

        LibraryGui.get_file_path(int) -> str
        """
        return self.model.item(row, self.get_file_path_column()).text()

    def set_row_unavailable(self, row):
        """ Disables the given row.

        LibraryGui.set_row_unavailable(int) -> None
        """
        for i in range(self.model.columnCount()):
            item = self.model.item(row, i)
            item.setToolTip(self.localisation.FILE_DOESNT_EXIST_STRING)
            item.setForeground(QtGui.QBrush(INVALID_FILE_FONT_COLOUR))

    def set_path_unavailable(self, file_path):
        """ Finds a path in the library and sets it as unavailable. This is
        done if they file cannot be found.

        LibraryGui.set_path_unavailable(str) -> None
        """
        row = self.get_library_row(file_path)
        self.set_row_unavailable(row)

    def library_item_double_clicked(self, item):
        """ Called when a library item is double clicked. Gets the file path
        from that item and uses it to load and play the song.

        LibraryGui.library_item_double_clicked(QModelIndex) -> None
        """
        file_path = item.sibling(
            item.row(), self.get_file_path_column()).data()
        self.main_gui.player_gui.load_song(file_path)
        self.main_gui.player_gui.player.play_song()

    def create_table_item(self, text):
        """ Creates a QStandardItem from the text given and applies settings.

        LibraryGui.create_table_item(str) -> QStandardItem
        """
        table_item = QtGui.QStandardItem()
        table_item.setDragEnabled(True)
        table_item.setEditable(False)
        table_item.setText(text)
        table_item.setFont(QtGui.QFont(TABLE_FONT, TABLE_FONT_SIZE))
        return table_item

    def update_table_row(self, file_path):
        """ Updates a table row. Get the metadata for the given file_path and
        uses it to create a new table row. The old table row is located in the
        QTableView and replaced with the new one.

        LibraryGui.update_table_row(str) -> None
        """
        updated_item_data = self.library.get_item_data(file_path)
        new_row = \
        [self.create_table_item(unicode(tag)) for tag in updated_item_data]
        index = self.model.findItems(
            file_path, column=self.get_file_path_column())[0]
        row_position = index.row()
        self.model.removeRow(row_position)
        self.model.insertRow(row_position, new_row)
        self.set_row_heights(TABLE_FONT_SIZE)

    def set_row_heights(self, size):
        """ Sets the height of all rows in the QTableView to the given size.

        LibraryGui.set_row_heights(int) -> None
        """
        row = 0
        while row < self.model.rowCount():
            self.library_widget.setRowHeight(row, size * 1.8)
            row += 1

    def remove_items(self):
        """ Called when a library item had been deleted (and confirmed via 
        prompt). Removes the items from the Library widget, then removes 
        them from the library database.

        LibraryGui.remove_items() -> None
        """
        rows = self.selected_rows()
        file_paths = [self.model.item(
            row.row(), self.get_file_path_column()).text() for row in rows]
        rows.sort()
        rows.reverse()
        for row in rows:
            self.model.removeRow(row.row())
        self.library.remove_items(file_paths)
        self.delete_prompt.accept()

    def selected_rows(self):
        """ Returns all selected rows in the library

        LibraryGui.selected_rows() -> list(int)
        """
        selection_model = self.library_widget.selectionModel()
        return selection_model.selectedRows()

    def get_file_path_column(self):
        """ Returns the column that contains file paths.

        LibraryGui.get_file_path_column() -> int
        """
        for c in self.library_columns:
            if c["Name"] == 'File Path':
                return c["Column"]

    def get_title_column(self):
        """ Returns the column that contains song title.

        LibraryGui.get_title_column() -> int
        """
        for c in self.library_columns:
            if c["Name"] == 'Title':
                return c["Column"]

    def get_artist_column(self):
        """ Returns the column that contains artist names.

        LibraryGui.get_artist_column() -> int
        """
        for c in self.library_columns:
            if c["Name"] == 'Artist':
                return c["Column"]

    def get_library_size(self):
        """ Returns the number of rows in the library.

        LibraryGui.get_library_size() -> int
        """
        return self.model.rowCount()

    def get_number_of_selected_items(self):
        """ Returns the number of selected rows in the library.

        LibraryGui.get_number_of_selected_items() -> int
        """
        return len(self.selected_rows())

    def set_library_status(self):
        """ Sets the current status of the library in the StatusBar.

        LibraryGui.set_library_status() -> None
        """
        size = self.get_library_size()
        selected = self.get_number_of_selected_items()
        if selected == 0:
            message = str(size) + ' ' + self.localisation.FILES_STRING + '.'
        else:
            message = str(size) + ' ' + self.localisation.FILES_STRING + ', ' +\
             str(selected) + " " + self.localisation.SELECTED_STRING + "."
        self.status_bar.set_right_message(message)

    def remove_from_library(self):
        """ Called when the user tries to delete files. Opens a confirmation
        prompt.

        LibraryGui.remove_from_library() -> None
        """
        self.delete_prompt = QtGui.QDialog(self)
        layout = QtGui.QGridLayout(self.delete_prompt)
        label = QtGui.QLabel(
            self.localisation.DELETE_PROMPT_STRING, self.delete_prompt)
        layout.addWidget(label, 0, 0 , 1, 2)
        y_button = QtGui.QPushButton(
            self.localisation.YES_STRING, self.delete_prompt)
        y_button.clicked.connect(self.remove_items)
        layout.addWidget(y_button, 1, 0)
        n_button = QtGui.QPushButton(
            self.localisation.NO_STRING, self.delete_prompt)
        n_button.clicked.connect(self.delete_prompt.reject)
        layout.addWidget(n_button, 1, 1)
        self.delete_prompt.open()

    def create_add_files_progress_dialog(self):
        """ Creates a progress dialog object to be used while loading tracks
        into the library.

        LibraryGui.create_add_files_progress_dialog() -> None
        """
        self.progress_dialog = QtGui.QProgressDialog(
            self.localisation.FILE_SEARCH_STRING, "", 0, 0)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.progress_dialog.setAutoReset(False)

    def get_add_files_progress_dialog(self):
        """ Gets the progress dialog object.

        LibraryGui.get_add_files_progress_dialog() -> QProgressDialog
        """
        return self.progress_dialog

    def keyPressEvent(self, event):
        """ Called when a key is pressed while the LibraryGui is the view being
        used. If the key pressed is backspace then the selected songs are 
        removed from the library after a prompt.

        LibraryGui.keyPressEvent(QEvent) -> None
        """
        if event.key() == QtCore.Qt.Key_Backspace:
            self.remove_from_library()

class ArtistInfoGui(QtWebKit.QWebView):
    """
    This class contains a web view that displays information on the 
    current artist. 
    """
    def __init__(self, parent=None):
        super(ArtistInfoGui, self).__init__(parent)
        self.parent = parent
        self._current_artist = None

    def get_artist(self):
        """ Returns the currently loaded page.

        LastfmGui.get_current_page() -> str
        """
        return self._current_artist

    def set_artist(self, artist):
        """ Sets the currently loaded page.

        LastfmGui.set_current_page(str) -> None
        """
        self._current_artist = artist

class GetArtistInfoThread(QtCore.QThread):
    """
    This class gets information about the currently playing artist via the 
    Last.FM API. That information is the rearranged in HTML.
    """
    def __init__(self, artist, parent=None):
        super(GetArtistInfoThread, self).__init__(parent)
        self.artist = artist
        self.parent = parent
        self.localisation = self.parent.localisation
        self.api_url = "http://ws.audioscrobbler.com/2.0/?method="
        self.api_key = "&api_key=74531d253dc8e9fa6165fc50d331f8c2"

    def run(self):
        """ Runs the thread and sends the data back to the calling function
        once the thread is complete. Returns None in order to close the thread.

        GetArtistInfoThread.run() -> None
        """
        artist_info_html = self.get_artist_info()
        self.emit(QtCore.SIGNAL("thread_done(QString)"), artist_info_html)
        return None

    def get_artist_info(self):
        """ Gets the seperates of the artist info and combines them. Returns
        it as HTML. If there is an error accessing the internet an error message
        is returned.

        GetArtistInfoThread.get_artist_info() -> str
        """
        if self.get_canonical_artist_name():
            biography = self.get_artist_biography()
            top_tracks = self.get_top_tracks()
            top_albums = self.get_top_albums()
            lists_html = self.build_lists_html(top_tracks, top_albums)
            html = biography + lists_html
            return html
        else:
            return '<p>' + self.localisation.NO_INTERNET_CONNECTION_STRING +\
             '</p>'

    def get_canonical_artist_name(self):
        """ Gets the correct name for an artist. For example, if the the
        artist name 'The Beetles' is given, this will be corrected to 'The 
        Beatles'. Also serves as a way to detect if an internet connection is
        available, returning False if this is not the case.

        GetArtistInfoThread.get_canonical_artist_name() -> boolean
        """
        url = self.api_url + 'artist.getcorrection&artist=' + self.artist \
        + self.api_key
        try:
            request = requests.post(url)
            soup = BeautifulSoup(request.text, "xml")
            name = soup.find("name")
            if name != None:
                self.artist = name.text
            return True
        except:
            return False

    def get_artist_biography(self):
        """ Retreives the biography of the current artist.

        GetArtistInfoThread.get_artist_biography() -> str
        """
        url = self.api_url + 'artist.getinfo&artist=' + self.artist +\
         self.api_key
        request = requests.post(url)
        soup = BeautifulSoup(request.text, "xml")
        error = soup.find("error")
        if error != None:
            return error.text
        else:
            image = self.get_artist_image(request.text)
            bio = self.get_artist_description(soup)
            tags = self.get_artist_tags(soup)
            similar_artists = self.get_similar_artists(soup)

        html = self.build_bio_html(image, bio, tags, similar_artists)
        return html

    def get_artist_image(self, xml):
        """ Retreives a link to an image of the current artist.

        GetArtistInfoThread.get_artist_biography() -> str
        """
        header_end = xml.find("<streamable>")
        soup = BeautifulSoup(xml[:header_end], "xml")
        images = soup.find_all('image')
        if images == None:
            return None
        else:
            #The last image in the list will be the largest
            return images[-1].text

    def get_artist_description(self, soup):
        """ Retreives a description of the current artist.

        GetArtistInfoThread.get_artist_description() -> str
        """
        description = soup.find("summary")
        return description.text

    def get_artist_tags(self, soup):
        """ Retreives a list of tags for the current artist.

        GetArtistInfoThread.get_artist_tags() -> list(str)
        """
        tags = soup.find_all("tag")
        tag_list = [t.find("name").text for t in tags]
        return tag_list

    def get_similar_artists(self, soup):
        """ Retreives a list of similar artists for the current artist.

        GetArtistInfoThread.get_similar_artists() -> list(str)
        """
        similar_artists = []
        soup = soup.find('similar')
        artists = soup.find_all('artist')
        for a in artists:
            name = a.find('name')
            url = a.find('url')
            images = a.find_all('image')
            if images == []:
                similar_artists.append((name.text, url.text, ''))
            elif len(images) < 3:
                similar_artists.append((name.text, url.text, images[-1].text))
            else:
                similar_artists.append((name.text, url.text, images[3].text)) 
                #Returns the 4rd image i.e. xlarge size
        return similar_artists

    def get_top_tracks(self):
        """ Retreives the top ten most listened tracks for the current artist
        on LastFM. Stores the track name, URL, and image link.

        GetArtistInfoThread.get_top_tracks() -> list((str, str, str))
        """
        url = self.api_url + 'artist.gettoptracks&artist=' + self.artist +\
         self.api_key
        request = requests.post(url)
        soup = BeautifulSoup(request.text, "xml")
        error = soup.find("error")
        if error != None:
            return error.text
        tracks = soup.find_all('track')
        top_tracks = []
        
        while len(top_tracks) < 10 and len(tracks) > 0:
            name = tracks[0].find('name')
            url = tracks[0].find('url')
            images = tracks[0].find_all('image')
            if images == []:
                top_tracks.append((name.text, url.text, ''))
            elif len(images) < 3:
                top_tracks.append((name.text, url.text, images[-1].text)) 
                #Returns the 3rd image i.e. large size
            else:
                top_tracks.append((name.text, url.text, images[2].text)) 
                #Returns the 3rd image i.e. large size
            tracks.pop(0)
        return top_tracks

    def get_top_albums(self):
        """ Retreives the top ten most listened albums for the current artist
        on LastFM. Stores the album name, URL, and image link.

        GetArtistInfoThread.get_top_tracks() -> list((str, str, str))
        """
        url = self.api_url + 'artist.gettopalbums&artist=' + self.artist +\
         self.api_key
        request = requests.post(url)
        soup = BeautifulSoup(request.text, "xml")
        error = soup.find("error")
        if error != None:
            return error.text
        albums = soup.find_all('album')
        top_albums = []
        
        while len(top_albums) < 10 and len(albums) > 0:
            name = albums[0].find('name')
            url = albums[0].find('url')
            images = albums[0].find_all('image')
            if images == []:
                top_albums.append((name.text, url.text, ''))
            elif len(images) < 3:
                top_albums.append((name.text, url.text, images[-1].text))
                #Returns the 3rd image i.e. large size
            else:
                top_albums.append((name.text, url.text, images[2].text))
                #Returns the 3rd image i.e. large size
            albums.pop(0)
        return top_albums

    def build_bio_html(self, image, bio, tags, similar_artists):
        """ Builds a HTML string out of the provided parts of the artist
        biography.

        GetArtistInfoThread.build_bio_html(
            str, str, list(str), list(str)) -> str
        """
        html = "<h2>" + self.artist + "</h2>"
        html += "<div style = 'margin-bottom:20px; overflow: hidden;\
         width: 690px;'>"
        if image != None:
            html += "<img src=" + image + " style='width: auto; height: auto;\
             max-width: 400px; margin: 0 auto; margin-right: 20px; \
             float:left;'/>"
        if bio != None:
            html += "<p>" + bio + "</p>"
        if tags != None:
            html += "<p> " + self.localisation.TAGS_STRING + ": "
            for tag in tags:
                html +=  tag + " / "
            html += "</p></div>"
        else:
            html += "</div>"

        if similar_artists != None:
            html += "<div><h3>" + self.localisation.SIMILAR_ARTISTS_STRING \
            + "</h3>"
            for a in similar_artists:
                html += "<div style='float:left; overflow:hidden;\
                 position:relative; margin-right:10px;'>"
                html += "<div style='background-image: url(" + a[2] + ");\
                 background-position: top; width: 130px; height: 130px;'></div>"
                html += '<h5 style="position: relative; margin-top:0px;\
                 padding-bottom:10px; padding-top:10px; max-width: 130px;\
                  background:black; text-align:center; overflow: hidden;">'
                html += '<a href="' + a[1] + '" style=" color:white;\
                 text-decoration: none;">' + a[0] + '</a>'
                html += "</h5></div>"
            html += "</div>"
        return html

    def build_lists_html(self, top_tracks, top_albums):
        """ Builds a HTML string out of the provided parts of the artist's top 
        albums and top tracks lists.

        GetArtistInfoThread.build_lists_html(list((str, str, str)), 
            list((str, str, str))) -> str
        """
        html = "<div style='width:80%;'><div style='float:left; max-width=40%;\
         overflow:hidden;'>"
        html += "<h4>" + self.localisation.TOP_TRACKS_STRING + "</h4>"
        if top_tracks != None:
            for t in top_tracks:
                html += "<div style='overflow: hidden; margin-bottom: 10px;\
                 border: 1px solid; border-color: #e5e5e5 #dbdbdb #d2d2d2;\
                  -webkit-border-radius: 4px;\
                   -webkit-box-shadow: rgba(0, 0, 0, 0.3) 0 1px 3px;'>"
                html += "<div style='padding: 10px; float: left;'>"
                html += "<img style='' src='" + t[2] + "'></img>"
                html += "</div><div style='padding: 10px; float: left;'>"
                html += "<h5>" + t[0] + "</h5></div></div>"
            html += "</div>"
        html += "</div>"
        html += "<div style='float:right; max-width=40%; overflow:hidden;'>"
        html += "<h4>" + self.localisation.TOP_ALBUMS_STRING + "</h4>"
        if top_albums != None:
            for t in top_albums:
                html += "<div style='overflow: hidden; margin-bottom: 10px;\
                 border: 1px solid; border-color: #e5e5e5 #dbdbdb #d2d2d2;\
                  -webkit-border-radius: 4px;\
                   -webkit-box-shadow: rgba(0, 0, 0, 0.3) 0 1px 3px;'>"
                html += "<div style='padding: 10px; float: left;'>"
                html += "<img style='' src='" + t[2] + "'></img>"
                html += "</div><div style='padding: 10px; float: left;'>"
                html += "<h5>" + t[0] + "</h5></div></div>"
            html += "</div></div>"
        return html

class LyricsGui(QtWebKit.QWebView):
    """
    This class contains a web view that displays the lyrics of the current song.
    """
    def __init__(self, parent=None):
        super(LyricsGui, self).__init__(parent)
        self.parent = parent
        self._current_track_and_artist = None

    def get_track_and_artist(self):
        """ Returns the artist and track name for the lyrics currently loaded.

        LyricsGui.get_track_and_artist() -> (str, str)
        """
        return self._current_track_and_artist

    def set_track_and_artist(self, track_and_artist):
        """ Receives a tuple containing the track and artist names for the
        lyrics currently loaded and stores it.

        LyricsGui.set_track_and_artist((str, str)) -> None
        """
        self._current_track_and_artist = track_and_artist

class GetLyricsThread(QtCore.QThread):
    """
    This class creates a new thread to fetch the lyrics for a song. The new 
    thread is needed in case the web request take a long time and holds up the
    application.
    """
    def __init__(self, artist, track, parent=None):
        super(GetLyricsThread, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.artist = artist
        self.track = track

    def run(self):
        """ Gets the lyrics for the song and sends them to the class the thread
        was start from. Returns None to make sure thread closes.

        GetLyricsThread.run() -> None
        """
        lyrics = self.get_lyrics()
        self.emit(QtCore.SIGNAL("thread_done(QString)"), lyrics)
        return None

    def get_lyrics(self):
        """Makes a request to lyrics.wikia.com for the song lyrics by giving it
        the item's artist name and track name. It returns as XML, which is
        parsed and returned as a string. If there is no internet connection a
        message stating so is returned.

        GetLyricsThread.get_lyrics() -> str
        """
        search_url = "http://lyrics.wikia.com/api.php?func=getSong&artist="\
         + self.artist + '&song=' + self.track + '&fmt=xml'
        headers = {'X-Wikia-API-Key': 'XFCKR0ARK4PDDQTWX'}
        try:
            request = requests.post(search_url, headers)
        except:
            return '<p>' + self.localisation.NO_INTERNET_CONNECTION_STRING +\
             '</p>'
        text = self.parse_lyrics_xml(request.text)
        return text

    def parse_lyrics_xml(self, xml):
        """ Parses an XML page containing lyrics metadata. If xml is None, which
        is what will be sent to the function if no lyrics exist, then a message
        stating "No lyrics available" is returned. If the XML is valid a link to
        a HTML page with the lyrics is requested, parsed, and returned as a 
        string.

        GetLyricsThread.parse_lyrics_xml(str) -> str
        """
        if xml == None:
            return self.localisation.NO_LYRICS_STRING
        else:
            soup = BeautifulSoup(xml, "xml")
            lyrics_url = soup.find("url")
            if lyrics_url == None:
                return self.localisation.NO_LYRICS_STRING
            else: 
                request = requests.get(lyrics_url.text)
                lyrics = self.parse_lyrics_html(request.text, lyrics_url.text)
                return lyrics

    def parse_lyrics_html(self, html, url):
        """ Parses a HTML page containing lyrics. If html is None, which
        is what will be sent to the function if the string given to the function
        parse_lyrics_xml was not proper XML, then a message stating "No lyrics 
        available" is returned. If the HTML is valid a link to a HTML page with 
        the lyrics is parsed, and returned as a string.

        GetLyricsThread.parse_lyrics_html(str) -> str
        """
        if html == None:
            return self.localisation.NO_LYRICS_STRING
        else:
            soup = BeautifulSoup(html)
            lyric_box = soup.find("div", { "class" : "lyricbox" })
            lyrics = unicode(lyric_box)
            ad_end = lyrics.find("</div>") + 6
            lyrics_end = lyrics.find("<!--")
            lyrics = lyrics[ad_end:lyrics_end]
            if lyrics == "" or lyrics == None:
                return self.localisation.NO_LYRICS_STRING
            return "<p>" + lyrics + "</p><br/><br/><p>" + \
            self.localisation.LYRICS_FROM_STRING + " <a href='" + url + "'>"\
             + url + "</a></p>"

class StatusBar(QtGui.QWidget):
    """ A QWidget that holds two QLabels for displaying status text at the
    bottom of the main window.
    """
    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)
        self.parent = parent
        self.create_status_bar()

    def create_status_bar(self):
        """ Creates the status bar.

        StatusBar.create_status_bar() -> None
        """
        layout = QtGui.QHBoxLayout(self)
        self.left_message = QtGui.QLabel()
        layout.addWidget(self.left_message)
        self.right_message = QtGui.QLabel()
        self.right_message.setAlignment(QtCore.Qt.AlignRight)
        layout.addWidget(self.right_message)
        layout.setContentsMargins(0,0,0,0)

    def set_right_message(self, message):
        """ Sets the right side label to display the given text.

        StatusBar.set_right_message(str) -> None
        """
        self.right_message.setText(message)

    def set_left_message(self, message):
        """ Sets the left side label to display the given text.

        StatusBar.set_left_message(str) -> None
        """
        self.left_message.setText(message)

class ImageButton(QtGui.QAbstractButton):
    """
    This is a subclass of QAbstractButton that changes the button to be 
    an image. The button is created with with two images (normal and pressed)
    and a function to be called on clicking the button.
    ImageButton(self, QObject, str, str, function) -> ImageButton
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
        ImageButton.setImage(str) -> None
        """       
        self.image = image
        self.repaint()

    def set_pressed_image(self, image):
        """ Set the prsesed_image of the button
        ImageButton.set_pressed_image(str) -> None
        """       
        self.pressed_image = image
        self.repaint()

    def paintEvent(self, event):
        """ The function called when self.repaint() is called. Updates the
        widget with the new image.
        ImageButton.paintEvent(QEvent) -> None
        """
        painter = QtGui.QPainter(self)
        pm = QtGui.QPixmap(self.image)
        painter.drawPixmap(event.rect(), pm)

    def mousePressEvent(self, event):
        """ When a mouse press is detected the button will change image to the
        specified press_image file.
        ImageButton.mousePressEvent(QEvent) -> None
        """
        self.setImage(self.pressed_image)

    def mouseReleaseEvent(self, event):
        """ When a mouse release is detected the button will change back to the
        usual image for the button and run the function associated with the 
        button.
        ImageButton.mouseReleaseEvent(QEvent) -> None
        """
        self.setImage(self.released_image)
        self.function()

class ToggleButton(QtGui.QAbstractButton):
    """
    This is a subclass of QAbstractButton that makes a button that can be
    toggled and change image when toggled. It is created with two images (to 
    toggle between), and a function that will be called when the button is
    clicked
    ToggleButton(self, QObject, str, str, function) -> ToggleButton
    """

    def __init__(self, parent, image, toggled_image, function):
        super(ToggleButton, self).__init__(parent)
        self.function = function
        self.untoggled_image = image
        self.toggled_image = toggled_image
        self.setImage(image)


    def setImage(self, image):
        """ Set the image of the button
        ToggleButton.setImage(str) -> None
        """       
        self.image = image
        self.repaint()


    def paintEvent(self, event):
        """ The function called when self.repaint() is called. Updates the
        widget with the new image.
        ToggleButton.paintEvent(QEvent) -> None
        """
        painter = QtGui.QPainter(self)
        pm = QtGui.QPixmap(self.image)
        painter.drawPixmap(event.rect(), pm)

    def toggle(self):
        """ The button will switch
        image and run the associated function.
        ToggleButton.toggle() -> None
        """
        if self.image == self.untoggled_image:
            self.setImage(self.toggled_image)
        else:
            self.setImage(self.untoggled_image)
        self.function()

    def mousePressEvent(self, event):
        """ When the button is clicked this is called. The button will switch
        image and run the associated function.
        ToggleButton.mousePressEvent(QEvent) -> None
        """
        self.toggle()

class PlaylistListView(QtGui.QListView):
    """
    This is a subclass of Pyside’s QListView class. The main difference is a 
    change it what occurs when an item is dropped on the list.
    """
    def __init__(self, parent=None):
        super(PlaylistListView, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.main = self.parent.parent
        self.metadata = metadata.Metadata()
        self.playlist = self.parent.playlist
        self.setUniformItemSizes(True)
        self.setIconSize(QtCore.QSize(60, 60))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setLayoutMode(QtGui.QListView.Batched)
        self.setDragDropOverwriteMode(False)
        self.setDragEnabled(True)
        self.setMovement(QtGui.QListView.Free)
        self.setDefaultDropAction(QtCore.Qt.LinkAction)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

    def dropEvent(self, event):
        """ When items are dragged to the PlaylistListView this function is 
        called. If the items are added from the library or from outside the app 
        they are added at the correct index and their file paths are added to 
        the Playlist class. If the items are being moved within the 
        PlaylistListView the same process applies, but with the old items being 
        removed from the PlaylistListView and Playlist.

        PlaylistListView.dropEvent(QEvent) -> None
        """
        drop_index = self.get_drop_position(self.indexAt(event.pos()).row())
        new_items = []
        if event.source() == self:
            selected_items = self.selectedIndexes()
            #sorts the items so that if a user makes individual selections in 
            #reverse (e.g. select row 3, then 1) it returns the selected items
            #from lowest to highest(e.g 1,3)
            selected_items.sort()
            selected_items_paths = []
            for item in selected_items:
                file_path = self.parent.playlist_model.item(
                    item.row()).get_file_path()
                selected_items_paths.append(file_path)
            items_to_remove = []
            for i, selected_item in enumerate(selected_items):
            # -1 is returned if the playlist is empty 
            # or the drop is below all the other items
                if drop_index == -1:
                    playlist_item = self.create_playlist_item(
                        selected_items_paths[i])
                    new_items.append(playlist_item)
                    self.parent.playlist_model.appendRow(playlist_item)
                    self.playlist.append_to_playlist(
                        playlist_item.get_file_path())
                    items_to_remove.append(selected_item.row())
                else:
                    playlist_item = self.create_playlist_item(
                        selected_items_paths[i])
                    new_items.append(playlist_item)
                    self.parent.playlist_model.insertRow(
                        drop_index, playlist_item)
                    self.playlist.insert_in_playlist(
                        playlist_item.get_file_path(), drop_index)
                    if drop_index > selected_item.row():
                        items_to_remove.append(selected_item.row())
                    else:
                        items_to_remove.append(
                            selected_item.row() + len(selected_items))
                    drop_index +=1
            items_to_remove.reverse()
            for row in items_to_remove:
                self.parent.playlist_model.removeRow(row)
                self.playlist.remove_item(row)
        ## If the source is None then the drop is from outside the app.
        elif event.source() == None:
            items = []
            for item in event.mimeData().urls():
                items.append(item.toString()[6:]) #Removes 'file://' from string
            for i in items:
                if self.metadata.isValidFile(i):
                    if drop_index == -1:
                        playlist_item = self.create_playlist_item(i)
                        new_items.append(playlist_item)
                        self.parent.playlist_model.appendRow(playlist_item)
                        self.playlist.append_to_playlist(
                            playlist_item.get_file_path())
                    else:
                        playlist_item = self.create_playlist_item(i)
                        new_items.append(playlist_item)
                        self.parent.playlist_model.insertRow(
                            drop_index, playlist_item)
                        self.playlist.insert_in_playlist(
                            playlist_item.get_file_path(), drop_index)
                        drop_index +=1

        else:
            row = 0
            model = QtGui.QStandardItemModel()
            model.dropMimeData(event.mimeData(), QtCore.Qt.CopyAction,
             0, 0, QtCore.QModelIndex())
            # -1 is returned if the playlist is empty 
            # or the drop is below all the other items
            if drop_index == -1: 
                while row < model.rowCount():
                    file_path = model.item(row, self.main.tabview_gui.\
                        library_gui.get_file_path_column()).text()
                    if os.path.exists(file_path):
                        title = model.item(row, self.main.tabview_gui.\
                            library_gui.get_title_column()).text()
                        artist = model.item(row, self.main.tabview_gui.\
                            library_gui.get_artist_column()).text()
                        playlist_item = self.create_playlist_item(
                            file_path, title, artist)
                        new_items.append(playlist_item)
                        self.parent.playlist_model.appendRow(playlist_item)
                        self.playlist.append_to_playlist(
                            playlist_item.get_file_path())
                    else:
                        self.main.tabview_gui.library_gui.set_path_unavailable(
                            file_path)
                    row += 1
            else:
                while row < model.rowCount():
                    file_path = model.item(row, self.main.tabview_gui.\
                        library_gui.get_file_path_column()).text()
                    if os.path.exists(file_path):
                        title = model.item(row, self.main.tabview_gui.\
                            library_gui.get_title_column()).text()
                        artist = model.item(row, self.main.tabview_gui.\
                            library_gui.get_artist_column()).text()
                        playlist_item = self.create_playlist_item(
                            file_path, title, artist)
                        new_items.append(playlist_item)
                        self.parent.playlist_model.insertRow(
                            drop_index, playlist_item)
                        self.playlist.insert_in_playlist(
                            playlist_item.get_file_path(), drop_index)
                        drop_index += 1
                    else:
                        self.main.tabview_gui.library_gui.set_path_unavailable(
                            file_path)
                    row += 1
        self.parent.get_album_covers(new_items)

    def dragEnterEvent(self, event):
        """ Reimplements QListView's dragEnterEvent. Checks the source of a
        drag and accepts it if valid.

        PlaylistListView.dragEnterEvent(QEvent) -> None
        """
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """ Reimplements QListView's dragMoveEvent. Checks the source of a
        drag and accepts it if valid.

        PlaylistListView.dragMoveEvent(QEvent) -> None
        """
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def append_item(self, playlist_item):
        """ Appends a given PlaylistItem to the playlist.

        PlaylistListView.append_item(PlaylistItem) -> None
        """
        self.parent.playlist_model.appendRow(playlist_item)
        self.playlist.append_to_playlist(playlist_item.get_file_path())

    def get_drop_position(self, drop_index):
        """ Returns the currect row to insert the new item at based on whether 
        or not the drop position was above or below the halfway mark of the 
        nearest item.

        PlaylistListView.get_drop_position(int) -> int
        """
        if drop_index == -1:
            return drop_index
        elif self.dropIndicatorPosition()\
         == QtGui.QAbstractItemView.DropIndicatorPosition.BelowItem:
            drop_index += 1
        return drop_index

    def create_playlist_item(self, file_path, title = None, artist = None):
        """ Creates a new PlaylistItem with the file_path argument. If the 
        artist and title arguments are empty the metadata is taken from the file
        and then applied to the new PlaylistItem to display.

        PlaylistListView.create_playlist_item(str, str, str) -> PlaylistItem
        """

        playlist_item = PlaylistItem(file_path)
        if title == None or artist == None:
            artist, title = self.metadata.get_playlist_metadata(file_path)
        playlist_item.set_item_metadata(title, artist)
        return playlist_item

    def contextMenuEvent(self, event):
        """ Creates a context menu when an item in the playlist is 
        right-clicked.

        PlaylistListView.contextMenuEvent(QEvent) -> None
        """
        menu = QtGui.QMenu(self)
        menu.addAction(self.main.parent.edit_metadata_action)
        remove_from_playlist_action = QtGui.QAction(
            self.localisation.REMOVE_FROM_PLAYLIST_STRING, self)
        remove_from_playlist_action.triggered.connect(
            self.parent.remove_from_playlist)
        menu.addAction(remove_from_playlist_action)
        menu.exec_(event.globalPos())

class PlaylistItemCoverThread(QtCore.QThread):
    """This is a thread in which the cover art for items in the playlist can be 
    fetched.
    """
    ## This only works if created here.
    thread_done = QtCore.Signal(object, object)

    def __init__(self, items, parent=None):
        super(PlaylistItemCoverThread, self).__init__(parent)
        self.items = items
        self.metadata = metadata.Metadata()

    def run(self):
        """ Goes through all items added to the playlist and gets their
        album covers. The data for the images are added to a list which is then 
        sent back to the class that started the thread. Returns None to 
        close thread.

        PlaylistItemCoverThread.run() -> None
        """
        images = []
        for item in self.items:
            image = self.metadata.get_album_cover(item.get_file_path())
            image_bytes = QtCore.QByteArray(image)
            images.append(image_bytes)
        self.thread_done.emit(self.items, images)
        return None

class PlaylistItem(QtGui.QStandardItem):
    """This is a subclass of Pyside’s QStandardItem class. It formats the item 
    to display the album cover, song name, and artist name. It’s constructed 
    with the song’s file_path, which can then be retrieved from the item when 
    it is chosen for playback.
    """
    def __init__(self, file_path, parent=None):
        super(PlaylistItem, self).__init__(parent)
        self.file_path = file_path
        self.setDragEnabled(True)
        self.setDropEnabled(False)
        self.setEditable(False)

    def set_item_metadata(self, title, artist):
        """ Sets the display for the PlaylistItem. The title and artist are
        set, as well as a placeholder album cover image (which will potentially
        change later depending on if a cover can be found). The item is then
        given a uniform size.

        PlaylistItem.set_item_metadata(str, str) -> None
        """
        self.artist = artist
        self.title = title
        self.setText(title + '\n' + artist)
        album_art = QtGui.QPixmap(DEFAULT_ALBUM_COVER)
        self.setIcon(album_art)
        self.setSizeHint(QtCore.QSize(290, 60))

    def set_item_icon(self, image_bytes):
        """ Changes the icon (i.e. album cover) of the PlaylistItem.

        PlaylistItem.set_item_icon(str) -> None
        """
        pixel_map = QtGui.QPixmap()
        pixel_map.loadFromData(image_bytes)
        self.setIcon(pixel_map)

    def get_file_path(self):
        """ Gets the file_path associated with the PlaylistItem.

        PlaylistItem.get_file_path() -> str
        """
        return self.file_path

    def get_artist(self):
        return self.artist

    def get_title(self):
        return self.title

class PlaylistItemModel(QtGui.QStandardItemModel):
    """This is a subclass of Pyside’s QStandardItemModel class. """
    def __init__(self, parent=None):
        super(PlaylistItemModel, self).__init__(parent)

    def get_item_file_path(self, row):
        """Receives the row number of one of its child items and returns the
        file_path for the item.

        PlaylistItemModel.get_item_file_path(int) -> str
        """
        playlist_item = self.item(row)
        return playlist_item.get_file_path()

class LibraryTableView(QtGui.QTableView):
    """ This is a subclass of Pyside’s QTableView class. The ways in which 
    items are dragged, dropped, and selected have been reimplemented.
    """

    def __init__(self, parent=None):
        super(LibraryTableView, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.main = self.parent.parent.parent.parent
        self.library = self.parent.library
        self.metadata = metadata.Metadata()
        self.setSelectionBehavior(QtGui.QTableView.SelectRows)
        self.verticalHeader().hide()
        self.setDragDropOverwriteMode(False)
        self.setDragEnabled(True)
        self.setDefaultDropAction(QtCore.Qt.LinkAction)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setSortingEnabled(True)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

    def selectionChanged(self, selected, deselected):
        """ Called by QTableView when the selection is changed. Updates the
        status text for the library.

        LibraryTableView.selectionChanged(list(QModelIndex), 
            list(QModelIndex)) -> None
        """
        super(LibraryTableView, self).selectionChanged(selected, deselected)
        self.parent.set_library_status()

    def startDrag(self, supportedActions):
        """ Called by QTableView when internal items are dragged. This function
        had been modified from the standard QTableView.startDrag function in
        order to improve speed.

        LibraryTableView.startDrag(list(Qt.supportedActions)) -> None
        """

        rows = self.selectionModel().selectedRows()
        indexes = []
        for row in rows:
            indexes.append(self.model().index(row.row(), 0))
            indexes.append(self.model().index(row.row(), 1))
            indexes.append(self.model().index(row.row(), 11))
        data = self.model().mimeData(indexes)
        drag = QtGui.QDrag(self)
        drag.setMimeData(data)
        drag.exec_(supportedActions, self.defaultDropAction())

    def dragEnterEvent(self, event):
        """ Called by QTableView when an item is dragged to the table. This
        function had been modified to allow only items from outside the app to
        be dropped on the library (i.e. files).

        LibraryTableView.dragEnterEvent(QEvent) -> None
        """
        if event.source() == None:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """ Called by QTableView when an item is dragged over the table. This
        function had been modified to allow only items from outside the app to
        be dropped on the library (i.e. files).

        LibraryTableView.dragMoveEvent(QEvent) -> None
        """
        if event.source() == None:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """ Called when items are dropped on the table. Checks if the files are
        valid and adds them to the library.

        LibraryTableView.dropEvent(QEvent) -> None
        """

        file_paths = []
        for item in event.mimeData().urls():
            file_path = item.toString()[7:]
            if self.metadata.isValidFile(file_path) and \
            not self.library.file_in_library(file_path):
                file_paths.append(file_path)
        if len(file_paths) > 0:
            self.library.add_files_to_library(file_paths)
            new_track_data = []
            for item in file_paths:
                data = self.library.get_item_data(item)
                new_track_data.append(data)
            self.parent.add_items(new_track_data)

    def contextMenuEvent(self, event):
        """ Creates a context menu when an item in the library is right-clicked.

        LibraryTableView.contextMenuEvent(QEvent) -> None
        """
        menu = QtGui.QMenu(self)
        menu.addAction(self.main.edit_metadata_action)
        add_to_playlist_action = QtGui.QAction(
            self.localisation.ADD_TO_PLAYLIST_STRING, self)
        add_to_playlist_action.triggered.connect(self.add_selected_to_playlist)
        menu.addAction(add_to_playlist_action)
        remove_from_library_action = QtGui.QAction(
            self.localisation.REMOVE_FROM_LIBRARY_STRING, self)
        remove_from_library_action.triggered.connect(
            self.parent.remove_from_library)
        menu.addAction(remove_from_library_action)
        menu.exec_(event.globalPos())

    def add_selected_to_playlist(self):
        """ Adds the selected files to the playlist.

        LibraryTableView.add_selected_to_playlist() -> None
        """
        playlist_widget = self.main.beatbox_gui.playlist_gui.playlist_widget
        new_items = []
        for row in self.parent.selected_rows():
            file_path = self.parent.get_file_path(row)
            playlist_item = playlist_widget.create_playlist_item(file_path)
            playlist_widget.append_item(playlist_item)
            new_items.append(playlist_item)
        self.main.beatbox_gui.playlist_gui.get_album_covers(new_items)

class PreferencesDialog(QtGui.QDialog):
    """ This class creates a dialog window containing the different preferences
     for the application."""
    def __init__(self, parent=None):
        super(PreferencesDialog, self).__init__(parent)
        
        self.parent = parent
        self.preferences = self.parent.preferences
        self.localisation = self.parent.localisation
        self.library = self.parent.beatbox_gui.tabview_gui.library_gui.library
        self.create_preferences_widget()
        self.load_preferences()
        self.pending_actions = []
        self._language_changed_flag = False

    def create_preferences_widget(self):
        """ Creates the GUI for the preferences widget.

        PreferencesDialog.create_preferences_widget() -> None
        """
        layout = QtGui.QVBoxLayout(self)

        language_hbox = QtGui.QHBoxLayout()

        language_label = QtGui.QLabel(self.localisation.LANGUAGE_STRING)
        language_hbox.addWidget(language_label)
        self.language_combo = QtGui.QComboBox()
        self.language_combo.addItem("English")
        self.language_combo.addItem(u"汉语")
        self.language_combo.setCurrentIndex(self.language_combo.findText(
            self.parent.beatbox_gui.get_language()))
        self.language_combo.currentIndexChanged.connect(self.language_changed)
        language_hbox.addWidget(self.language_combo)

        layout.addLayout(language_hbox)
        h_bar = HorizontalBar()
        layout.addWidget(h_bar)

        library_hbox_1 = QtGui.QHBoxLayout()
        dirs_label = QtGui.QLabel(self.localisation.DIRECTORIES_SEARCH_STRING)
        library_hbox_1.addWidget(dirs_label)
        
        self.add_directory_button = QtGui.QPushButton('+', self)
        self.add_directory_button.clicked.connect(self.add_directory)
        self.add_directory_button.setFlat(True)
        library_hbox_1.addWidget(self.add_directory_button)
        self.remove_directory_button = QtGui.QPushButton('-', self)
        self.remove_directory_button.clicked.connect(self.remove_directory)
        self.remove_directory_button.setFlat(True)
        
        library_hbox_1.addWidget(self.remove_directory_button)
        layout.addLayout(library_hbox_1)
        self.directories_list_view = QtGui.QListWidget(self)
        layout.addWidget(self.directories_list_view)

        buttons_hbox = QtGui.QHBoxLayout()
        self.apply_button = QtGui.QPushButton(
            self.localisation.APPLY_STRING, self)
        self.apply_button.clicked.connect(self.apply_preferences)
        buttons_hbox.addWidget(self.apply_button)
        self.cancel_button = QtGui.QPushButton(self.localisation.CANCEL_STRING, 
            self)
        self.cancel_button.clicked.connect(self.reject)
        buttons_hbox.addWidget(self.cancel_button)
        layout.addLayout(buttons_hbox)
        
        self.setWindowTitle(self.localisation.PREFERENCES_STRING)

    def load_preferences(self):
        """ Loads the current preferences.

        PreferencesDialog.load_preferences() -> None
        """
        for d in self.preferences.get_library_dirs_pref():
            self.directories_list_view.addItem(QtGui.QListWidgetItem(d))

    def language_changed(self):
        """ Called when the language combo box is changed. Sets a flag so that
        the lanugage will be checked when apply is clicked.

        Preferences.language_changed() -> None
        """
        self._language_changed_flag = True

    def remove_directory(self):
        """ Removes the selected folder from the library.

        PreferencesDialog.remove_directory() -> None
        """
        for d in self.directories_list_view.selectedItems():
            func = (self.library.remove_directory, d.text())
            self.pending_actions.append(func)
            row = self.directories_list_view.row(d)
            self.directories_list_view.takeItem(row)

    def add_directory(self):
        """ Opens a QFileDialog and queues up the selected folder to be added
        to the library.

        PreferencesDialog.add_directory() -> None
        """
        dialog = QtGui.QFileDialog(self)
        dialog.setFileMode(QtGui.QFileDialog.Directory)
        dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
        new_dir = dialog.getExistingDirectory(
            self, self.localisation.CHOOSE_DIRECTORY_STRING)
        if new_dir != "" and new_dir not in self.library.directories: 
            self.directories_list_view.addItem(new_dir)
            func = (self.library.add_directory, new_dir)
            self.pending_actions.append(func)


    def apply_preferences(self):
        """ Applies all changes to the preferences. 

        PreferencesDialog.apply_preferences() -> None
        """
        new_dirs = False
        for action in self.pending_actions:
            func = action[0]
            if func == self.library.add_directory:
                new_dirs = True
            arg = action[1]
            func(arg)
        if self._language_changed_flag:
            self.parent.beatbox_gui.set_language(
                self.language_combo.currentText())
            self.parent.beatbox_gui.reload_text()
        self.accept() ## Close the dialog
        if new_dirs:
            new_tracks = self.library.update_library()
            self.parent.beatbox_gui.tabview_gui.library_gui.refresh_library()
            self.parent.beatbox_gui.tabview_gui.library_gui.\
            progress_dialog.reset()

class MetadataEditor(QtGui.QDialog):
    """ QDialog that allows the viewing and editing of song metadata.

    """
    def __init__(self, parent=None):
        super(MetadataEditor, self).__init__(parent)
        self.parent = parent
        self.localisation = self.parent.localisation
        self.library_gui = self.parent.beatbox_gui.tabview_gui.library_gui
        self.playlist_gui = self.parent.beatbox_gui.playlist_gui
        self.file_paths = self.get_selected_items()
        if len(self.file_paths) > 1:
            self.create_multiple_items_editor()
        else:
            self.create_single_item_editor()
    
    def get_selected_items(self):
        """ Finds the active view (playlist or library) and gets the file paths
        of the selected songs. Returns the file paths in a list.

        MetadataEditor,get_selected_items() -> list(str)
        """
        if self.playlist_gui.playlist_widget.hasFocus():   
            selected_items = self.playlist_gui.playlist_widget.selectedIndexes()
            return[self.playlist_gui.playlist_model.item(item.row())\
                .get_file_path() for item in selected_items]
        else:  
            selected_rows = self.library_gui.selected_rows()
            return [self.library_gui.get_file_path(row.row()) \
            for row in selected_rows]

    def create_single_item_editor(self):
        """ Creates a QTabWidget for viewing and editing a single track's 
        metadata.

        MetadataEditor.create_single_item_editor() -> None
        """
        self.track = metadata.Track(self.file_paths[0])

        layout = QtGui.QVBoxLayout(self)
        self.tabview_widget = QtGui.QTabWidget(self)
        self.tabview_widget.setTabPosition(QtGui.QTabWidget.West)
        self.info_tab = self.create_info_tab(self.track)
        self.tabview_widget.addTab(self.info_tab, self.localisation.INFO_STRING)
        self.metadata_tab = self.create_metadata_tab(self.track)
        self.tabview_widget.addTab(self.metadata_tab, 
            self.localisation.METADATA_STRING)
        layout.addWidget(self.tabview_widget)

        button_box = QtGui.QHBoxLayout()
        self.apply_button = QtGui.QPushButton(
            self.localisation.APPLY_STRING, self)
        self.apply_button.clicked.connect(self.apply_clicked_single)
        button_box.addWidget(self.apply_button)
        self.cancel_button = QtGui.QPushButton(
            self.localisation.CANCEL_STRING, self)
        self.cancel_button.clicked.connect(self.reject)
        button_box.addWidget(self.cancel_button)
        layout.addLayout(button_box)
        self.setWindowTitle(self.localisation.METADATA_EDITOR_STRING)

    def create_multiple_items_editor(self):
        """ Creates a QWidget for viewing and editing multiple tracks' metadata.

        MetadataEditor.create_multiple_items_editor() -> None
        """
        self.tracks = [metadata.Track(i) for i in self.file_paths]
        md = self.aggregate_metadata(self.tracks)

        layout = QtGui.QVBoxLayout(self)
        self.metadata_widget = self.create_multiple_metadata_layout(md)
        layout.addWidget(self.metadata_widget)

        button_box = QtGui.QHBoxLayout()
        self.apply_button = QtGui.QPushButton(
            self.localisation.APPLY_STRING, self)
        self.apply_button.clicked.connect(self.apply_clicked_multiple)
        button_box.addWidget(self.apply_button)
        self.cancel_button = QtGui.QPushButton(
            self.localisation.CANCEL_STRING, self)
        self.cancel_button.clicked.connect(self.reject)
        button_box.addWidget(self.cancel_button)
        layout.addLayout(button_box)
        self.setWindowTitle(self.localisation.METADATA_EDITOR_STRING)

    def create_info_tab(self, track):
        """ Creates a tab for the given track that display the track's 
        technical metadata. Returns the QWidget to be loaded in the QTabWidget.

        MetadataEditor.create_info_tab(Track) -> QWidget
        """
        info_tab = QtGui.QWidget(self)
        layout = QtGui.QVBoxLayout(info_tab)
        top_box = QtGui.QGridLayout()
        album_cover = QtGui.QLabel()
        cover = metadata.Metadata().get_album_cover(track.file_path)
        if cover == None:
            pixel_map = QtGui.QPixmap(DEFAULT_ALBUM_COVER)
        else:
            pixel_map = QtGui.QPixmap()
            pixel_map.loadFromData(cover)
        album_cover.setPixmap(pixel_map.scaled(PLAYER_COVER_SIZE,\
         PLAYER_COVER_SIZE, QtCore.Qt.KeepAspectRatio,\
          QtCore.Qt.SmoothTransformation))
        top_box.addWidget(album_cover, 0, 0, 0, 2)
        track_label = QtGui.QLabel(track.title)
        top_box.addWidget(track_label, 0, 1)
        artist_label = QtGui.QLabel(track.artist)
        top_box.addWidget(artist_label, 1, 1)
        album_label = QtGui.QLabel(track.album)
        top_box.addWidget(album_label, 2, 1)
        top_box.setColumnStretch(1, 1)
        top_box.setColumnMinimumWidth(0, PLAYER_COVER_SIZE)
        layout.addLayout(top_box)
        h_bar1 = HorizontalBar()
        layout.addWidget(h_bar1)
        middle_box = QtGui.QVBoxLayout()
        format_label = QtGui.QLabel('<b>' + self.localisation.FORMAT_STRING + 
            ': </b>' + track.format)
        middle_box.addWidget(format_label)
        size_label = QtGui.QLabel('<b>' + self.localisation.SIZE_STRING + 
            ': </b>'+ track.size)
        middle_box.addWidget(size_label)
        length_label = QtGui.QLabel('<b>'+ self.localisation.LENGTH_STRING + 
            ': </b>' + track.time)
        middle_box.addWidget(length_label)
        bit_rate_label = QtGui.QLabel(
            '<b>' + self.localisation.BIT_RATE_STRING + ': </b>' \
            + track.bit_rate)
        middle_box.addWidget(bit_rate_label)
        sample_rate_label = QtGui.QLabel('<b>' + 
            self.localisation.SAMPLE_RATE_STRING + ': </b>' + track.sample_rate)
        middle_box.addWidget(sample_rate_label)
        date_modified_label = QtGui.QLabel('<b>' + 
            self.localisation.DATE_MODIFIED_STRING + ': </b>' +\
             track.date_modified)
        middle_box.addWidget(date_modified_label)
        channels_label = QtGui.QLabel(
            '<b>' + self.localisation.CHANNELS_STRING + \
            ': </b>' + track.channels)
        middle_box.addWidget(channels_label)
        layout.addLayout(middle_box)
        h_bar2 = HorizontalBar()
        layout.addWidget(h_bar2)
        bottom_box = QtGui.QVBoxLayout()
        file_path_label = QtGui.QLabel(
            '<b>' + self.localisation.FILE_PATH_STRING + \
            ': </b>' + track.file_path)
        file_path_label.setWordWrap(True)
        bottom_box.addWidget(file_path_label)
        layout.addLayout(bottom_box)
        return info_tab

    def create_metadata_tab(self, track):
        """ Creates a tab for the given track that display the track's 
        song-related metadata. Returns the QWidget to be loaded in the 
        QTabWidget.

        MetadataEditor.create_metadata_tab(Track) -> QWidget
        """

        metadata_tab = QtGui.QWidget(self)
        layout = QtGui.QFormLayout(metadata_tab)
        layout.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        layout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)  
        self.title_textedit = QtGui.QLineEdit(track.title)
        layout.addRow(self.localisation.TITLE_STRING, self.title_textedit)
        self.artist_textedit = QtGui.QLineEdit(track.artist)
        layout.addRow(self.localisation.ARTIST_STRING, self.artist_textedit)
        self.album_textedit = QtGui.QLineEdit(track.album)
        layout.addRow(self.localisation.ALBUM_STRING, self.album_textedit)

        inner_layout = QtGui.QHBoxLayout()
        inner_layout_left = QtGui.QFormLayout()
        inner_layout_left.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)
        inner_layout_left.setFieldGrowthPolicy(
            QtGui.QFormLayout.AllNonFixedFieldsGrow)
        inner_layout_right = QtGui.QFormLayout()
        inner_layout_right.setRowWrapPolicy(QtGui.QFormLayout.WrapAllRows)

        self.genre_textedit = QtGui.QLineEdit(track.genre)
        inner_layout_left.addRow(
            self.localisation.GENRE_STRING, self.genre_textedit)
        self.year_textedit = QtGui.QLineEdit(track.year)
        inner_layout_right.addRow(
            self.localisation.YEAR_STRING, self.year_textedit)
        self.album_artist_textedit = QtGui.QLineEdit(track.album_artist)
        inner_layout_left.addRow(self.localisation.ALBUM_ARTIST_STRING,
         self.album_artist_textedit)


        track_number_row = QtGui.QHBoxLayout()
        self.track_number_textedit = QtGui.QLineEdit(track.track_number)
        track_number_row.addWidget(self.track_number_textedit)
        total_tracks_label = QtGui.QLabel(' / ')
        track_number_row.addWidget(total_tracks_label)
        self.total_tracks_textedit = QtGui.QLineEdit(track.total_tracks)
        track_number_row.addWidget(self.total_tracks_textedit)
        inner_layout_right.addRow(
            self.localisation.TRACK_STRING, track_number_row)

        self.composer_textedit = QtGui.QLineEdit(track.composer)
        inner_layout_left.addRow(self.localisation.COMPOSER_STRING,
         self.composer_textedit)

        disc_number_row = QtGui.QHBoxLayout()
        self.disc_number_textedit = QtGui.QLineEdit(track.disc_number)
        disc_number_row.addWidget(self.disc_number_textedit)
        total_discs_label = QtGui.QLabel(' / ')
        disc_number_row.addWidget(total_discs_label)
        self.total_discs_textedit = QtGui.QLineEdit(track.total_discs)
        disc_number_row.addWidget(self.total_discs_textedit)
        inner_layout_right.addRow(
            self.localisation.DISC_STRING, disc_number_row)

        inner_layout.addLayout(inner_layout_left, 3)
        inner_layout.addSpacing(20)
        inner_layout.addLayout(inner_layout_right, 1)
        layout.addRow(inner_layout)

        self.publisher_textedit = QtGui.QLineEdit(track.publisher)
        layout.addRow(
            self.localisation.PUBLISHER_STRING, self.publisher_textedit)
        self.comments_textedit = QtGui.QTextEdit(track.comment)
        layout.addRow(self.localisation.COMMENTS_STRING, self.comments_textedit)

        return metadata_tab

    def create_multiple_metadata_layout(self, md):
        """ Creates a QWidget in which the metadata of multiple songs can
        be edited. The metadata is loaded from a given dictionary.
        Returns the QWidget to be loaded in MetadataEditor's QDialog.

        MetadataEditor.create_multiple_metadata_layout(dict) -> QWidget
        """
        metadata_widget = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(metadata_widget)
        title_label = QtGui.QLabel(self.localisation.TITLE_STRING)
        layout.addWidget(title_label, 0, 0)
        self.title_textedit = QtGui.QLineEdit(md['title'])
        layout.addWidget(self.title_textedit, 0, 1)
        self.title_checkbox = CheckBox()
        layout.addWidget(self.title_checkbox, 0, 2)
        self.title_textedit.textEdited.connect(self.title_checkbox.set_checked)
        artist_label = QtGui.QLabel(self.localisation.ARTIST_STRING)
        layout.addWidget(artist_label, 1, 0)
        self.artist_textedit = QtGui.QLineEdit(md['artist'])
        layout.addWidget(self.artist_textedit, 1, 1)
        self.artist_checkbox = CheckBox()
        layout.addWidget(self.artist_checkbox, 1, 2)
        self.artist_textedit.textEdited.connect(
            self.artist_checkbox.set_checked)
        album_label = QtGui.QLabel(self.localisation.ALBUM_STRING)
        layout.addWidget(album_label, 2, 0)
        self.album_textedit = QtGui.QLineEdit(md['album'])
        layout.addWidget(self.album_textedit, 2, 1)
        self.album_checkbox = CheckBox()
        layout.addWidget(self.album_checkbox, 2, 2)
        self.album_textedit.textEdited.connect(self.album_checkbox.set_checked)
        genre_label = QtGui.QLabel(self.localisation.GENRE_STRING)
        layout.addWidget(genre_label, 3, 0)
        self.genre_textedit = QtGui.QLineEdit(md['genre'])
        layout.addWidget(self.genre_textedit, 3, 1)
        self.genre_checkbox = CheckBox()
        layout.addWidget(self.genre_checkbox, 3, 2)
        self.genre_textedit.textEdited.connect(self.genre_checkbox.set_checked)
        year_label = QtGui.QLabel(self.localisation.YEAR_STRING)
        layout.addWidget(year_label, 4, 0)
        self.year_textedit = QtGui.QLineEdit(md['year'])
        layout.addWidget(self.year_textedit, 4 , 1)
        self.year_checkbox = CheckBox()
        layout.addWidget(self.year_checkbox, 4, 2)
        self.year_textedit.textEdited.connect(self.year_checkbox.set_checked)
        album_artist_label = QtGui.QLabel(self.localisation.ALBUM_ARTIST_STRING)
        layout.addWidget(album_artist_label, 5, 0)
        self.album_artist_textedit = QtGui.QLineEdit(md['album_artist'])
        layout.addWidget(self.album_artist_textedit, 5 , 1)
        self.album_artist_checkbox = CheckBox()
        layout.addWidget(self.album_artist_checkbox, 5, 2)
        self.album_artist_textedit.textEdited.connect(
            self.album_artist_checkbox.set_checked)
        composer_label = QtGui.QLabel(self.localisation.COMPOSER_STRING)
        layout.addWidget(composer_label, 6, 0)
        self.composer_textedit = QtGui.QLineEdit(md['composer'])
        layout.addWidget(self.composer_textedit, 6 , 1)
        self.composer_checkbox = CheckBox()
        layout.addWidget(self.composer_checkbox, 6, 2)
        self.composer_textedit.textEdited.connect(
            self.composer_checkbox.set_checked)
        publisher_label = QtGui.QLabel(self.localisation.PUBLISHER_STRING)
        layout.addWidget(publisher_label, 7, 0)
        self.publisher_textedit = QtGui.QLineEdit(md['publisher'])
        layout.addWidget(self.publisher_textedit, 7 , 1)
        self.publisher_checkbox = CheckBox()
        layout.addWidget(self.publisher_checkbox, 7, 2)
        self.publisher_textedit.textEdited.connect(
            self.publisher_checkbox.set_checked)
        comments_label = QtGui.QLabel(self.localisation.COMMENTS_STRING)
        layout.addWidget(comments_label, 8, 0)
        self.comments_textedit = QtGui.QTextEdit(md['comment'])
        layout.addWidget(self.comments_textedit, 8 , 1)
        self.comments_checkbox = CheckBox()
        layout.addWidget(self.comments_checkbox, 8, 2)
        self.comments_textedit.textChanged.connect(
            self.comments_checkbox.set_checked)
        track_number_label = QtGui.QLabel(self.localisation.TRACK_NUMBER_STRING)
        layout.addWidget(track_number_label, 9, 0)
        self.track_number_textedit = QtGui.QLineEdit(md['track_number'])
        layout.addWidget(self.track_number_textedit, 9 , 1)
        self.track_number_checkbox = CheckBox()
        layout.addWidget(self.track_number_checkbox, 9, 2)
        self.track_number_textedit.textEdited.connect(
            self.track_number_checkbox.set_checked)
        total_tracks_label = QtGui.QLabel(self.localisation.TOTAL_TRACKS_STRING)
        layout.addWidget(total_tracks_label, 10, 0)
        self.total_tracks_textedit = QtGui.QLineEdit(md['total_tracks'])
        layout.addWidget(self.total_tracks_textedit, 10 , 1)
        self.total_tracks_checkbox = CheckBox()
        layout.addWidget(self.total_tracks_checkbox, 10, 2)
        self.total_tracks_textedit.textEdited.connect(
            self.total_tracks_checkbox.set_checked)
        disc_number_label = QtGui.QLabel(self.localisation.DISC_NUMBER_STRING)
        layout.addWidget(disc_number_label, 11, 0)
        self.disc_number_textedit = QtGui.QLineEdit(md['disc_number'])
        layout.addWidget(self.disc_number_textedit, 11 , 1)
        self.disc_number_checkbox = CheckBox()
        layout.addWidget(self.disc_number_checkbox, 11, 2)
        self.disc_number_textedit.textEdited.connect(
            self.disc_number_checkbox.set_checked)
        total_discs_label = QtGui.QLabel(self.localisation.TOTAL_DISCS_STRING)
        layout.addWidget(total_discs_label, 12, 0)
        self.total_discs_textedit = QtGui.QLineEdit(md['total_discs'])
        layout.addWidget(self.total_discs_textedit, 12, 1)
        self.total_discs_checkbox = CheckBox()
        layout.addWidget(self.total_discs_checkbox, 12, 2)
        self.total_discs_textedit.textEdited.connect(
            self.total_discs_checkbox.set_checked)
        return metadata_widget

    def get_single_item_editor_data(self):
        """ Collects all the metadata displayed in the metadata editor and adds 
        it to a dictionary which is returned.

        MetadataEditor.get_single_item_editor_data() -> dict
        """
        data = {}
        data['title'] = self.title_textedit.text()
        data['artist'] = self.artist_textedit.text()
        data['album'] = self.album_textedit.text()
        data['genre'] = self.genre_textedit.text()
        data['year'] = self.year_textedit.text()
        data['album_artist'] = self.album_artist_textedit.text()
        data['track_number'] = self.track_number_textedit.text()
        data['total_tracks'] = self.total_tracks_textedit.text()
        data['composer'] = self.composer_textedit.text()
        data['disc_number'] = self.disc_number_textedit.text()
        data['total_discs'] = self.total_discs_textedit.text()
        data['publisher'] = self.publisher_textedit.text()
        data['comments'] = self.comments_textedit.toPlainText()
        return data

    def get_multiple_item_editor_data(self):
        """ Collects all the metadata displayed in the metadata editor and adds 
        it to a dictionary which is returned. Only collects metadata that's
        checkbox has been checked.

        MetadataEditor.get_multiple_item_editor_data() -> dict
        """
        data = {}
        if self.title_checkbox.checkState():
            data['title'] = self.title_textedit.text()
        if self.artist_checkbox.checkState():    
            data['artist'] = self.artist_textedit.text()
        if self.album_checkbox.checkState():
            data['album'] = self.album_textedit.text()
        if self.genre_checkbox.checkState():
            data['genre'] = self.genre_textedit.text()
        if self.year_checkbox.checkState():
            data['year'] = self.year_textedit.text()
        if self.album_artist_checkbox.checkState():
            data['album_artist'] = self.album_artist_textedit.text()
        if self.track_number_checkbox.checkState():
            data['track_number'] = self.track_number_textedit.text()
        if self.total_tracks_checkbox.checkState():
            data['total_tracks'] = self.total_tracks_textedit.text()
        if self.composer_checkbox.checkState():
            data['composer'] = self.composer_textedit.text()
        if self.disc_number_checkbox.checkState():
            data['disc_number'] = self.disc_number_textedit.text()
        if self.total_discs_checkbox.checkState():
            data['total_discs'] = self.total_discs_textedit.text()
        if self.publisher_checkbox.checkState():
            data['publisher'] = self.publisher_textedit.text()
        if self.comments_checkbox.checkState():
            data['comments'] = self.comments_textedit.toPlainText()
        return data

    def apply_clicked_single(self):
        """ Called when the apply button is clicked in the single track editor.
        Gets the track's metadata, saves it, then updates the library.

        MetadataEditor.apply_clicked_single() -> None
        """
        data = self.get_single_item_editor_data()
        self.track.save_metadata(data)
        self.library_gui.library.update_file(self.track)
        self.accept()

    def apply_clicked_multiple(self):
        """ Called when the apply button is clicked in the multi-track editor.
        Gets the selected tracks' metadata, saves it, then updates the library.

        MetadataEditor.apply_clicked_multiple() -> None
        """
        data = self.get_multiple_item_editor_data()
        for track in self.tracks:
            track.save_metadata(data)
            self.library_gui.library.update_file(track)
        self.accept()

    def aggregate_metadata(self, tracks):
        """Aggregates the metadata of the selected tracks. If metadata does not
        match an empty string is added to the non-matching tag.

        MetadataEditor.aggregate_metadata(list[Track]) -> dict
        """
        t1 = tracks[0]
        md = {'title':t1.title, 'artist':t1.artist, 'album':t1.album, 
        'album_artist':t1.album_artist, 'genre':t1.genre, 'year':t1.year,
        'track_number':t1.track_number, 'total_tracks':t1.total_tracks, 
        'disc_number':t1.disc_number, 'total_discs':t1.total_discs,
        'composer':t1.composer, 'publisher':t1.publisher, 'comment':t1.comment}
        for t in tracks:
            if t.title != t1.title:
                md['title'] = ""
            if t.artist != t1.artist:
                md['artist'] = ""
            if t.album != t1.album:
                md['album'] = ""
            if t.album_artist != t1.album_artist:
                md['album_artist'] = ""
            if t.genre != t1.genre:
                md['genre'] = ""
            if t.year != t1.year:
                md['year'] = ""
            if t.track_number != t1.track_number:
                md['track_number'] = ""
            if t.total_tracks != t1.total_tracks:
                md['total_tracks'] = ""
            if t.disc_number != t1.disc_number:
                md['disc_number'] = ""
            if t.total_discs != t1.total_discs:
                md['total_discs'] = ""
            if t.composer != t1.composer:
                md['composer'] = ""
            if t.publisher != t1.publisher:
                md['publisher'] = ""
            if t.comment != t1.comment:
                md['comment'] = ""
        return md

class HorizontalBar(QtGui.QFrame):
    """ A QFrame that is transformed to work as a horizontal bar. """
    def __init__(self, parent=None):
        super(HorizontalBar, self).__init__(parent)
        self.setFrameShape(QtGui.QFrame.HLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)

class CheckBox(QtGui.QCheckBox):
    """ Subclass of QCheckBox that adds a function to check the box
    without any arguments.
    """
    def __init__(self, parent=None):
        super(CheckBox, self).__init__(parent)

    def set_checked(self):
        """ Set the CheckBox to be Checked

        CheckBox.set_checked -> None
        """
        self.setCheckState(QtCore.Qt.Checked)

def main():
    """ Main loop for the app.

    main() -> None
    """
    application = QtGui.QApplication(sys.argv)
    pixmap = QtGui.QPixmap(SPLASH_IMAGE)
    splash = QtGui.QSplashScreen(pixmap)
    splash.showMessage("", color = SPLASH_TEXT_COLOUR)
    splash.show()
    splash.raise_()
    main_gui = MainGui(splash)
    on_exit(application.exec_(), main_gui)

def on_exit(app_exit, main):
    """ Called on exiting the app. Saves the preferences.

    on_exit(int, MainGui) -> None
    """

    main.beatbox_gui.playlist.save_playlist()
    main.preferences.save_prefs()
    sys.exit(app_exit)

if __name__ == '__main__':
    main()