from typing import cast

from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow

from services import notification_service, Notification
from widgets import NotificationWidget

class Notifications(WaylandWindow):
    def __init__(self, **kwargs):
        super().__init__(
            name="notifications",
            layer="overlay",
            anchor="top right",
            margin="10px 10px 0px 10px",
            exclusivity="auto",
            visible=False,
            all_visible=False,
            **kwargs,
        )

        self.notifs_service = notification_service.build()\
            .connect('notification-added', self.on_notification_added)\
            .unwrap()

        self.inner_box =  Box(
            size=1, 
            spacing=4,
            orientation="v",
        )

        self.add(self.inner_box)

        self.show_all()

    def on_notification_added(self, _, nid):
        self.inner_box.add(
            NotificationWidget(
                cast(
                    Notification,
                    self.notifs_service.get_notification_from_id(nid),
                )
            )
        )