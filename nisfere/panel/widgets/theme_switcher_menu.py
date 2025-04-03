import os
import re
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.label import Label
from fabric.utils import exec_shell_command, monitor_file

from shared import Button, ButtonWithIcon
from utils.icons import check_circle as apply_icon
from utils.config import CONFIG


class ThemeSwitcherMenu(Box):
    @staticmethod
    def get_available_themes():
        user_themes_dir = CONFIG["user-themes-folder"]
        deafult_themes_dir = CONFIG["default-themes-folder"]
        theme_dirs = [user_themes_dir, deafult_themes_dir]
        themes = []
        for theme_dir in theme_dirs:
            if not os.path.exists(theme_dir):  # Skip if directory doesn't exist
                continue
            for theme_name in os.listdir(theme_dir):
                theme_path = os.path.join(theme_dir, theme_name)
                wallpaper = None
                colors_file = None

                if os.path.isdir(theme_path):
                    for file in os.listdir(theme_path):
                        if file.endswith((".jpg", ".png")):
                            wallpaper = os.path.join(theme_path, file)
                        elif file == "colors.sh":
                            colors_file = os.path.join(theme_path, file)

                    if wallpaper and colors_file:
                        themes.append(
                            {
                                "name": theme_name,
                                "wallpaper": wallpaper,
                                "colors": colors_file,
                            }
                        )

        return themes

    @staticmethod
    def parse_colors(file_path):
        colors = {}
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(r'(\w+)="(#?[A-Fa-f0-9]+)"', line.strip())
                if match:
                    name, hex_value = match.groups()
                    colors[name] = hex_value
        return colors

    def __init__(self, **kwargs):
        super().__init__(name="theme-switcher", style_classes="menu", **kwargs)

        self.current_theme = None

        self.themes = self.get_available_themes()

        self.header = Label(
            name="theme-switcher-menu-header", label="Choose theme", h_align="start"
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

        row, col = 0, 0
        for theme in self.themes:
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

        self.add(
            Box(
                style_classes="menu-inner",
                orientation="v",
                spacing=14,
                children=[
                    self.header,
                    self.scrolled_window,
                    self.color_preview,
                    self.apply_theme_button,
                ],
            )
        )
        self.current_theme_file = monitor_file(CONFIG["theme-current-path"])
        self.current_theme_file.connect(
            "changed", lambda *args: self.get_current_theme()
        )
        self.get_current_theme()

        self.on_theme_selected(self.current_theme)

    def get_current_theme(self):
        current_theme_file = CONFIG["theme-current-path"]

        with open(current_theme_file, "r") as f:
            current_theme = f.read().strip()

        for theme in self.themes:
            if theme["name"] == current_theme.strip():
                self.current_theme = theme

        self.apply_active_class_to_current_theme()

    def apply_active_class_to_current_theme(self):
        current_theme_name = self.current_theme.get(
            "name"
        )  # safely get the current theme name

        if not current_theme_name:
            return  # Exit the function if there's no valid current theme name

        for button in self.theme_buttons.values():
            button.remove_style_class("active")

        # Then, apply the 'active' class to the button for the current theme
        if current_theme_name in self.theme_buttons:
            self.theme_buttons[current_theme_name].add_style_class("active")

    def apply_theme(self):
        script_path = CONFIG["nisfere-scripts-path"]
        output = exec_shell_command(f"{script_path}/change-theme.sh {self.current_theme['name']}")

    def on_theme_selected(self, theme):
        self.current_theme = theme
        colors = self.parse_colors(theme["colors"])

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
