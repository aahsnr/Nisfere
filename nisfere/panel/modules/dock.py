from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.wayland import WaylandWindow as Window
from fabric.utils.helpers import exec_shell_command_async, truncate

from services import hyprland_clients_service, HyprlandClient
from shared import Button, PopOverWindow
from utils.config import CONFIG
from utils.icons import close as close_icon

from gi.repository import GLib

config = CONFIG['dock-config']
position = config['position']
default_orientation = "h" if position in ("top", "bottom") else "v"

class Dock(Window):
    def __init__(self, **kwargs):
        super().__init__(
            layer="overlay",
            anchor=f"{position} center",
            exclusivity="none",
            **kwargs,
        )

        self.is_hidden = False
        self.hide_id = None
        self.should_hide = False
        self.popup = DockPopup(parent=self,pointing_to=self)

        self.pinned_box = Box(
            orientation=default_orientation,
            spacing=13,
            children=[PinnedDockButton(app=app) for app in config['pinned_apps']]
        )

        self.clients_box = Box(
            orientation=default_orientation,
            spacing=13,
        )

        self.client_buttons = {}

        self.inner_box = Box(
            orientation=default_orientation,
            spacing=13,
            children=[self.pinned_box, self.clients_box]
        )

        self.connect("enter-notify-event", lambda *args: self.on_hover_enter())
        self.connect("leave-notify-event", lambda *args: self.on_hover_leave())

        self.add(self.inner_box)

        self.clients = hyprland_clients_service.build()\
            .connect('initialized', lambda *args: self.on_initialized())\
            .connect('client-added', lambda _, client: self.on_client_added(client))\
            .connect('client-removed', lambda _, client: self.on_client_removed(client))\
            .connect('empty-workspace', lambda *args: self.on_empty_workspace())\
            .connect('filled-workspace', lambda *args: self.on_filled_workspace())\
            .unwrap()

        self.clients.emit("initialized")
        self.show()

    def on_initialized(self):
        for client in self.clients.clients:
            self.on_client_added(client)

    def on_client_added(self, client: HyprlandClient):
        if client.class_name in config['pinned_apps']:
            for button in self.pinned_box:
                if button.app == client.class_name:
                    button.destroy()

        dock_button = self.client_buttons.get(client.class_name)
        if dock_button:
            dock_button.add_client(client)
        else:
            dock_button = DockButton(app=client.class_name, dock=self)
            dock_button.add_client(client)
            self.clients_box.add(dock_button)
            self.client_buttons[client.class_name] = dock_button

    def on_client_removed(self, client: HyprlandClient):
        class_name = client.class_name
        dock_button = self.client_buttons.get(class_name)

        if dock_button:
            dock_button.remove_client(client)
            if not dock_button.clients:
                dock_button.destroy()
                del self.client_buttons[class_name]

        if class_name in config['pinned_apps'] and not any(c.class_name == class_name for c in self.clients.clients):
            self.pinned_box.add(PinnedDockButton(app=class_name))

    def on_empty_workspace(self):
        print(self.is_hidden)
        self.should_hide = False
        self.toggle_dock(True)

    def on_filled_workspace(self):
        self.should_hide = True
        self.delay_hide()

    def on_hover_enter(self):
        self.toggle_dock(True)

    def on_hover_leave(self):
        if self.should_hide:
            self.delay_hide()
    
    def show_popup(self, app, clients):
        self.popup.initlialize_clients(app=app, clients=clients)
        self.popup.set_visible(True)

    def close_popup(self):
        self.popup.set_visible(False)

    def toggle_dock(self, show):
        if show == self.is_hidden:
            self.is_hidden = not show
            self.add_style_class("show-dock" if show else "hide-dock")
            self.remove_style_class("hide-dock" if show else "show-dock")
            if not show:
                self.close_popup()
        if show:
            self.clear_hide_timeout()

    def delay_hide(self):
        self.clear_hide_timeout()
        self.hide_id = GLib.timeout_add(2000, self.hide_dock)

    def hide_dock(self):
        if not self.popup.get_visible():
            self.toggle_dock(False)
            self.hide_id = None
        return False

    def clear_hide_timeout(self):
        if self.hide_id:
            GLib.source_remove(self.hide_id)
            self.hide_id = None

