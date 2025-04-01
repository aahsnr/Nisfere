from fabric.widgets.label import Label

from shared import Button
from modules.side_panel.side_panel import SidePanel
from modules.launcher import Launcher
from utils.icons import arch as side_panel_icons

class SidePanelButton(Button):
    def __init__(self, bar, launcher: Launcher, **kwargs):
        super().__init__(
            name = "side-panel-button",
            style_classes = "bar-widget",
            **kwargs
        )
        
        self.side_panel = SidePanel(
            bar= bar,
            side_panel_button= self,
            launcher= launcher
        )
        
        self.set_label(side_panel_icons)

        self.connect("clicked", lambda *args: self.side_panel.set_visible(not self.side_panel.get_visible()))
