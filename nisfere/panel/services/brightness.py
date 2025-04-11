import os
from loguru import logger
from fabric.core import Service, Property, Signal
from fabric.utils import exec_shell_command_async, monitor_file


class Brightness(Service):
    @Signal
    def changed(self) -> None: ...

    @Property(int, "readable")
    def max_brightness(self):
        try:
            with open(self._max_brigthness_path) as f:
                return int(f.read().strip())
        except Exception as e:
            logger.error(f"[Brightness] Error reading max brightness: {e}")
            return -1

    @Property(int, "read-write")
    def brightness(self):
        """Reads brightness as a percentage from sysfs."""
        try:
            with open(self._brightness_path) as f:
                return int(f.read().strip())
        except Exception as e:
            logger.error(f"[Brightness] Error reading brightness: {e}")
            return -1

    @brightness.setter
    def brightness(self, value: int):
        if not (0 <= value <= self.max_brightness):
            value = max(0, min(value, self.max_brightness))
        try:
            exec_shell_command_async(
                f"brightnessctl --device '{self._device}' set {value}")
            logger.info(f"[Brightness] Set screen brightness to {value} ")
        except Exception as e:
            logger.exception(
                f"[Brightness] Unexpected error setting screen brightness: {e}")

    @Property(str, "readable")
    def brightness_percentage(self):
        return int((self.brightness / self.max_brightness) * 100)

    def __init__(self):
        super().__init__()
        self._device = None

        try:
            screen_device = os.listdir("/sys/class/backlight")
            if screen_device:
                self._device = screen_device[0]
        except FileNotFoundError:
            logger.error(
                f"[Brightness] No backlight devices found, brightness control disabled")
            return

        self._backlight_path = "/sys/class/backlight"

        self._max_brigthness_path = f"{self._backlight_path}/{self._device}/max_brightness"
        self._brightness_path = f"{self._backlight_path}/{self._device}/brightness"

        self._screen_monitor = monitor_file(self._brightness_path)

        self._screen_monitor.connect(
            "changed", lambda *args: self.changed.emit())

    def get_max_brightness(self):
        with open(f"{BACKLIGHT_PATH}/max_brightness") as f:
            return int(f.read().strip())
