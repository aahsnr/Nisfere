
import gi
import urllib.request
from io import BytesIO
from typing import Literal
from loguru import logger

from gi.repository import Gdk, GdkPixbuf

from fabric.utils.helpers import get_relative_path, truncate

from utils.config import CONFIG

gi.require_version("Gtk", "3.0")


def setup_cursor_hover(
    button, cursor_name: Literal["pointer", "crosshair", "grab"] = "pointer"
):
    display = Gdk.Display.get_default()

    def on_enter_notify_event(widget, _):
        cursor = Gdk.Cursor.new_from_name(display, cursor_name)
        widget.get_window().set_cursor(cursor)

    def on_leave_notify_event(widget, _):
        cursor = Gdk.Cursor.new_from_name(display, "default")
        widget.get_window().set_cursor(cursor)

    button.connect("enter-notify-event", on_enter_notify_event)
    button.connect("leave-notify-event", on_leave_notify_event)

def get_audio_icon_name(volume: int, is_muted: bool) -> str:
    if is_muted:
        return ""
    if volume <= 0:
        return ""
    if volume > 0 and volume < 32:
        return ""
    if volume > 32 and volume < 66:
        return ""
    if volume >= 66 and volume <= 100:
        return ""
    return ""

def get_microphone_icon(is_muted)-> str:
    if is_muted:
        return "󰍭"
    return "󰍬"

def get_media_player_button_icon(status: str) -> str:
    if status == "playing":
        return "󰏤"
    elif status == "paused":
        return "󰐊"
    else:
        return "󰝛"

def get_window_name(win_class, win_title):
    default_icon = " "
    default_win_name = "Desktop"
    icon_map = CONFIG.get("active_window_icons")
    return f"{icon_map.get(win_class, default_icon)} {truncate(win_title, 20) if win_title else default_win_name}"

def load_image_from_url(url):
    try:
        if not url:
            raise ValueError("Invalid URL")
        
        with urllib.request.urlopen(url) as response:
            loader = GdkPixbuf.PixbufLoader.new()
            loader.write(response.read())
            loader.close()
            pixbuf = loader.get_pixbuf()
            if pixbuf:
                return pixbuf.scale_simple(120, 120, GdkPixbuf.InterpType.BILINEAR)

    except Exception as e:
        logger.warning(f"[Media] Error loading image from {url}: {e}")
        path = get_relative_path(CONFIG.get("default_media_image_path"))
        return GdkPixbuf.Pixbuf.new_from_file(path).scale_simple(120, 120, GdkPixbuf.InterpType.BILINEAR)

def get_media_player_icon(player_name: str) -> str:
    default_icon = ""
    icon_map = CONFIG.get("media_player_icons")
    return f"{icon_map.get(player_name, default_icon)}"

def convert_ms(microseconds):
    seconds = (microseconds // 1000000) % 60
    minutes = (microseconds // (1000000 * 60)) % 60
    return f"{minutes}:{seconds:02d}"