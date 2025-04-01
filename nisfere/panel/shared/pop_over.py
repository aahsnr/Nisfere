import contextlib
import gi
from typing import Literal

from fabric.widgets.wayland import WaylandWindow
from fabric.widgets.box import Box

from gi.repository import Gtk, GtkLayerShell

gi.require_version("GtkLayerShell", "0.1")
gi.require_version("Gtk", "3.0")


class PopOverWindow(WaylandWindow):
    """A popover window to show the content."""

    def __init__(
        self,
        parent: WaylandWindow,
        pointing_to: Gtk.Widget,
        margin: tuple[int, ...] | str = "10px",
        visible=False,
        all_visible=False,
        **kwargs,
    ):
        super().__init__(
            visible=visible,
            all_visible=all_visible,
            **kwargs,
        )

        self._parent = parent
        self._pointing_widget = pointing_to
        self._base_margin = self.extract_margin(margin)
        self.margin = margin
        self.connect("notify::visible", self.do_update_handlers)

    def get_coords_for_widget(self, widget: Gtk.Widget) -> tuple[int, int]:
        if not ((toplevel := widget.get_toplevel()) and toplevel.is_toplevel()):  # type: ignore
            return 0, 0
        allocation = widget.get_allocation()
        x, y = widget.translate_coordinates(toplevel, allocation.x, allocation.y) or (
            0,
            0,
        )
        return round(x / 2), round(y / 2)

    def do_update_handlers(self, *_):
        if not self._pointing_widget:
            return

        if not self.get_visible():
            try:
                self._pointing_widget.disconnect_by_func(self.do_handle_size_allocate)
                self.disconnect_by_func(self.do_handle_size_allocate)
            except Exception:
                pass
            return

        self._pointing_widget.connect("size-allocate", self.do_handle_size_allocate)
        self.connect("size-allocate", self.do_handle_size_allocate)

        return self.do_handle_size_allocate()

    def do_handle_size_allocate(self, *_):
        return self.do_reposition(self.do_calculate_edges())

    def do_calculate_edges(self):
        move_axe = "x"
        parent_anchor = self._parent.anchor

        if len(parent_anchor) != 3:
            return move_axe

        if (
            GtkLayerShell.Edge.LEFT in parent_anchor
            and GtkLayerShell.Edge.RIGHT in parent_anchor
        ):
            # horizontal -> move on x-axies
            move_axe = "x"
            if GtkLayerShell.Edge.TOP in parent_anchor:
                self.anchor = "left top"
            else:
                self.anchor = "left bottom"
        elif (
            GtkLayerShell.Edge.TOP in parent_anchor
            and GtkLayerShell.Edge.BOTTOM in parent_anchor
        ):
            # vertical -> move on y-axies
            move_axe = "y"
            if GtkLayerShell.Edge.RIGHT in parent_anchor:
                self.anchor = "top right"
            else:
                self.anchor = "top left"

        return move_axe

    def do_reposition(self, move_axe: str):
        parent_margin = self._parent.margin
        parent_x_margin, parent_y_margin = parent_margin[0], parent_margin[3]

        height = self.get_allocated_height()
        width = self.get_allocated_width()

        coords = self.get_coords_for_widget(self._pointing_widget)
        
        coords_centered = (
            coords[0] + self._pointing_widget.get_allocated_width() / 2,
            coords[1] + self._pointing_widget.get_allocated_height() / 2,
        )

        # Get screen bounds
        screen = self.get_screen()
        monitor = screen.get_monitor_at_window(self._parent.get_window())
        monitor_geometry = screen.get_monitor_geometry(monitor)

        # Calculate initial X and Y margins
        margin_x = round((parent_x_margin + coords_centered[0]) - (width / 2))
        margin_y = round((parent_y_margin + coords_centered[1]) - (height / 2))

        # Adjust if the popover goes out of bounds
        if margin_x < monitor_geometry.x:
            margin_x = monitor_geometry.x
        elif margin_x + width > monitor_geometry.x + monitor_geometry.width:
            margin_x = monitor_geometry.x + monitor_geometry.width - width

        if margin_y < monitor_geometry.y:
            margin_y = monitor_geometry.y
        elif margin_y + height > monitor_geometry.y + monitor_geometry.height:
            margin_y = monitor_geometry.y + monitor_geometry.height - height

        # Apply margins based on the axis
        self.margin = tuple(
            a + b
            for a, b in zip(
                (
                    (0, 0, 0, margin_x) if move_axe == "x" else (margin_y, 0, 0, 0)
                ),
                self._base_margin.values(),
            )
        )
