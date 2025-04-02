from fabric.widgets.image import Image
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from shared import Button, ButtonWithIcon
from services import battery_service
from utils.helpers import get_battery_icon


class Battery(ButtonWithIcon):
    def __init__(self, **kwargs):
        super().__init__(
            name="battery",
            style_classes="bar-widget",
            **kwargs
        )
        self.show_time = False

        self.battery = battery_service.build()\
            .connect("changed", lambda *args: self.update_ui())\
            .unwrap()

        self.connect("clicked", lambda *args: self.toggle_display())
        self.set_text("100%")
        self.set_icon(get_battery_icon(battery_percentage=100, charging=False))

        if self.battery._device:
            self.update_ui()

    def update_ui(self):
        """Update the button icon and label."""
        self.set_text(self.battery.time_to_full if self.battery.state ==
                      "CHARGING" else self.battery.time_to_empty) if self.show_time else self.set_text(f"{self.battery.percentage}%")
        self.set_icon(get_battery_icon(self.battery.percentage,
                      self.battery.state == "CHARGING"))
        self.set_tooltip_text(self.battery.time_to_full if self.battery.state ==
                              "CHARGING" else self.battery.time_to_empty)

        self.icon_label.add_style_class(
            'low') if self.battery.percentage <= 20 else self.icon_label.remove_style_class('low')
        self.text_label.add_style_class(
            'low') if self.battery.percentage <= 20 else self.text_label.remove_style_class('low')

    def toggle_display(self):
        """Toggle between percentage and time remaining on click."""
        self.show_time = not self.show_time
        self.set_text(self.battery.time_to_full if self.battery.state ==
                      "CHARGING" else self.battery.time_to_empty) if self.show_time else self.set_text(f"{self.battery.percentage}%")
