from loguru import logger
import time
import os
from pydbus import SessionBus
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
        self.send_notification(file_path=filename)
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

    def send_notification(self, file_path):
        cmd = ["notify-send"]
        cmd.extend(
            [
                "-A",
                "files=Show in Files",
                "-A",
                "view=View",
                "-A",
                "edit=Edit",
                "-i",
                "camera-photo-symbolic",
                "-a",
                "Fabric Screenshot Utility",
                "-h",
                f"STRING:image-path:{file_path}",
                "Screenshot Saved",
                f"Saved Screenshot at {file_path}",
            ]
        )

        proc: Gio.Subprocess = Gio.Subprocess.new(cmd, Gio.SubprocessFlags.STDOUT_PIPE)

        def do_callback(process: Gio.Subprocess, task: Gio.Task):
            try:
                _, stdout, stderr = process.communicate_utf8_finish(task)
            except Exception:
                logger.error(
                    f"[SCREENSHOT] Failed read notification action with error {stderr}"
                )
                return

            match stdout.strip("\n"):
                case "files":
                    exec_shell_command_async(f"xdg-open {self._screenshots_folder}")
                case "view":
                    exec_shell_command_async(f"xdg-open {file_path}")
                case "edit":
                    exec_shell_command_async(f"swappy -f {file_path}")

        proc.communicate_utf8_async(None, None, do_callback)
