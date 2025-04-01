from loguru import logger
import time
import os
from utils.config import CONFIG
from utils.helpers import run_command_with_output
from fabric.utils import exec_shell_command, exec_shell_command_async
from fabric.core import Service, Property, Signal
from gi.repository import GLib, Gio


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
        command = f"wf-recorder --file={self._filename} --pixel-format yuv420p {area}"

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
        self.send_notification()

    def send_notification(self):
        cmd = ["notify-send"]
        cmd.extend(
            [
                "-A",
                "files=Show in Files",
                "-A",
                "view=View",
                "-a",
                "Fabric Screenshot Utility",
                "Screen record Saved",
                f"Saved Screen record at {self._records_folder}",
            ]
        )

        proc: Gio.Subprocess = Gio.Subprocess.new(cmd, Gio.SubprocessFlags.STDOUT_PIPE)

        def do_callback(process: Gio.Subprocess, task: Gio.Task):
            try:
                _, stdout, stderr = process.communicate_utf8_finish(task)
            except Exception:
                logger.error(
                    f"[SCREEN RECORDER] Failed read notification action with error {stderr}"
                )
                return

            match stdout.strip("\n"):
                case "files":
                    exec_shell_command_async(f"xdg-open {self._records_folder}")
                case "view":
                    exec_shell_command_async(f"xdg-open {self._filename}")

        proc.communicate_utf8_async(None, None, do_callback)
