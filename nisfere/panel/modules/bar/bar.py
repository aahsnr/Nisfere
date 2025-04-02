from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.box import Box

from modules.bar.widgets import *
from modules.launcher import Launcher
from utils.config import CONFIG
from utils.helpers import create_inner_widgets

config = CONFIG['bar-config']

BAR_WIDGETS_MAPPING = {
    "side_panel_button": SidePanelButton,
    "workspaces": Workspaces,
    "active_window": ActiveWindow,
    "media_player": MediaPlayer,
    "brightness": Brightness,
    "volume": Volume,
    "date_time": DateTime,
    "language": Language,
    "battery": Battery,
    "system_tray": SystemTray,
    "power": Power
}

class StatusBar(Window):
    """Top bar widget """

    def __init__(
        self,
        launcher: Launcher
    ):
        super().__init__(
            name="bar",
            layer="top",
            anchor=f"left {config['position']} right",
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.start_box = Box(
            name="start-container",
            spacing=8,
            children=create_inner_widgets(
                widget_names=config['widgets']['left'], widget_mapping=BAR_WIDGETS_MAPPING, bar=self, launcher=launcher)
        )

        self.center_box = Box(
            name="center-container",
            spacing=8,
            children=create_inner_widgets(
                widget_names=config['widgets']['center'], widget_mapping=BAR_WIDGETS_MAPPING, bar=self)
        )

        self.end_box = Box(
            name="end-container",
            spacing=8,
            children=create_inner_widgets(
                widget_names=config['widgets']['right'], widget_mapping=BAR_WIDGETS_MAPPING, bar=self)
        )

        self.children = CenterBox(
            name="bar-inner",
            start_children=self.start_box,
            center_children=self.center_box,
            end_children=self.end_box
        )

        self.show()
