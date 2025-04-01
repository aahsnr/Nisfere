from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.scrolledwindow import ScrolledWindow

from services import notification_service
from shared import Button
from utils.icons import (
    trash as trash_icon,
    trash_empty as trash_empty_icon,
    toggle_off as toggle_off_icon,
    toggle_on as toggle_on_icon
)
from widgets.notification_popup import NotificationWidget


class NotificationsMenu(Box):
    def __init__(self, **kwargs):
        super().__init__(name="notifications-menu", orientation="v",
                         spacing=8, style_classes="menu", **kwargs)

        self.notifications = notification_service.build()\
            .connect("cached-notification-added", self.on_notification_added)\
            .connect("clear-all", self.on_clear_all)\
            .connect("notify::count", self.on_count_changed)\
            .connect("notify::dont-disturb", self.on_dnd_changed)\
            .unwrap()

        self.clear_button = Button(
            label=self.get_clear_button_label(self.notifications.count),
            on_clicked=lambda *args: self.notifications.clear_all_cached_notifications(),
            h_align="end",
            tooltip_text=self.get_clear_button_tooltip(
                self.notifications.count)
        )

        self.dnd_button = Button(
            label=self.get_dnd_button_label(self.notifications.dont_disturb),
            on_clicked=lambda *args: self.notifications.toggle_dnd(),
            h_align="end",
            tooltip_text="Do not disturb"
        )

        self.header = Box(
            style_classes="menu-inner",
            name="notifications-menu-header-box",
            orientation="h",
            spacing=8,
            children=[
                Label(name="notifications-menu-header",
                      label="Notifications", h_expand=True, h_align="start"),
                self.dnd_button,
                self.clear_button
            ]
        )

        self.notifications_box = Box(
            name="notifications-menu-body",
            orientation="v",
            spacing=8,
        )

        self.not_found_label = Label(
            style_classes="menu-inner",
            label="No notifications found!",
            h_align="center",
            h_expand=True,
            v_expand=True,
            v_align="center",
            visible=(self.notifications.count == 0)
        )

        for notification in self.notifications.cached_notifications:
            self.notifications_box.add(
                NotificationWidget(notification=notification, use_cache=True)
            )

        self.scrolled_window = ScrolledWindow(
            style_classes="menu-inner scrollbar",
            name="notifications-menu-scroll-bar",
            min_content_size=(300, 400),
            max_content_size=(350, 400),
            child=self.notifications_box,
            visible=(self.notifications.count > 0)
        )

        self.children = [
            self.header,
            self.not_found_label,
            self.scrolled_window
        ]

    def on_notification_added(self, _, notification):
        self.notifications_box.add(NotificationWidget(
            notification=notification, use_cache=True))

    def on_dnd_changed(self, *args):
        self.dnd_button.set_label(self.get_dnd_button_label(
            self.notifications.dont_disturb))

    def on_count_changed(self, *args):
        self.clear_button.set_label(
            self.get_clear_button_label(self.notifications.count))
        self.clear_button.set_tooltip_text(
            self.get_clear_button_tooltip(self.notifications.count))
        self.not_found_label.set_visible(self.notifications.count == 0)
        self.scrolled_window.set_visible(self.notifications.count > 0)

    def on_clear_all(self, *args):
        for child in self.notifications_box:
            child.destroy()
        self.notifications_box.children = []

    @staticmethod
    def get_clear_button_label(count: int):
        if count > 0:
            return trash_icon
        return trash_empty_icon

    @staticmethod
    def get_clear_button_tooltip(count: int):
        if count > 0:
            return "Clear all"
        return "No notifications found"

    @staticmethod
    def get_dnd_button_label(dnd: bool):
        if dnd:
            return toggle_on_icon
        return toggle_off_icon
