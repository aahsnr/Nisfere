from loguru import logger

from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.scale import Scale

from fabric.utils.helpers import (
    invoke_repeater,
    bulk_connect,
    bulk_disconnect,
    get_relative_path,
)

from services import MediaPlayerService, MediaManager

from shared import Button, ScrollingLabel, PopOverWindow

from utils.config import CONFIG
from utils.icons import media_player_icons
from utils.helpers import load_image_from_url, convert_ms


class MediaPlayerMenu(PopOverWindow):
    def __init__(self, media_player: MediaPlayerService, **kwargs):
        super().__init__(name="media-player-menu", **kwargs)

        self.user_interacting = False
        self.timeout_id = None

        self.media_player = media_player

        self.track_title_label = ScrollingLabel(
            name="track-title", h_align="start")
        self.track_artist_label = Label(name="track-artist", h_align="start")

        self.previous_button = Button(
            label=media_player_icons["previous"],
            on_clicked=lambda *args: self.media_player.previous(),
            h_expand=True,
        )

        self.next_button = Button(
            label=media_player_icons["next"],
            on_clicked=lambda *args: self.media_player.next(),
            h_expand=True,
        )

        self.play_button = Button(
            on_clicked=lambda *args: self.media_player.play_pause(), h_expand=True
        )

        self.track_position_label = Label(
            name="track-position", h_align="start", h_expand=True
        )

        self.track_duration_label = Label(
            name="track-duration", h_align="end", h_expand=True
        )

        self.buttons_box = Box(
            orientation="h",
            spacing=8,
            name="media-player-menu-buttons",
            children=[
                self.track_position_label,
                self.previous_button,
                self.play_button,
                self.next_button,
                self.track_duration_label,
            ],
        )

        self.track_scale = (
            Scale(
                name="track-position-scale",
                style_classes="scale",
                min_value=0,
                h_expand=True,
            )
            .build()
            .connect("button-press-event", lambda *args: self.on_scale_start())
            .connect("button-release-event", lambda *args: self.on_scale_end())
            .unwrap()
        )

        self.song_mgmt_box = Box(
            orientation="v",
            spacing=13,
            h_expand=True,
            v_align="center",
            children=[
                self.track_title_label,
                self.track_artist_label,
                self.track_scale,
                self.buttons_box,
            ],
        )

        self.song_image = Image(name="media-image")

        bulk_connect(
            self.media_player,
            {
                "notify::track": self.on_track_changed,
                "notify::track-duration": self.on_track_duration_changed,
                "notify::track-position": self.on_track_position_changed,
                "notify::album-image-url": self.on_album_image_url_changed,
                "notify::status": self.on_playback_status_changed,
                "exit": self.on_exit,
            },
        )

        invoke_repeater(1000, self.update_scale)

        self.add(
            Box(
                style_classes="menu",
                children=[
                    Box(
                        style_classes="menu-inner",
                        orientation="h",
                        name=self.get_name(),
                        spacing=13,
                        children=[self.song_image, self.song_mgmt_box],
                    )
                ],
            )
        )

        self.update_ui()

    def on_exit(self, *args):
        """Properly clean up the menu on exit."""
        if self.media_player:
            bulk_disconnect(
                self.media_player,
                [
                    self.on_track_changed,
                    self.on_track_duration_changed,
                    self.on_track_position_changed,
                    self.on_album_image_url_changed,
                    self.on_playback_status_changed,
                    self.on_exit,
                ],
            )
            self.media_player = None

        self.destroy()

    def update_ui(self):
        self.on_playback_status_changed()
        self.on_track_changed()
        self.on_track_duration_changed()
        self.on_track_position_changed()
        self.on_album_image_url_changed()

    def on_playback_status_changed(self, *args):
        self.play_button.set_label(
            media_player_icons.get(self.media_player.status))

    def on_track_changed(self, *args):
        self.track_title_label.set_scroll_label(self.media_player.track_title)
        self.track_artist_label.set_label(self.media_player.track_artist)

    def on_album_image_url_changed(self, *args):
        self.song_image.set_from_pixbuf(
            load_image_from_url(self.media_player.album_image_url)
        )

    def on_track_position_changed(self, *args):
        self.track_scale.set_value(self.media_player.get_position())
        self.track_position_label.set_label(
            convert_ms(self.media_player.get_position())
        )

    def on_track_duration_changed(self, *args):
        self.track_duration_label.set_label(
            convert_ms(self.media_player.track_duration)
        )
        self.track_scale.set_max_value(self.media_player.track_duration)

    def on_scale_start(self):
        """Flag that the user started interacting with the scale"""
        self.user_interacting = True

    def on_scale_end(self):
        """Flag that the user finished interacting with the scale"""
        self.seek_to_position()
        self.user_interacting = False

    def seek_to_position(self):
        """Seek to a new position in the track"""
        new_position = int(self.track_scale.get_value())
        try:
            self.media_player.track_position = new_position
            self.track_scale.set_value(new_position)
            self.track_position_label.set_label(convert_ms(new_position))
            logger.info(f"[Media] Seeking to {new_position} ms")
        except Exception as e:
            logger.error(f"[Media] Error seeking: {e}")

    def update_scale(self):
        """Update the scale position if the player is active."""
        if not self.media_player:
            return False

        if not self.user_interacting:
            if self.media_player.status == "playing":
                self.track_scale.set_value(self.media_player.get_position())
                self.track_position_label.set_label(
                    convert_ms(self.media_player.get_position()) or "0:00"
                )

        return True
