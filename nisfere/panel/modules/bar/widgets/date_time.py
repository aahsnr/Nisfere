import gi
import time
from collections.abc import Iterable
from gi.repository import Gdk

from fabric.widgets.label import Label
from fabric.widgets.widget import Widget

from fabricators.date_fabricator import date_fabricator
from shared import ButtonWithIcon, PopOverWindow
from utils.config import CONFIG
from utils.icons import clock as date_time_icon
from widgets import Calendar

formatters = CONFIG['date-time-formatters']


class DateTime(ButtonWithIcon):
    def __init__(
        self,
        bar: Widget,
        **kwargs
    ):
        super().__init__(style_classes="bar-widget",
                         name="date-time",
                         **kwargs
                         )

        self.add_events("scroll")

        self.formatters = formatters

        self.current_index: int = 0

        self.calendar = Calendar()

        self.popup = PopOverWindow(
            parent=bar,
            pointing_to=self,
            child=self.calendar
        )

        self.set_icon(date_time_icon)

        self.set_text(self.do_format())

        date_fabricator.build().connect("changed", lambda _,
                                        v: self.do_update_label(v)).unwrap()

        self.connect(
            "clicked", lambda *args: self.popup.set_visible(not self.popup.get_visible()))

        self.connect("scroll-event", self.do_handle_scroll)

    def do_format(self, updated_time=time) -> str:
        return updated_time.strftime(self.formatters[self.current_index])

    def do_check_invalid_index(self, index: int) -> bool:
        return (index < 0) or (index > (len(self.formatters) - 1))

    def do_update_label(self, updated_time=time):
        self.set_text(self.do_format(updated_time))
        self.calendar.update_clock_label(updated_time)

    def do_handle_press(self):
        self.calendar.set_visible(not self.calendar.get_visible())

    def do_handle_scroll(self, _, event):
        match event.direction:
            case Gdk.ScrollDirection.UP:  # scrolling up
                self.do_cycle_next()
            case Gdk.ScrollDirection.DOWN:  # scrolling down
                self.do_cycle_prev()
        return

    def do_cycle_next(self):
        self.current_index = self.current_index + 1
        if self.do_check_invalid_index(self.current_index):
            self.current_index = 0  # reset tags

        return self.do_update_label()

    def do_cycle_prev(self):
        self.current_index = self.current_index - 1
        if self.do_check_invalid_index(self.current_index):
            self.current_index = len(self.formatters) - 1

        return self.do_update_label()
