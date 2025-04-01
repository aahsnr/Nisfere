from fabric.widgets.wayland import WaylandWindow as Window
from fabric.widgets.box import Box
from loguru import logger

from widgets import *
from shared import PopOverWindow


class Launcher(Window):
    def __init__(self, **kwargs):
        super().__init__(
            layer="top",
            anchor="center",
            on_key_press_event=self.on_key_release,
            visible=False,
            all_visible=False,
            **kwargs,
        )

        self.calendar = Calendar()
        self.volume_menu = VolumeMenu()
        self.power_menu = PowerMenu()
        self.notifications_menu = NotificationsMenu()
        self.app_launcher = AppLauncher().build()\
            .connect('closed', lambda *args: self.close())\
            .unwrap()
        self.screenshot_menu = ScreenshotMenu().build()\
            .connect('closed', lambda *args: self.close())\
            .unwrap()
        self.screen_recorder_menu = ScreenRecorderMenu().build()\
            .connect('closed', lambda *args: self.close())\
            .unwrap()

        self.theme_switcher_menu = ThemeSwitcherMenu()


        self.widgets = {
            "calendar": self.calendar,
            "app_launcher": self.app_launcher,
            "volume_menu": self.volume_menu,
            "power_menu": self.power_menu,
            "screenshot_menu": self.screenshot_menu,
            "screen_recorder_menu": self.screen_recorder_menu,
            "notifications_menu": self.notifications_menu,
            "theme_switcher_menu": self.theme_switcher_menu,
        }

        self.visible_widgets = {key: False for key in self.widgets}

    def open(self, widget_name: str):
        widget = self.widgets.get(widget_name)

        if not widget:
            logger.error(f"[Launcher] Widget '{widget_name}' not found")
            return

        self.close()

        if widget_name == "app_launcher":
            self.app_launcher.open()
            self.app_launcher.search_entry.set_text("")
            self.app_launcher.search_entry.grab_focus()

        self.visible_widgets[widget_name] = True
        self.add(widget)

        self.set_keyboard_mode("exclusive")
        self.show_all()

    def close(self):
        for name, is_visible in self.visible_widgets.items():
            if is_visible:
                if name == "app_launcher":
                    self.app_launcher.close()
                self.visible_widgets[name] = False
                if self.widgets[name] in self.get_children():
                    self.remove(self.widgets[name])

        self.set_keyboard_mode("none")
        self.hide()

    def on_key_release(self, _, event_key):
        if event_key.get_keycode()[1] == 9:
            self.close()
