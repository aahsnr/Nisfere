import os
import psutil
import time
import urllib.request
import inspect

from loguru import logger
from gi.repository import GdkPixbuf
from gi.repository import Gio, GLib
from fabric.utils import truncate, get_relative_path

from utils.icons import (
    volume_icons,
    microphone_icons,
    brightness_icons,
    battery_icons,
    media_player_player_icons,
    notification_icons,
    app_icons,
)
from utils.config import CONFIG


def create_inner_widgets(widget_names: list, widget_mapping: dict, bar=None, launcher=None):
    """Create widgets dynamically based on the widget names."""
    widgets = []
    for name in widget_names:
        widget_class = widget_mapping.get(name)
        if widget_class:
            # Inspect the widget's __init__ signature
            parameters = inspect.signature(
                widget_class.__init__).parameters

            # Determine which arguments to pass
            kwargs = {}
            if 'bar' in parameters:
                kwargs['bar'] = bar
            if 'launcher' in parameters:
                kwargs['launcher'] = launcher

            widgets.append(widget_class(**kwargs))
    return widgets


def get_profile_picture_path() -> str | None:
    path = CONFIG["user-picture-path"]
    if not os.path.exists(path):
        path = get_relative_path("../assets/user.png")
    return path

def get_speaker_icon(volume: int, muted: bool):
    if muted:
        return volume_icons["muted"]
    if volume <= 0:
        return volume_icons["no"]
    if volume > 0 and volume < 32:
        return volume_icons["low"]
    if volume > 32 and volume < 66:
        return volume_icons["medium"]
    if volume >= 66 and volume <= 100:
        return volume_icons["high"]
    return volume_icons["default"]


def get_microphone_icon(muted: bool):
    if muted:
        return microphone_icons["muted"]
    return microphone_icons["default"]


def get_brightness_icon(brightness_percentage: int):
    if brightness_percentage < 33:
        return brightness_icons["low"]
    if brightness_percentage > 33 and brightness_percentage < 66:
        return brightness_icons["medium"]
    if brightness_percentage >= 66 and brightness_percentage <= 100:
        return brightness_icons["high"]
    return brightness_icons["default"]


def get_battery_icon(battery_percentage: int, charging: bool):
    icon = f"charging_percentage_" if charging else "percentage_"
    if battery_percentage > 0 and battery_percentage <= 10:
        return battery_icons[f"{icon}10"]
    if battery_percentage > 10 and battery_percentage <= 20:
        return battery_icons[f"{icon}20"]
    if battery_percentage > 20 and battery_percentage <= 30:
        return battery_icons[f"{icon}30"]
    if battery_percentage > 30 and battery_percentage <= 40:
        return battery_icons[f"{icon}40"]
    if battery_percentage > 40 and battery_percentage <= 50:
        return battery_icons[f"{icon}50"]
    if battery_percentage > 50 and battery_percentage <= 60:
        return battery_icons[f"{icon}60"]
    if battery_percentage > 60 and battery_percentage <= 70:
        return battery_icons[f"{icon}70"]
    if battery_percentage > 70 and battery_percentage <= 80:
        return battery_icons[f"{icon}80"]
    if battery_percentage > 80 and battery_percentage <= 90:
        return battery_icons[f"{icon}90"]
    if battery_percentage > 90 and battery_percentage <= 100:
        return battery_icons[f"{icon}100"]
    return battery_icons[f"{icon}100"]


def get_media_player_icon(player_name: str | None) -> str:
    return f"{media_player_player_icons.get(player_name, media_player_player_icons['default'])}"


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
        path = CONFIG.get("default-media-image-path")
        return GdkPixbuf.Pixbuf.new_from_file(path).scale_simple(
            120, 120, GdkPixbuf.InterpType.BILINEAR
        )


def convert_ms(microseconds):
    seconds = (microseconds // 1000000) % 60
    minutes = (microseconds // (1000000 * 60)) % 60
    return f"{minutes}:{seconds:02d}"


def get_notifications_icon(count: int):
    if count > 0:
        return notification_icons["filled"]
    return notification_icons["empty"]


def get_current_uptime():
    uptime = time.time() - psutil.boot_time()
    uptime_days, remainder = divmod(uptime, 86400)
    uptime_hours, remainder = divmod(remainder, 3600)
    return f"{int(uptime_days)} {'days' if uptime_days > 1 else 'day'}, {int(uptime_hours)} {'hours' if uptime_hours > 1 else 'hour'}"


def get_active_window_label(win_class, win_title):
    default_win_name = "Desktop"
    default_icon = app_icons["desktop"]
    return f"{app_icons.get(win_class.lower(), default_icon)} {truncate(win_title, 20) if win_title and win_title != 'unknown' else default_win_name}"


def get_cpu_usage():
    return psutil.cpu_percent()


def get_ram_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage("/").percent


def get_battery_life():
    return psutil.sensors_battery()


def minutes_to_microseconds(minutes):
    return minutes * 60 * 1000000


def run_command_with_output(command, expect_output=True):
    """Executes a shell command and optionally returns the output as a string."""
    try:
        process = Gio.Subprocess.new(
            ["sh", "-c", command],
            Gio.SubprocessFlags.STDOUT_PIPE if expect_output else Gio.SubprocessFlags.NONE,
        )

        if expect_output:
            stdout_stream = process.get_stdout_pipe()
            stdout_reader = Gio.DataInputStream.new(stdout_stream)

            def read_stdout():
                output, _ = stdout_reader.read_line_utf8(None)
                if output:
                    return output.strip()
                return None

            GLib.timeout_add(0, read_stdout)  # Handle asynchronously
            return None  # Return None since we handle output asynchronously

        return None  # If no output is expected, just return None
    except Exception as e:
        logger.error(f"Error executing command: {command} - {e}")
        return None
