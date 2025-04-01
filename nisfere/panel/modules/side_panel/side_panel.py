from fabric.widgets.box import Box
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.widget import Widget

from modules.side_panel.widgets import *
from shared import PopOverWindow

class SidePanel(PopOverWindow):

    def __init__(self,bar, side_panel_button, launcher: Widget, **kwargs):
        super().__init__(
            parent= bar,
            pointing_to= side_panel_button,
            **kwargs,
        )

        self.user_header = UserHeader()

        self.user_details_box =Box(
            spacing = 8,
            children = [
                UserDetails(size=180),
                PowerButtons(size=70)
            ]
        )

        self.apps_box = Box(
            orientation= "h",
            spacing= 8,
            children=[
                Apps(),
                LauncherApps(launcher= launcher)
            ]
        )

        self.folder_box = Folders()
        
        self.progress_bars_container = ProgressBarsContainer()
        
        self.children = Box(
            name="side-panel-box",
            style_classes="menu",
            size=(250),
            orientation="v",
            spacing=8,
            children=[self.user_header, self.user_details_box, self.apps_box, self.folder_box, self.progress_bars_container],
        )
