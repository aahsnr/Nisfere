from fabric.widgets.label import Label
from fabric.widgets.wayland import WaylandWindow as Window

from services import notification_service
from shared import Button, PopOverWindow
from utils.helpers import get_notifications_icon
from widgets import NotificationsMenu

class NotificationButton(Button):
    def __init__(self, bar, **kwargs):
        super().__init__(
            name = "notiifcation-button",
            # style_classes="bar-widget",
            **kwargs
        )
                
        self.label = Label()

        self.notifications = notification_service.build()\
            .connect("notify::count", self.on_count_changed)\
        .unwrap()

        self.popup= PopOverWindow(
            parent= bar,
            child= NotificationsMenu(),
            pointing_to= self
        )

        self.connect("clicked", lambda *args : self.popup.set_visible(not self.popup.get_visible()))

        self.notifications.notify('count')

        self.add(self.label)

    def on_count_changed(self, *args):
        self.label.set_label(get_notifications_icon(self.notifications.count))


