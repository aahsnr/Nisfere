from gi.repository import Gtk
import gi

from fabric.utils.helpers import exec_shell_command
from fabric.widgets.box import Box

from shared import Button
from utils.config import CONFIG

gi.require_version("Gtk", "3.0")

apps = CONFIG.get('apps')


class Apps(Box):
    def __init__(self, **kwargs):
        super().__init__(
            style_classes="side-panel-widget",
            orientation="h",
            spacing=8,
            h_expand=True,
            **kwargs
        )

        self.grid = Gtk.Grid(
            name="apps-grid",
            row_spacing=8,
            column_spacing=8,
        )

        for index, app in enumerate(apps):

            button = Button(name=f"app-{index}", label=app.get('icon'),
                            h_expand=True, tooltip_text=app.get('label'))

            button.connect("clicked", lambda _, app_name=app.get(
                'name'): self.launch_app(app_name))

            self.grid.attach(button, index % 2, index // 2, 1, 1)

        self.grid.show_all()

        self.add(
            Box(
                spacing=8,
                orientation="h",
                v_align="center",
                h_expand=True,
                children=self.grid
            )
        )

    def launch_app(self, app_name):
        exec_shell_command(f"hyprctl dispatch exec  {app_name}")
