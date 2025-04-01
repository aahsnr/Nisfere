import time
from gi.repository import GLib

from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.entry import Entry

from shared import Button
from utils.icons import (
    connect as connect_icon,
    disconnect as disconnect_icon,
    toggle_on as toggle_on_icon,
    toggle_off as toggle_off_icon,
    refresh as scan_icon,
    check_circle as check_icon,
    close_circle as close_icon,
    download as download_icon,
    upload as upload_icon
)
from services import Wifi, network_manager_service, Ethernet, AccessPoint


class NetworkMenu(Box):
    @staticmethod
    def get_network_button_label(network_status: bool):
        if network_status:
            return toggle_on_icon
        return toggle_off_icon

    def __init__(self, **kwargs):
        super().__init__(
            orientation="v",
            spacing=8,
            style_classes="menu",
            **kwargs
        )

        self.client = network_manager_service.build()\
            .connect('ethernet-device-added', self.on_ethernet_device_added)\
            .connect('wifi-device-added', self.on_wifi_device_added)\
            .connect('notify::networking-enabled', self.on_networking_enabled)\
            .unwrap()

        self.toggle_network = Button(
            label=self.get_network_button_label(
                self.client.networking_enabled),
            on_clicked=lambda *args: self.client.toggle_network(),
            h_expand=True,
            h_align="end",
            tooltip_text="Enable/Disable"
        )

        self.add(
            Box(
                name="network-menu-header-box",
                style_classes="menu-inner",
                orientation="h",
                spacing=8,
                children=[
                    Label(name="network-menu-header", label="Network",
                          h_expand=True, h_align="start"),
                    self.toggle_network
                ]
            )
        )

    def on_networking_enabled(self, *args):
        self.toggle_network.set_label(
            self.get_network_button_label(self.client.networking_enabled))

    def on_ethernet_device_added(self, *args):
        if self.client.ethernet_device:
            self.add(EthernetBox(device=self.client.ethernet_device))

    def on_wifi_device_added(self, *args):
        if self.client.wifi_device:
            self.add(WifiBox(device=self.client.wifi_device))


class EthernetBox(Box):
    def __init__(self, device: Ethernet, **kwargs):
        super().__init__(
            style_classes="menu-inner",
            spacing=8,
            orientation="v",
            name="ethernet-menu",
            **kwargs
        )

        self.device = device.build()\
            .connect("changed", lambda *args: self.update_ui())\
            .connect("notify::speed", lambda *args: self.on_speed_changed())\
            .unwrap()

        self.header = Label(label="Ethernet", h_align="start")

        self.inner = Box(orientation="h", spacing=12)

        self.icon = Image(
            icon_name='network-wired-disconnected-symbolic', icon_size=30, h_align="start")

        self.status = Label(name="ethernet-summary-status",
                            label="Disconnected", h_align="start")

        self.speed = Label(name="ethernet-summary-speed",
                           label="Not available", h_align="start")

        self.summary = Box(
            orientation="v",
            spacing=8,
            children=[
                self.status,
                self.speed,
            ]
        )

        self.inner.children = [
            self.icon,
            self.summary
        ]

        self.children = [
            self.header,
            self.inner
        ]
        self.previous_rx, self.previous_tx = self.device.get_network_stats()
        self.previous_time = time.time()
        # Update every 1 second
        GLib.timeout_add(1000, self.update_speed_display)
        self.update_ui()

    def update_ui(self, *args):
        if self.device:
            self.icon.set_from_icon_name(
                self.device.icon_name, icon_size=30)
            self.status.set_label(self.device.internet.capitalize())

    def update_speed_display(self):
        current_rx, current_tx = self.device.get_network_stats()
        current_time = time.time()
        time_diff = current_time - self.previous_time

        if time_diff == 0:
            return True

        # Calculate speeds in Mbps using correct formula
        download_speed_mbps = (
            (current_rx - self.previous_rx) * 8) / (time_diff * 1_000_000)
        upload_speed_mbps = ((current_tx - self.previous_tx)
                             * 8) / (time_diff * 1_000_000)

        self.speed.set_label(
            f"{download_icon} {download_speed_mbps:.2f} Mbps | {upload_icon} {upload_speed_mbps:.2f} Mbps")

        # Update previous values
        self.previous_rx, self.previous_tx = current_rx, current_tx
        self.previous_time = current_time

        return True  # Continue the timeout


