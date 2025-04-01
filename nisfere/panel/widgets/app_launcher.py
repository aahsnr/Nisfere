import gi

from collections.abc import Iterator

from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.entry import Entry
from fabric.widgets.scrolledwindow import ScrolledWindow

from fabric.utils import DesktopApp, get_desktop_applications, idle_add
from fabric.core import Signal

from shared import Button, PopOverWindow
from utils.icons import apps as apps_icon, close as close_icon

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class AppLauncher(Box):
    @Signal
    def closed(self) -> None: ...

    def __init__(self, **kwargs):
        super().__init__(
            name="app-launcher",
            orientation="v",
            spacing=8,
            style_classes="menu",
            **kwargs,
        )

        self._arranger_handler: int = 0
        self._all_apps = []
        self.closed = False
        self.viewport = Gtk.Grid(column_spacing=10, row_spacing=10)

        self.viewport.connect("key-press-event", self.on_key_press)

        self.scrolled_window = ScrolledWindow(
            name="app-launcher-scroll-bar",
            style_classes="scrollbar",
            size=(620, 350),
            child=self.viewport,
        )

        self.icon_header = Label(
            name="app-launcher-icon", label=apps_icon, v_expand=True, h_align="center"
        )

        self.search_entry = Entry(
            name="app-launcher-entry",
            placeholder="Search Applications...",
            h_expand=True,
            notify_text=lambda entry, *args: self.arrange_viewport(entry.get_text()),
        )

        self.close_button = Button(
            name="app-launcher-close",
            label=close_icon,
            v_expand=True,
            h_align="center",
            on_clicked=lambda *args: self.emit("closed"),
        )

        self.children = [
            Box(
                name="app-launcher-box",
                orientation="h",
                spacing=14,
                children=[self.icon_header, self.search_entry, self.close_button],
            ),
            self.scrolled_window,
        ]

    def on_key_press(self, widget, event):
        toplevel = widget.get_toplevel()

        buttons = [
            child for child in widget.get_children() if isinstance(child, Button)
        ]
        if not buttons:
            return False  # No buttons to navigate

        # Get currently focused widget
        focused_widget = toplevel.get_focus()

        if focused_widget not in self.viewport.get_children():
            buttons[0].grab_focus()  # Default focus to first button
            return True

        index = buttons.index(focused_widget)
        cols = 2

        # Wrapping logic for Down and Up keys
        if event.keyval == Gdk.KEY_Down:
            new_index = (
                index - cols if index - cols >= 0 else index + (len(buttons) - cols)
            )
        elif event.keyval == Gdk.KEY_Up:
            new_index = (
                index + cols
                if index + cols < len(buttons)
                else index - (len(buttons) - cols)
            )

        else:
            return False  # Ignore other keys

        buttons[new_index].grab_focus()  # Move focus to new button
        return True

    def arrange_viewport(self, query: str = ""):
        for child in self.viewport.get_children():
            child.destroy()
            self.viewport.remove(child)

        col = 1
        row = 0

        filtered_apps_iter = iter(
            [
                {"col": col, "row": row, "app": app}
                for app in self._all_apps
                if query.casefold()
                in (
                    (app.display_name or "")
                    + (" " + app.name + " ")
                    + (app.generic_name or "")
                ).casefold()
                if (col := col + 1) % 2 != 0 or (col := 0) is col and (row := row + 1)
            ]
        )

        self._arranger_handler = idle_add(
            self.add_next_application, filtered_apps_iter, pin=True
        )

        return False

    def add_next_application(self, apps_iter: Iterator[dict]):
        if not (app_dict := next(apps_iter, None)):
            return False

        app: DesktopApp = app_dict.get("app")
        col: int = app_dict.get("col")
        row: int = app_dict.get("row")

        app_button = self.bake_application_slot(app)

        self.viewport.attach(app_button, col, row, 1, 1)

        return True

    def bake_application_slot(self, app: DesktopApp, **kwargs) -> Button:
        return Button(
            name="app-launcher-button",
            child=Box(
                orientation="h",
                spacing=12,
                children=[
                    Image(pixbuf=app.get_icon_pixbuf(size=24), h_align="start"),
                    Label(
                        label=app.display_name or "Unknown",
                        v_align="center",
                        h_align="center",
                    ),
                ],
            ),
            tooltip_text=app.description,
            on_clicked=lambda *_: (app.launch(), self.emit("closed")),
            h_expand=True,
            **kwargs,
        )

    def close(self, *_):
        self._all_apps = []
        self.viewport.children = []

    def open(self):
        self._all_apps = get_desktop_applications()
        self.arrange_viewport("")
