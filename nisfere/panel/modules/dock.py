from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.utils.helpers import exec_shell_command_async

from services import hyprland_clients_service, HyprlandClient
from shared import Button
from utils.config import CONFIG
from gi.repository import GLib

config = CONFIG['dock-config']

default_orientation = "h" if config['position'] in ("top", "bottom") else "v"


class Dock(Window):
    def __init__(self, **kwargs):
        super().__init__(
            layer="overlay",
            anchor=f"{config['position']} center",
            exclusivity="none",
            **kwargs,
        )

        self.is_hidden = False
        self.hide_id = None  # Timeout reference
        self.should_hide = False

        # Pinned apps box
        self.pinned_box = Box(
            orientation=default_orientation,
            spacing=13,
            children=[PinnedDockButton(app=app)
                      for app in config['pinned_apps']]
        )

        # Initialize the service and listen to signals
        self.clients = hyprland_clients_service.build()\
            .connect('initialized', lambda *args: self.on_initialized())\
            .connect('client-added', lambda _, client: self.on_client_added(client))\
            .connect('client-removed', lambda _, client: self.on_client_removed(client))\
            .connect('empty-workspace', lambda *args: self.on_empty_workspace())\
            .connect('filled-workspace', lambda *args: self.on_filled_workspace())\
            .unwrap()

        # Main clients box (to hold active apps)
        self.clients_box = Box(
            orientation=default_orientation,
            spacing=13,
        )

        # Inner box for layout
        self.inner_box = Box(
            orientation=default_orientation,
            spacing=13,
            # style_classes="menu",
            children=[self.pinned_box, self.clients_box]
        )

        self.connect("enter-notify-event", lambda *args: self.on_hover_enter())
        self.connect("leave-notify-event", lambda *args: self.on_hover_leave())

        self.add(self.inner_box)
        # Trigger the initialization
        self.clients.emit("initialized")

        self.show_all()

    def on_empty_workspace(self):
        """Show the dock when workspace is empty."""
        self.should_hide = False
        self.toggle_dock(show=True)

    def on_filled_workspace(self):
        """Delay hiding the dock when workspace is filled."""
        self.should_hide = True
        self.delay_hide()

    def on_hover_enter(self):
        """Show the dock when hovered."""
        self.toggle_dock(show=True)

    def on_hover_leave(self):
        """Delay hiding the dock when mouse leaves."""
        if self.should_hide:
            self.delay_hide()

    def on_initialized(self):
        """Creates all clients in the dock."""
        for client in self.clients.clients:
            self.on_client_added(client)

    def on_client_added(self, client: HyprlandClient):
        """Creates a widget for each individual client, including replacing pinned ones if needed."""
        # If it's a pinned app, we should not add it to the normal client box again.
        if client.class_name in config['pinned_apps']:
            # Find and remove the pinned app button if it's present
            for button in self.pinned_box:
                if button.app == client.class_name:
                    button.destroy()  # Only remove if it's already present

            # Add the new client to the pinned box
            self.clients_box.add(DockButton(client=client))
        else:
            # Add non-pinned app to the dock
            self.clients_box.add(DockButton(client=client))

    def on_client_removed(self, client: HyprlandClient):
        """Handles removing apps and re-pinning if necessary."""
        class_name = client.class_name

        # If it's a pinned app and no instances of it remain, re-pin it
        if class_name in config['pinned_apps']:
            # Check if any other instance of the same app exists
            if not any(c.class_name == class_name for c in self.clients.clients):
                self.pinned_box.add(PinnedDockButton(app=class_name))

    def toggle_dock(self, show):
        """Show or hide the dock."""
        if show:
            if self.is_hidden:
                self.is_hidden = False
                self.add_style_class("show-dock")
                self.remove_style_class("hide-dock")
            if self.hide_id:
                GLib.source_remove(self.hide_id)
                self.hide_id = None
        else:
            if not self.is_hidden:
                self.is_hidden = True
                self.add_style_class("hide-dock")
                self.remove_style_class("show-dock")

    def delay_hide(self):
        """Schedule hiding the dock after a short delay."""
        if self.hide_id:
            GLib.source_remove(self.hide_id)
        self.hide_id = GLib.timeout_add(2000, self.hide_dock)

    def hide_dock(self):
        """Actually hide the dock."""
        self.toggle_dock(show=False)
        self.hide_id = None
        return False


class PinnedDockButton(Box):
    def __init__(self, app: str, **kwargs):
        super().__init__(
            name="dock-button",
            orientation="v" if config['position'] in (
                "top", "bottom") else "h",
            **kwargs
        )

        self.app = app

        self.image = Image(icon_name=self.app, icon_size=25)
        self.button = Button(image=self.image, size=35)
        self.label = Label("●")

        self.children = [
            self.button,
            self.label
        ]

        self.button.connect("clicked", lambda *args: self.on_clicked())
        self.button.connect("enter-notify-event",
                            lambda *args: self.on_hover_enter())
        self.button.connect("leave-notify-event",
                            lambda *args: self.on_hover_leave())

    def on_clicked(self):
        exec_shell_command_async(f"hyprctl dispatch exec {self.app}")

    def on_hover_enter(self):
        """Make button icon bigger when hovered."""
        self.image.set_pixel_size(35)

    def on_hover_leave(self):
        """Make button icon back to the default size when mouse leaves."""
        self.image.set_pixel_size(24)


class DockButton(Box):
    def __init__(self, client: HyprlandClient, **kwargs):
        super().__init__(
            name="dock-button",
            orientation="v" if config['position'] in (
                 "top", "bottom") else "h",
            **kwargs
        )
        self.client = client

        self.client.connect("closed", lambda *args: self.destroy())
        self.client.connect("changed", lambda *args: self.on_changed())

        self.label = Label("●")
        self.image = Image(icon_name=self.client.class_name, icon_size=25)
        self.button = Button(image=self.image, size=35)

        self.children = [
            self.button,
            self.label
        ]

        self.button.connect("clicked", lambda *args: self.on_clicked())
        self.button.connect("enter-notify-event",
                            lambda *args: self.on_hover_enter())
        self.button.connect("leave-notify-event",
                            lambda *args: self.on_hover_leave())

        self.client.changed.emit()

    def on_clicked(self):
        exec_shell_command_async(
            f"hyprctl dispatch focuswindow address:{self.client.address}")

    def on_changed(self):
        if self.client.focused:
            self.label.add_style_class("active")
        else:
            self.label.remove_style_class("active")

    def on_hover_enter(self):
        """Make button icon bigger when hovered."""
        self.image.set_pixel_size(35)

    def on_hover_leave(self):
        """Make button icon back to the default size when mouse leaves."""
        self.image.set_pixel_size(24)
