import time
import os
from pydbus import SessionBus
import threading
from loguru import logger
from utils.config import CONFIG
from utils.helpers import run_command_with_output
from fabric.utils import invoke_repeater, exec_shell_command_async
from fabric.core import Service, Property, Signal
from gi.repository import Gio, GLib, Gtk, Notify

class Screenshot(Service):

    @Signal
    def screenshot_saved(self) -> None: ...

    def __init__(self):
        super().__init__()
        self._screenshots_folder = CONFIG["screenshots-folder"]

    def _generate_filename(self):
        return f"{self._screenshots_folder}/screenshot_{time.strftime('%Y-%m-%d_%H-%M-%S')}.png"

    def _capture(self, command: str):
        filename = self._generate_filename()
        command = f"{command} {filename}"
        run_command_with_output(command=command)
        self._send_notification(file_path=filename)
        return False

    # Specific functions for each action
    def capture_desktop(self, *args):
        self.screenshot_saved.emit()
        GLib.timeout_add(500, lambda: self._capture(f"grim"))

    def capture_window(self, *args):
        self.screenshot_saved.emit()
        GLib.timeout_add(
            500,
            lambda: self._capture(
                "grim -c -o \"$(hyprctl activeworkspace -j | jq -r '.monitor')\""
            ),
        )

    def capture_area(self, *args):
        self.screenshot_saved.emit()
        GLib.timeout_add(500, lambda: self._capture('grim -g "$(slurp)"'))

    # Inside your class...
    def _send_notification(self, file_path):
        def notify():
            try:
                bus = SessionBus()
                notifications = bus.get("org.freedesktop.Notifications", "/org/freedesktop/Notifications")

                actions = [
                    "files", "Show in Files",
                    "view", "View",
                    "edit", "Edit"
                ]

                hints = {
                    "urgency": GLib.Variant("y", 1),  # Use y (byte) for urgency
                    # "image-path": GLib.Variant("s", file_path)  # You can add image if needed
                }

                notification_id = notifications.Notify(
                    "Nisfere",
                    0,
                    "camera-photo-symbolic",
                    "Screenshot Saved",
                    f"Saved screenshot at {file_path}",
                    actions,
                    hints,
                    3000
                )

                # pydbus allows connecting to signals too
                def on_action_invoked(id, key):
                    logger.info(f"Notification action: {key}")
                    if key == "files":
                        exec_shell_command_async(f"xdg-open {self._screenshots_folder}")
                    elif key == "view":
                        exec_shell_command_async(f"xdg-open {file_path}")
                    elif key == "edit":
                        exec_shell_command_async(f"swappy -f {file_path}")

                # Connect the ActionInvoked signal
                notifications.onActionInvoked = on_action_invoked

            except Exception as e:
                logger.error(f"[SCREENSHOT] Failed to send notification: {e}")

        threading.Thread(target=notify, daemon=True).start()
