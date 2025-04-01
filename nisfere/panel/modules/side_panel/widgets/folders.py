import gi

import os
from fabric.utils.helpers import exec_shell_command_async
from fabric.widgets.box import Box

from shared import ButtonWithIcon
from utils.config import CONFIG

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

folders = CONFIG.get('folders')

class Folders(Box):
    def __init__(self):
        super().__init__(
            style_classes= "side-panel-widget",
            spacing= 8
        )

        self.grid = Gtk.Grid(name= "folders-grid", column_spacing= 8, row_spacing= 8)

        for index, folder in enumerate(folders):

            button = ButtonWithIcon(name= f"folder-{index}", icon= folder.get('icon'), text= folder.get('label'),  tooltip_text= f"Open {folder.get('name')}")

            button.connect("clicked", lambda _, name= folder.get('name'): self.open_folder(name))

            self.grid.attach(button, index % 2, index // 2, 1, 1)

        self.grid.show_all()

        self.add(
            Box(
                spacing= 8,
                orientation="h",
                h_align= "center",
                v_align= "center",
                h_expand= True,
                children= self.grid
            )
        )

    def open_folder(self, folder_name):
        folder_path = os.path.expanduser(f"~/{folder_name}")  # Expands ~ to full path
        command = f"xdg-open '{folder_path}'"
        exec_shell_command_async(command)  # Use async to avoid blocking
