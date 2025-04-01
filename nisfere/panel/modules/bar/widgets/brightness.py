from fabric.widgets.box import Box
from fabric.widgets.label import Label
from shared import Button, ProgressBarWithIcon, PopOverWindow
from utils.helpers import get_brightness_icon
from services import brightness_service
from widgets import BrightnessMenu
from gi.repository import Gdk


class Brightness(Button):
    def __init__(self, bar, **kwargs):
        super().__init__(name="brightness", style_classes="bar-widget", **kwargs)

        # Ensure widget captures scroll events
        self.add_events(Gdk.EventMask.SCROLL_MASK)

        self.brightness = brightness_service

        self.progress_bar = ProgressBarWithIcon(
            progress_bar_name="brightness-progress-bar",
            progress_bar_size=26,
            icon=get_brightness_icon(
                brightness_percentage=100),
            icon_style="font-size: 14px",
            icon_style_classes="brightness-progress-icon",
            value=100,
        )

        self.label = Label("100%")

        self.add(
            Box(
                name="brightness",
                spacing=8,
                orientation="h",
                children=[
                    self.progress_bar,
                    self.label
                ]
            )
        )

        if self.brightness._device:
            self.popup = PopOverWindow(
                parent=bar,
                pointing_to=self,
                child=BrightnessMenu()
            )
            self.brightness.connect(
                "changed", lambda *args: self.on_brightness_changed())
            self.connect("scroll-event", self.on_scroll)
            self.connect(
                "clicked", lambda *args: self.popup.set_visible(not self.popup.get_visible()))

            self.on_brightness_changed()

    def on_scroll(self, widget, event):
        if event.direction == Gdk.ScrollDirection.UP:
            self.brightness.brightness += 8  # Increase brightness
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.brightness.brightness -= 8  # Decrease brightness

    def on_brightness_changed(self):
        self.progress_bar.set_icon(icon=get_brightness_icon(
            brightness_percentage=self.brightness.brightness_percentage))
        self.progress_bar.set_progress_bar_value(
            self.brightness.brightness_percentage)
        self.label.set_label(
            f"{round(self.brightness.brightness_percentage)}%")
