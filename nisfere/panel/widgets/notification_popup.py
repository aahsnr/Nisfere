from gi.repository import GdkPixbuf

from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.utils.helpers import truncate, invoke_repeater
from services import CachedNotification, Notification
from utils.icons import close as close_icon
from shared import Button

NOTIFICATION_IMAGE_SIZE = 60
NOTIFICATION_TIMEOUT = 10 * 1000  # 10 seconds


class NotificationWidget(Box):
    def __init__(self, notification: CachedNotification | Notification, use_cache=False, **kwargs):
        super().__init__(
            name="notification-popup",
            spacing=8,
            orientation="v",
            style_classes="menu",
            **kwargs,
        )

        self.notification = notification

        if use_cache:
            self.notification.connect(
                "removed-from-cache", lambda *args: self.close())
        else:
            self.notification.connect("closed", lambda *args: self.close())
            invoke_repeater(
                NOTIFICATION_TIMEOUT,
                lambda: self.notification.close("expired"),
                initial_call=False,
            )

        self.summary_label = Label(
            name="notification-popup-summary",
            label=self.notification.summary,
            v_align="start",
            h_align="start"
        )

        self.body_label = Label(
            name="notification-popup-body",
            label=truncate(self.notification.body, 32),
            v_align="start",
            h_align="start",
            v_expand=True
        )

        self.summary_box = Box(
            spacing=8,
            orientation="v",
            h_expand=True,
            children=[
                self.summary_label,
                self.body_label
            ]
        )

        if self.notification.actions and not use_cache:
            actions_box = Box(
                spacing=8,
                orientation="h",
                name="notification-popup-actions",
                h_expand=True,
                v_align="end",
            )

            for action in self.notification.actions:
                actions_box.add(
                    Button(
                        label=action.label,
                        on_clicked=lambda *_, action= action: self.on_action_clicked(
                            action=action),
                        h_expand=True,
                    )
                )
            self.summary_box.add(actions_box)

        self.close_button = Button(
            name="notification-popup-close",
            label=close_icon,
            v_align="center",
            h_align="end",
            on_clicked=lambda *args: (self.notification.remove_from_cache()
                                      if use_cache else self.notification.close()),
        )

        self.notification_box = Box(
            orientation="h",
            spacing=12,
            name="notification-popup-inner"
        )

        if self.notification.image_pixbuf:
            self.notification_box.add(
                Image(
                    h_align="start",
                    pixbuf=self.notification.image_pixbuf.scale_simple(
                        NOTIFICATION_IMAGE_SIZE,
                        NOTIFICATION_IMAGE_SIZE,
                        GdkPixbuf.InterpType.BILINEAR,
                    )
                )
            )

        self.notification_box.add(self.summary_box)

        self.notification_box.add(self.close_button)

        self.add(
            self.notification_box
        )

    def close(self):
        parent = self.get_parent()
        if parent:
            parent.remove(self)
        self.destroy()

    def on_action_clicked(self, action):
        action.invoke()
        self.close()
