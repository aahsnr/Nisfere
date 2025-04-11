
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window

from shared import Button, PopOverWindow
from widgets import PowerMenu
from utils.icons import power as power_icon

class Power(Button):
    def __init__(self,bar, **kwargs):
        super().__init__(name= "power", style_classes= "bar-widget", **kwargs)
        
        self.popup = PopOverWindow(
            parent= bar,
            pointing_to= self,
            child= PowerMenu().build().connect("closed", lambda *args: self.toggle()).unwrap()
        )

        self.set_label(power_icon)

        self.connect("clicked", lambda *args: self.toggle())

    def toggle(self):
        self.popup.set_visible(not self.popup.get_visible())
