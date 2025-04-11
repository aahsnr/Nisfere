import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.label import Label
from fabric.core import Signal

from shared import Button, ButtonWithIcon
from services import theme_switcher_service
from utils.icons import check_circle as apply_icon
from utils.config import CONFIG
from utils.icons import close as close_icon


class ThemeSwitcherMenu(Box):

    @Signal
    def closed(self) -> None: ...

    def __init__(self, **kwargs):
        super().__init__(name="theme-switcher", style_classes="menu", **kwargs)

        self.theme_switcher = theme_switcher_service.build()\
            .connect("current-theme-changed", lambda *args: self.on_current_theme_changed())\
            .connect("themes-changed", lambda *args: self.on_themes_changed())\
            .unwrap()

        self.selected_theme = None

        self.header = Label(
            name="theme-switcher-menu-header", label="Choose theme", h_align="start", h_expand= True
        )

        self.close_button = Button(
            name="theme-switcher-menu-close",
            label=close_icon,
            v_expand=True,
            h_align="end",
            on_clicked=lambda *args: self.emit("closed"),
        )

        self.buttons_box = Gtk.Grid(
            name="theme-switcher-menu-body", row_spacing=8, column_spacing=8
        )

        self.scrolled_window = ScrolledWindow(
            name="theme-switcher-scroll-bar",
            style_classes="scrollbar",
            size=(620, 350),
            child=self.buttons_box,
        )

        self.color_preview = Gtk.Grid(row_spacing=5, column_spacing=5)

        self.apply_theme_button = ButtonWithIcon(
            name="theme-switcher-menu-apply-button",
            icon=apply_icon,
            text="Apply",
            h_align="center",
            on_clicked=lambda *args: self.apply_theme(),
        )

        self.theme_buttons = {}

        self.add(
            Box(
                style_classes="menu-inner",
                orientation="v",
                spacing=14,
                children=[
                    Box(

                        spacing=14,
                        children= [
                            self.header,
                            self.close_button
                        ]
                    ),
                    self.scrolled_window,
                    self.color_preview,
                    self.apply_theme_button,
                ],
            )
        )
        
        self.on_themes_changed()

        self.on_current_theme_changed()

    def on_themes_changed(self):
        self.theme_buttons = {}

        for child in self.buttons_box.get_children():
            self.buttons_box.remove(child)

        row, col = 0, 0
        for theme in self.theme_switcher.themes:
            theme_box = Box(
                name="theme-switcher-menu-theme",
                spacing=3,
                orientation="v",
                children=[
                    Image(
                        image_file=theme["wallpaper"], size=(150, 80), v_align="start"
                    ),
                    Label(label=theme["name"], v_align="start"),
                ],
            )

            theme_button = Button(
                name="theme-switcher-menu-theme-button",
                child=theme_box,
                on_clicked=lambda _, theme=theme: self.on_theme_selected(theme),
            )

            # Store the button reference in a dictionary with theme name as the key
            self.theme_buttons[theme["name"]] = theme_button

            # Add to grid
            self.buttons_box.attach(theme_button, col, row, 1, 1)

            # Move to next column, wrap to new row if needed
            col += 1
            if col >= 4:
                col = 0
                row += 1

    def on_current_theme_changed(self):
        current_theme_name = self.theme_switcher.current_theme.get(
            "name"
        )  # safely get the current theme name

        if not current_theme_name:
            return  # Exit the function if there's no valid current theme name

        for button in self.theme_buttons.values():
            button.remove_style_class("active")

        # Then, apply the 'active' class to the button for the current theme
        if current_theme_name in self.theme_buttons:
            self.theme_buttons[current_theme_name].add_style_class("active")        
        
        self.on_theme_selected(self.theme_switcher.current_theme)


    def on_theme_selected(self, theme):
        self.selected_theme = theme
        colors = self.theme_switcher.parse_colors(theme["colors"])

        for child in self.color_preview.get_children():
            self.color_preview.remove(child)

        num_colors = len(colors)
        columns = 7 if num_colors >= 14 else 5  # Adjust column count dynamically
        row, col = 0, 0

        # Display new colors as color rectangles
        for name, hex_color in colors.items():
            color_box = Box(
                orientation="v",
                spacing=3,
                children=[
                    Box(
                        name="theme-switcher-menu-color-box",
                        size=(100, 40),
                        style=f"background-color: {hex_color};",
                        children=Label(
                            name="theme-switcher-menu-hex-label",
                            label=hex_color,
                            h_expand=True,
                            h_align="center",
                        ),
                    ),
                    Label(name="theme-switcher-menu-color-name-label", label=name),
                ],
            )

            self.color_preview.attach(color_box, col, row, 1, 1)

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def apply_theme(self):
        if self.selected_theme:
            self.theme_switcher.current_theme = self.selected_theme['name']