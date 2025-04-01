from fabric.widgets.label import Label
from fabric.widgets.image import Image

from shared import Button, PopOverWindow
from widgets import BluetoothMenu
from services import bluetooth_service

class Bluetooth(Button):

    @staticmethod
    def get_bluetooth_icon(client) -> str:
            """
            Returns the appropriate Bluetooth icon name based on the Bluetooth state.
            """
            if not client.enabled:
                return "bluetooth-disabled-symbolic"  # Bluetooth is off

            if client.scanning:
                return "bluetooth-searching-symbolic"  # Bluetooth is scanning for devices

            if client.connected_devices:
                return "bluetooth-active-symbolic"  # Bluetooth has connected devices

            return "bluetooth-symbolic"  # Default when Bluetooth is on but not connected

    def __init__(self, bar, **kwargs):

        super().__init__(
            name = "bluetooth",
            # style_classes = "bar-widget",
            **kwargs
        )

        self.bluetooth_icon = Image()

        self.client = bluetooth_service.build()\
            .connect("notify::state", self.update_icon)\
            .unwrap()

        self.popup = PopOverWindow(
            parent= bar,
            pointing_to= self,
            child= BluetoothMenu(),
        )
       
        self.connect("clicked", lambda *args: self.popup.set_visible(not self.popup.get_visible()))

        self.add(self.bluetooth_icon)

        self.update_icon()
    
    def update_icon(self, *_):
        self.bluetooth_icon.set_from_icon_name(icon_name=self.get_bluetooth_icon(self.client), icon_size=16)