import gi

from fabric.utils.helpers import exec_shell_command
from fabric.widgets.box import Box
from modules.launcher import Launcher

from shared import Button
from utils.config import CONFIG

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

launcher_apps = CONFIG.get('launcher-apps')


class LauncherApps(Box):
    def __init__(self, launcher: Launcher, **kwargs):
        super().__init__(
            style_classes="side-panel-widget",
            orientation="h",
            spacing= 8,
            h_expand= True,
            **kwargs
        )

        self.launcher = launcher

        self.grid = Gtk.Grid(
            name= "launcher-apps-grid",
            row_spacing = 8,
            column_spacing= 8,
        )

        for index, app in enumerate(launcher_apps):

            button = Button(name = f"launcher-app-{index}", label = app.get('icon'), h_expand = True, tooltip_text = app.get('label'))
            
            button.connect("clicked", lambda _, launcher_app=app.get('name'): self.launch_app(launcher_app))
            
            self.grid.attach(button, index % 2, index // 2, 1, 1)
        
        self.grid.show_all()
        
        self.add(
            Box(
                spacing= 8,
                orientation="h",
                v_align= "center",
                h_expand= True,
                children= self.grid
            )
        )

    def launch_app(self, launcher_app):
        self.launcher.open(launcher_app)
    