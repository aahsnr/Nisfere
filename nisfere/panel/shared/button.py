from fabric.widgets.button import Button
from utils.widgets import setup_cursor_hover

class ButtonWidget(Button):
    """A button widget with fixed cursor hover."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        setup_cursor_hover(self)
