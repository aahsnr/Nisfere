from fabric.widgets.box import Box
from modules.bar.widgets import Bluetooth, Network, Recording, NotificationButton
from utils.helpers import create_inner_widgets
from utils.config import CONFIG

config = CONFIG['system-tray-config']

SYSTEM_TRAY_WIDGETS_MAPPING = {
    "bluetooth": Bluetooth,
    "network": Network,
    "notifications": NotificationButton,
    "stop_recording": Recording,
}


class SystemTray(Box):
    def __init__(self, bar, **kwargs):
        super().__init__(name="system-tray", spacing=8, style_classes="bar-widget", **kwargs)

        self.children = create_inner_widgets(
            widget_names=config['widgets'], widget_mapping=SYSTEM_TRAY_WIDGETS_MAPPING, bar=bar)
