from fabric.widgets.box import Box
from fabric.widgets.label import Label

from services import  MediaPlayerService, MediaManager
from shared import Button, ScrollingLabel
from utils.helpers import get_media_player_icon
from utils.icons import media_player_icons, media_player_player_icons
from widgets import MediaPlayerMenu

class MediaPlayer(Button):
    def __init__(self, bar, **kwargs):
        super().__init__(name= "media-player", style_classes= "bar-widget", spacing= 8, orientation= "h", **kwargs)

        self.bar = bar

        self.media_manager = MediaManager().build()\
            .connect("notify::current-player", self.on_current_player_changed)\
        .unwrap()
        
        self.media_player = self.media_manager.current_player

        self.media_menu = None

        self.icon = Label(label= media_player_player_icons['default'])
        
        self.label = ScrollingLabel(scroll_label= "Music")

        self.connect("clicked", self.toggle_menu)

        self.add(
            Box(
                name= self.get_name(),
                spacing= 4,
                orientation= "h",
                children= [
                    self.icon,
                    self.label
                ]
            )
        )

        self.media_manager.notify('current-player')

    def on_current_player_changed(self, *_):
        """Called when the media player changes."""
        if self.media_manager.current_player:
            self.media_player = self.media_manager.current_player
            self.media_player.connect("notify::track", self.update_widget)
        else:
            if self.media_player:
                self.media_player.disconnect_by_func(self.update_widget)
            self.media_player = None

        self.update_widget()
        self.update_media_menu()

    def update_widget(self, *_):
        """Update the media player icon and track name."""
        if self.media_player:
            track = self.media_player.track
            icon = get_media_player_icon(self.media_player.player_name)
        else:
            track = "Music"
            icon = media_player_player_icons['default']

        self.icon.set_label(icon)
        self.label.set_scroll_label(track)

    def update_media_menu(self):
        if self.media_player:
            if not self.media_menu:
                self.media_menu = self.create_media_menu()
            else:
                self.media_menu.on_exit()
                self.media_menu = self.create_media_menu()
        else:
            if self.media_menu : self.media_menu = None

    def toggle_menu(self, *_):
        """Toggle the media player menu visibility."""
        if not self.media_menu:
            return  # No active player, do nothing
        self.media_menu.set_visible(not self.media_menu.get_visible())

    def create_media_menu(self):
        return MediaPlayerMenu(media_player= self.media_player, pointing_to= self, parent= self.bar)

