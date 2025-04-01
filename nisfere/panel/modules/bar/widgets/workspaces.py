from fabric.hyprland.widgets import Workspaces as WorkspacesWidget, WorkspaceButton
from fabric.widgets.box import Box
from utils.widgets import setup_cursor_hover

class Workspaces(WorkspacesWidget):
    def __init__(self, **kwargs):
        super().__init__(
            name= "workspaces",
            style_classes= "bar-widget",
            spacing= 8,
            buttons_factory= lambda ws_id: WorkspaceButton(id=ws_id, label=None),
            **kwargs
        )
        for button in self._buttons.values():
            setup_cursor_hover(button)
        
        for button in self._buttons_preset:
            setup_cursor_hover(button)
