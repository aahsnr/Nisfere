import time
import os
import threading
from loguru import logger
from pydbus import SessionBus
from utils.config import CONFIG
from utils.helpers import run_command_with_output
from fabric.utils import exec_shell_command, exec_shell_command_async
from fabric.core import Service, Property, Signal
from gi.repository import GLib


class ScreenRecorder(Service):

    @Property(bool, "readable", default_value=False)
    def is_recording(self) -> bool:
        return self._is_recording

    def __init__(self):
        super().__init__()
        self._records_folder = CONFIG["screen-records-folder"]
        self._filename = None
        self._is_recording = False

    def _generate_filename(self):
        return f"{self._records_folder}/record_{time.strftime('%Y-%m-%d_%H-%M-%S')}.mp4"

    def start_recording(self, fullscreen: bool):
        if self._is_recording:
            return

        self._is_recording = True
        self.notify("is_recording")
        self._filename = self._generate_filename()

        area = "" if fullscreen else f'-g "$(slurp)"'
        command = f"wf-recorder --audio --file={self._filename} --pixel-format yuv420p {area}"

        GLib.timeout_add(
            500,
            lambda: run_command_with_output(command=command, expect_output=False)
            or False,
        )

    # Specific functions for each action
    def stop_recording(self):
        if not self._is_recording:
            return
        self._is_recording = False
        self.notify("is_recording")
        run_command_with_output("pkill -INT wf-recorder", expect_output=False)
        self._send_notification()

    def _send_notification(self):
        def notify():
            try:
                # Use pydbus to get the session bus and the Notifications object
                bus = SessionBus()
                notifications = bus.get("org.freedesktop.Notifications", "/org/freedesktop/Notifications")

                actions = [
                    "files", "Show in Files",
                    "view", "View",
                ]

                hints = {
                    "urgency": GLib.Variant("y", 1),  # Use byte type for urgency
                }

                # Send the notification to the D-Bus
                notification_id = notifications.Notify(
                    "Nisfere",
                    0,
                    "camera-photo-symbolic",
                    "Screen Record Saved",
                    f"Saved screen record at {self._filename}",
                    actions,
                    hints,
                    3000  # Timeout in milliseconds
                )

                # Define callback for the action invoked signal
                def on_action_invoked(id, key):
                    logger.info(f"Notification action: {key}")
                    if key == "files":
                        exec_shell_command_async(f"xdg-open {self._records_folder}")
                    elif key == "view":
                        exec_shell_command_async(f"xdg-open {self._filename}")

                # Assign the callback to the ActionInvoked signal
                notifications.onActionInvoked = on_action_invoked

            except Exception as e:
                logger.error(f"[SCREEN RECORDER] Failed to send notification: {e}")

        # Run the notification in a separate thread to avoid blocking
        GLib.timeout_add(0, lambda: threading.Thread(target=notify, daemon=True).start())