class WifiBox(Box):
    @staticmethod
    def get_wifi_button_label(wifi_status: bool):
        if wifi_status is True:
            return toggle_on_icon
        return toggle_off_icon

    def __init__(self, device: Wifi, **kwargs):
        super().__init__(
            name="wifi-menu",
            style_classes="menu-inner",
            spacing=8,
            orientation="v",
            **kwargs
        )

        self.device = device.build()\
            .connect('notify::wireless-enabled', self.update_header)\
            .connect('ap-added', lambda _,
                     ap: self.add_access_point(ap=ap))\
            .connect('ap-removed', lambda _,
                     ap: self.remove_access_point(ap=ap))\
            .unwrap()

        self.header_label = Label(
            name="wifi-menu-header", label="Wi-Fi", h_align="start")

        self.toggle_button = Button(
            name='wifi-menu-toggle-button',
            label=self.get_wifi_button_label(
                wifi_status=self.device.wireless_enabled),
            on_clicked=lambda *args: self.device.toggle_wifi(),
            tooltip_text="Enable/Disable"
        )

        self.scan_button = Button(label=scan_icon, name='wifi-menu-scan-button',
                                  on_clicked=lambda *args: self.device.scan(), tooltip_text="Scan")

        self.header_buttons = Box(
            orientation="h",
            spacing=4,
            name="wifi-menu-header-buttons",
            h_expand=True,
            h_align="end",
            children=[
                self.toggle_button,
                self.scan_button
            ]
        )

        self.header = Box(
            orientation="h",
            spacing=8,
            name="wifi-menu-header-box",
            children=[
                self.header_label,
                self.header_buttons
            ]
        )

        self.networks = Box(name="wifi-menu-networks",
                            orientation="v", spacing=15)

        self.scrolled_window = ScrolledWindow(
            style_classes="scrollbar",
            min_content_size=(250, 300),
            max_content_size=(250, 300*2),
            child=self.networks,
        )

        self.children = [
            self.header,
            self.scrolled_window
        ]

        self.update_header()
        self.update_networks()

    def update_header(self, *args):
        self.toggle_button.set_label(
            self.get_wifi_button_label(self.device.wireless_enabled))
        if self.device.wireless_enabled:
            self.scrolled_window.set_visible(True)
            self.header_buttons.children = [
                self.toggle_button,
                self.scan_button
            ]
        else:
            self.header_buttons.children = self.toggle_button
            self.scrolled_window.set_visible(False)

    def add_access_point(self, ap):
        self.networks.add(
            AccessPointBox(ap=ap, wifi_widget=self)
        )

    def update_networks(self, *args):
        self.networks.children = []
        for ap in self.device.access_points:
            self.networks.add(
                AccessPointBox(ap=ap, wifi_widget=self)
            )

    def remove_access_point(self, ap):
        for child in self.networks.get_children():
            if child.ap == ap:  # Assuming AccessPointBox has an `ap` attribute
                self.networks.remove(child)
                break  # Exit loop after removing the correct one


class AccessPointBox(Box):
    def __init__(self, ap: AccessPoint, **kwargs):
        super().__init__(
            name="access-point",
            orientation="v",
            spacing=8,
            **kwargs
        )

        self.ap = ap

        self.ap.connect("changed", self.on_changed)

        self.icon = Image(icon_name=self.ap.icon, icon_size=16)

        self.connect_button = Button(
            name="wifi-connect-button", label=connect_icon, h_expand=True, h_align="end", tooltip_text="Connect")

        self.update_connect_button()

        self.password_entry = WifiPasswordEntry(
            ap=ap) if self.ap.requires_password else None

        self.add(
            Box(
                orientation="h",
                spacing=8,
                children=[
                    self.icon,
                    Label(label=self.ap.ssid),
                    self.connect_button
                ]
            ),
        )
        if self.password_entry:
            self.add(self.password_entry)

    def update_connect_button(self):
        if self.ap.is_active:
            self.connect_button.set_label(disconnect_icon)
            self.connect_button.set_tooltip_text("Disconnect")
            self.connect_button.connect(
                "clicked", lambda *args: self.ap.device.disconnect_wifi())
        else:
            self.connect_button.set_label(connect_icon)
            if not self.ap.requires_password:
                self.connect_button.set_tooltip_text("Connect")
                self.connect_button.connect(
                    "clicked", lambda *args: self.ap.device.connect_to_wifi(ap=self.ap))
            else:
                self.connect_button.set_tooltip_text("Needs password")
                self.connect_button.connect(
                    "clicked", lambda *args: self.create_password_entry())

    def create_password_entry(self):
        if self.password_entry:
            self.password_entry.set_visible(
                not self.password_entry.get_visible())

    def on_changed(self, *args):
        self.icon.set_from_icon_name(icon_name=self.ap.icon, icon_size=14)
        self.update_connect_button()


class WifiPasswordEntry(Box):
    def __init__(self, ap: AccessPoint, **kwargs):
        super().__init__(
            name="wifi-menu-password",
            orientation="v",
            spacing=8,
            visible=False,
            all_visible=False,
            **kwargs
        )
        self.ap = ap

        self.password_entry = Entry(name="wifi-menu-password-entry",
                                    placeholder="Enter password", h_expand=True, h_align="start")

        self.connect_button = Button(label=check_icon, on_clicked=lambda *args: self.wifi_password_connect(
        ), h_expand=True, h_align="end", tooltip_text="Connect")

        self.close_button = Button(
            label=close_icon, on_clicked=lambda *args: self.remove(), h_align="end", tooltip_text="Close")

        self.add(
            Box(
                orientation="h",
                spacing=8,
                h_expand=True,
                children=[
                    self.password_entry,
                    self.connect_button,
                    self.close_button
                ]
            )
        )

    def remove(self):
        self.set_visible(False)

    def wifi_password_connect(self):
        self.ap.device.connect_to_wifi(
            ap=self.ap, password=self.password_entry.get_text()) and self.remove()
