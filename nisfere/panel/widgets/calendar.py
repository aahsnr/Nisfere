import gi
import time

from fabric.widgets.box import Box
from fabric.widgets.label import Label

from fabricators.date_fabricator import date_fabricator
from utils.config import CONFIG

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Calendar(Box):
    def __init__(self, **kwargs):
        super().__init__(
            name="calendar", orientation="v", spacing=8, style_classes="menu", **kwargs
        )

        self.clock_label = Label(
            name="calendar-clock-label",
            style_classes="menu-inner",
            label=time.strftime(CONFIG["calendar-clock-formatter"]),
        )

        self.calendar = Box(
            style_classes="menu-inner",
            children=Gtk.Calendar(
                visible=True,
                hexpand=True,
                halign=Gtk.Align.CENTER,
            ),
        )

        self.children = [self.clock_label, self.calendar]

    def update_clock_label(self, updated_time: time):
        self.clock_label.set_label(
            updated_time.strftime(CONFIG["calendar-clock-formatter"])
        )
