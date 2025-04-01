from fabric.hyprland.widgets import ActiveWindow as ActiveWindowWidget
from fabric.utils import FormattedString
from fabric.widgets.box import Box

from utils.helpers import get_active_window_label

class ActiveWindow(ActiveWindowWidget):
    """A widget that displays the title of the active window."""
        
    def __init__(self, **kwargs):
        super().__init__(
            name="active-window",
            style_classes="bar-widget",
            formatter=FormattedString(
                string="{get_window_name(win_class,win_title)}",
                get_window_name = lambda win_class, win_title:
                    get_active_window_label(
                        win_class=win_class,
                        win_title=win_title
                    )
                ),
            **kwargs
        )
        
