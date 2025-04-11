import os
import re
from loguru import logger
from fabric.core import Service, Property, Signal
from fabric.utils import exec_shell_command, monitor_file
from utils.config import CONFIG

class ThemeSwitcher(Service):
    @Signal
    def current_theme_changed(self) -> None: ...
    
    @Signal
    def themes_changed(self) -> None: ...

    @Property(str, "read-write")
    def current_theme(self):
        """Reads the current theme file and return the content which is the current theme."""
        with open(self._current_theme_file, "r") as f:
            current_theme = f.read().strip()

        for theme in self.themes:
            if theme["name"] == current_theme.strip():
                return theme

    @current_theme.setter
    def current_theme(self, value: str):
        exec_shell_command(f"{self._script_path}/change-theme.sh {value}")

    @Property(list, "readable")
    def themes(self):
        """Reads the folders where themes exist and return a list of dicts including the themes"""
        theme_dirs = [self._user_themes_dir, self._deafult_themes_dir]
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

    def __init__(self):
        super().__init__()
        self._current_theme_file = CONFIG["theme-current-path"]
        self._user_themes_dir = CONFIG["user-themes-folder"]
        self._deafult_themes_dir = CONFIG["default-themes-folder"]
        self._script_path = CONFIG["nisfere-scripts-path"]

        self._current_theme_monitor = monitor_file(self._current_theme_file)

        self._current_theme_monitor.connect(
            "changed", lambda *args: self.current_theme_changed.emit())

        self._themes_monitor = monitor_file(self._user_themes_dir)

        self._themes_monitor.connect(
            "changed", lambda *args: self.themes_changed.emit())

    def parse_colors(self, file_path):
        colors = {}
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(r'(\w+)="(#?[A-Fa-f0-9]+)"', line.strip())
                if match:
                    name, hex_value = match.groups()
                    colors[name] = hex_value
        return colors
