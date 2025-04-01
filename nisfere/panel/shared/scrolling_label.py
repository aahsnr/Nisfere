
import gi

from fabric.widgets.label import Label

gi.require_version("Gtk", "3.0")
from gi.repository import GLib

class ScrollingLabel(Label):
    def __init__(
        self,
        scroll_label = "",
        scroll_speed = 1000,
        width = 20,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.scroll_speed = scroll_speed  # Lower = Faster
        self.width = width  # Fixed display width
        self.current_index = 0
        self.timeout_id = None
        self.set_scroll_label(scroll_label)
        
    def start_scrolling(self):
        """Start the scrolling effect"""
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
        self.timeout_id = GLib.timeout_add(self.scroll_speed, self.scroll_text)

    def scroll_text(self):
        """Shifts the text left while keeping a fixed size"""
        self.current_index += 1
        if self.current_index + self.width > len(self.scroll_label):
            self.current_index = 0  # Loop back to start
        self.set_label(self.scroll_label[self.current_index : self.current_index + self.width])
        return True

    def set_scroll_label(self, scroll_label: str):
        if (len(scroll_label) > self.width):
            self.scroll_label = f"   {scroll_label}   "
            self.set_label(self.scroll_label[: self.width])
            self.start_scrolling()
        else:
            self.scroll_label = scroll_label
            self.set_label(self.scroll_label)