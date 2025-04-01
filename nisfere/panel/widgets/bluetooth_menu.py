from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.bluetooth import BluetoothClient, BluetoothDevice

from utils.icons import (
    toggle_on as toggle_on_icon,
    toggle_off as toggle_off_icon,
    refresh as refresh_icon,
    connect as connect_icon,
    disconnect as disconnect_icon,
    connecting as connecting_icon,
    scanning as scanning_icon,
)

from shared import Button
from services import bluetooth_service


class BluetoothDeviceSlot(Box):
    def __init__(self, device: BluetoothDevice, **kwargs):
        super().__init__(spacing=8, **kwargs)

        self.device = device

        self.device.connect("changed", self.on_changed)
        self.device.connect(
            "notify::closed", lambda *args: self.device.closed and self.destroy()
        )

        self.connect_button = Button(
            label=connect_icon,
            on_clicked=lambda *args: self.device.set_connecting(
                not self.device.connected
            ),
            h_expand=True,
            h_align="end",
        )

        self.children = [
            Image(icon_name=device.icon_name + "-symbolic", icon_size=16),
            Label(label=device.name),
            self.connect_button,
        ]

        self.device.emit("changed")  # to update display status

    def on_changed(self, *args):
        if self.device.connecting:
            self.connect_button.set_label("󰌚")
        else:
            self.connect_button.set_label(
                connect_icon if not self.device.connected else disconnect_icon
            )
        return


class BluetoothMenu(Box):
    def __init__(self, **kwargs):
        super().__init__(
            name="bluetooth-menu",
            style_classes="menu",
            orientation="v",
            spacing=8,
            **kwargs,
        )

        self.client = (
            bluetooth_service.build()
            .connect("device_added", self.on_device_added)
            .connect(
                "notify::enabled",
                lambda *args: self.toggle_button.set_label(
                    toggle_on_icon if self.client.enabled else toggle_off_icon
                ),
            )
            .connect(
                "notify::scanning",
                lambda *args: self.scan_button.set_label(
                    scanning_icon if self.client.scanning else refresh_icon
                ),
            )
            .unwrap()
        )

        self.header = Label(
            name="bluetooth-menu-header",
            label="Bluetooth",
            h_align="start",
            h_expand=True,
        )

        self.scan_button = Button(
            on_clicked=lambda *args: self.client.toggle_scan(), h_align="end"
        )

        self.toggle_button = Button(
            on_clicked=lambda *args: self.client.toggle_power(), h_align="end"
        )

        self.header_box = Box(
            style_classes="menu-inner",
            name="bluetooth-menu-header-box",
            spacing=8,
            orientation="h",
            children=[self.header, self.toggle_button, self.scan_button],
        )

        self.paired_box = Box(
            spacing=14,
            style_classes="menu-inner scrollbar",
            orientation="v",
            children=Label(
                name="bluetooth-menu-paired-header",
                label="Paired Devices",
                h_align="start",
            ),
        )

        self.available_box = Box(
            spacing=8,
            orientation="v",
            children=Label(
                name="bluetooth-menu-available-header",
                label="Available Devices",
                h_align="start",
            ),
        )

        self.children = [
            self.header_box,
            self.paired_box,
            ScrolledWindow(
                style_classes="menu-inner scrollbar",
                min_content_size=(250, 300),
                max_content_size=(250, 300 * 2),
                child=self.available_box,
            ),
        ]

        self.client.notify("scanning")
        self.client.notify("enabled")

    def on_device_added(self, client: BluetoothClient, address: str):
        if not (device := client.get_device(address)):
            return
        slot = BluetoothDeviceSlot(device)

        if device.paired:
            return self.paired_box.add(slot)
        return self.available_box.add(slot)