class BaseDockButton(Box):
    def __init__(self, icon_name: str, **kwargs):
        super().__init__(name="dock-button", orientation="v" if position in ("top", "bottom") else "h", **kwargs)
        self.label = Label("●")
        self.image = Image(icon_name=icon_name, icon_size=30)
        self.button = Button(image=self.image, size=40)
        self.button.connect("enter-notify-event", lambda *args: self.on_hover_enter())
        self.button.connect("leave-notify-event", lambda *args: self.on_hover_leave())
        self.children = [self.button, self.label]

    def on_hover_enter(self):
        self.image.set_pixel_size(40)

    def on_hover_leave(self):
        self.image.set_pixel_size(30)

class PinnedDockButton(BaseDockButton):
    def __init__(self, app: str, **kwargs):
        super().__init__(icon_name=app, **kwargs)
        self.app = app
        self.button.connect("clicked", lambda *args: exec_shell_command_async(f"hyprctl dispatch exec {self.app}"))

class DockButton(BaseDockButton):
    def __init__(self, app: str, dock: Dock, **kwargs):
        super().__init__(icon_name=app, **kwargs)
        self.class_name = app
        self.dock = dock
        self.clients = []
        self.button.connect("clicked", lambda *args: self.on_clicked())

    def add_client(self, client: HyprlandClient):
        self.clients.append(client)
        client.connect("closed", lambda *args: self.remove_client(client=client))
        client.connect("changed", lambda *args: self.on_client_changed(changed_client = client))
        if self.dock.popup.app == self.class_name:
            self.dock.popup.add_client(client=client)
        self.on_client_changed()

    def remove_client(self, client: HyprlandClient):
        if client in self.clients:
            self.clients.remove(client)
            if self.dock.popup.app == self.class_name:
                self.dock.popup.remove_client(client=client)

    def on_clicked(self):
        if len(self.clients) == 1:
            exec_shell_command_async(f"hyprctl dispatch focuswindow address:{self.clients[0].address}")
            self.dock.close_popup()
        else:
            self.dock.show_popup(app=self.class_name, clients=self.clients)

    def on_client_changed(self, changed_client: HyprlandClient = None):
        if any(c.focused for c in self.clients):
            self.label.add_style_class("active")
        else:
            self.label.remove_style_class("active")
        
        if changed_client:
            for client in self.clients:
                if client.address == changed_client.address:
                    client= changed_client
        
        if self.dock.popup.app == self.class_name:
            self.dock.popup.update_client(client=changed_client)

class DockPopup(PopOverWindow):
    def __init__(self,parent, pointing_to, **kwargs):
        super().__init__(name="dock-popup",parent=parent,pointing_to=pointing_to, anchor=position,  **kwargs)

        self.app = None

        self.close_button = Button(
            name="dock-popup-close",
            label=close_icon,
            v_expand=True,
            h_align="end",
            on_clicked=lambda *args: self._parent.close_popup()
        )

        self.clients = Box(
            spacing=4,
            orientation="v"
        )

        self.inner = Box(
            spacing=8,
            orientation="v",
            style_classes="menu-inner",
            style=f"margin-{position}: 60px;",
            children=[self.close_button, self.clients]
        )

        self.add(self.inner)

    def initlialize_clients(self, app: str, clients: list[HyprlandClient]):
        self.app = app

        for child in self.clients.children:
            self.clients.remove(child)
            child.destroy()

        for client in clients:
            button = Button(name= "dock-list-button", label=truncate(client.title, 30), on_clicked=lambda *args, client= client: self.focus_client(client=client))
            button._client_ref = client
            if client.focused:
                button.add_style_class("active")
            self.clients.add(button)

    def update_client(self, client: HyprlandClient):
        for child in self.clients.children:
            if getattr(child, '_client_ref', None) == client:
                child.set_label(truncate(client.title, 30))
                if client.focused:
                    child.add_style_class("active")
                else:
                    child.remove_style_class("active")
                break
    
    def add_client(self, client: HyprlandClient):
        button = Button(name= "dock-list-button", label=truncate(client.title, 30), on_clicked=lambda *args: self.focus_client(client=client))
        button._client_ref = client
        if client.focused:
            button.add_style_class("active")
        self.clients.add(button)

    def remove_client(self,  client: HyprlandClient):
        for child in self.inner.children:
            if getattr(child, '_client_ref', None) == client:
                self.clients.remove(child)
                child.destroy()

    def focus_client(self, client: HyprlandClient):
        exec_shell_command_async(f"hyprctl dispatch focuswindow address:{client.address}")
        self._parent.close_popup()