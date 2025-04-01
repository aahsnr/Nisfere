from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.scale import Scale

from utils.helpers import get_brightness_icon
from services import brightness_service


class BrightnessMenu(Box):

    def __init__(self, **kwargs):
        super().__init__(name="brightness-menu", style_classes="menu", **kwargs)

        self.brightness = (
            brightness_service.build()
            .connect("changed", lambda *args: self.on_changed())
            .unwrap()
        )

        self.header = Label(
            name="brightness-menu-header", label="Brightness", h_align="start"
        )

        self.icon = Label(
            label=get_brightness_icon(self.brightness.brightness_percentage),
            h_align="start",
        )

        self.scale = (
            Scale(
                name="brightness-menu-scale",
                style_classes="scale",
                min_value=0,
                max_value=self.brightness.max_brightness,
                value=self.brightness.brightness,
                h_expand=True,
            )
            .build()
            .connect("button-release-event", lambda *args: self.on_scale_changed())
            .unwrap()
        )

        self.percentage_label = Label(
            name="brightness-menu-percentage-label",
            label=f"{round(self.brightness.brightness_percentage)}%",
            h_align="end",
        )

        self.add(
            Box(
                style_classes="menu-inner",
                spacing=14,
                orientation="v",
                children=[
                    self.header,
                    Box(
                        name="brightness-menu-body",
                        orientation="h",
                        spacing=12,
                        children=[self.icon, self.scale, self.percentage_label],
                    ),
                ],
            )
        )

    def on_changed(self):
        self.scale.value = self.brightness.brightness
        self.percentage_label.set_label(
            f"{round(self.brightness.brightness_percentage)}%"
        )
        self.icon.set_label(get_brightness_icon(self.brightness.brightness_percentage))

    def on_scale_changed(self):
        value = self.scale.get_value()
        self.brightness.brightness = value
