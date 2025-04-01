from fabric.widgets.image import Image

from shared import Button, PopOverWindow
from services import network_manager_service
from widgets import NetworkMenu

class Network(Button):
    def __init__(self, bar, **kwargs):
        super().__init__(
            name = "network",
            # style_classes = "bar-widget",
            **kwargs
        )

        self.icon = Image()

        self.client = network_manager_service.build()\
            .connect("notify::state", self.update_icon)\
            .unwrap()

        self.popup= PopOverWindow(
            parent= bar,
            pointing_to=self,
            keyboard_mode= "on-demand",
            child= NetworkMenu(),
            
        )

        self.connect("clicked", lambda _: self.popup.set_visible(not self.popup.get_visible()))
        
        self.add(self.icon)


    def update_icon(self, *_):
        icon = "network-disconnected-symbolic"
        if self.client.wifi_device:
            if self.client.state == "connected-global":
                icon = self.client.wifi_device.active_access_point.icon
            else:
                icon = "network-wireless-disconnected-symbolic"
        if self.client.ethernet_device:
            if self.client.state == "connected-global":
                icon = self.client.ethernet_device.icon_name
            else:
                icon = "network-wired-disconnected-symbolic"
        self.icon.set_from_icon_name(icon_name=icon, icon_size=16)        

