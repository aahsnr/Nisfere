from fabric.core import Service, Property, Signal
from pydbus import SystemBus
from loguru import logger

DeviceState = {
    0: "UNKNOWN",
    1: "CHARGING",
    2: "DISCHARGING",
    3: "EMPTY",
    4: "FULLY_CHARGED",
    5: "PENDING_CHARGE",
    6: "PENDING_DISCHARGE",
}


class Battery(Service):
    @staticmethod
    def seconds_to_hours_minutes(seconds):
        """Converts seconds into a formatted string (hours:minutes)."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"

    @Signal
    def changed(self) -> None: ...

    @Property(int, "readable")
    def percentage(self):
        return int(self._device.Percentage)

    @Property(str, "readable")
    def temperature(self):
        return f"{self._device.Temperature}°C" if hasattr(self._device, "Temperature") else "N/A"

    @Property(str, "readable")
    def time_to_empty(self):
        return self.seconds_to_hours_minutes(getattr(self._device, "TimeToEmpty", 0))

    @Property(str, "readable")
    def time_to_full(self):
        return self.seconds_to_hours_minutes(getattr(self._device, "TimeToFull", 0))

    @Property(str, "readable")
    def icon_name(self):
        return self._device.IconName

    @Property(str, "readable")
    def state(self):
        return DeviceState.get(self._device.State, "UNKNOWN")

    @Property(str, "readable")
    def capacity(self):
        return f"{self._device.Capacity}%"

    @Property(bool, "readable", default_value=False)
    def is_present(self):
        return self._device.IsPresent

    def __init__(self):
        super().__init__()
        self._bus = SystemBus()
        self._device = None
        try:
            self._device = self._bus.get(
                "org.freedesktop.UPower", "/org/freedesktop/UPower/devices/battery_BAT0")
        except KeyError as e:
            logger.error(f"[Battery] Device not found: {e}")
            return
        self._device.PropertiesChanged.connect(self.handle_property_change)
        self.changed.emit()
        logger.info("[Battery] Service initialized.")

    def handle_property_change(self, *args):
        self.changed.emit()
