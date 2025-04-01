from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.datetime import DateTime

from utils.helpers import get_profile_picture_path, get_current_uptime

from fabricators.uptime_fabricator import uptime_fabricator

class UserDetails(Box):
    def __init__(self, **kwargs):
        super().__init__(
            spacing = 8,
            orientation = "v",
            style_classes="side-panel-widget",
            **kwargs
        )
        self.profile_pic = Image(
            image_file = get_profile_picture_path(),
            size = (150,120),
            style_classes = "profile-pic"
        )

        uptime_fabricator.build()\
            .connect("changed", lambda _, v: self.on_uptime_value_changed(v))\
            .unwrap()

        self.uptime_label = Label(label = f"{get_current_uptime()}", name = "user-uptime-label")

        self.children = [
            self.profile_pic,
            Box(
                orientation = "v",
                children = [
                    DateTime(
                        name = "panel-date-time",
                    ),
                    self.uptime_label,
                ],
            ),
        ]
        

    def on_uptime_value_changed(self, uptime_value):
        self.uptime_label.set_label(uptime_value)
    