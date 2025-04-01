from fabric.widgets.box import Box

from shared import ProgressBarWithIcon
from utils.icons import (
    ram as ram_icon,
    cpu as cpu_icon,
    disk as disk_icon
)
from fabricators.psutil_fabricator import psutil_fabricator


class ProgressBarsContainer(Box):
    def __init__(self, **kwargs):
        super().__init__(
            style_classes="side-panel-widget",
            spacing=8,
            **kwargs
        )

        psutil_fabricator.build()\
            .connect("changed", lambda _, v: self.on_psutil_value_changed(v))\
            .unwrap()

        self.cpu_progress_bar_with_icon = ProgressBarWithIcon(
            progress_bar_name="cpu-progress-bar",
            icon=cpu_icon,
            icon_style="text-shadow: 0 0 10px #fff, 0 0 10px #fff, 0 0 10px #fff;",
            icon_style_classes="cpu-progress-icon"
        )

        self.ram_progress_bar_with_icon = ProgressBarWithIcon(
            progress_bar_name="ram-progress-bar",
            icon=ram_icon,
            icon_style="text-shadow: 0 0 10px #fff, 0 0 10px #fff, 0 0 10px #fff;",
            icon_style_classes="ram-progress-icon"
        )

        self.disk_progress_bar_with_icon = ProgressBarWithIcon(
            progress_bar_name="disk-progress-bar",
            icon=disk_icon,
            icon_style="text-shadow: 0 0 10px #fff, 0 0 10px #fff, 0 0 10px #fff;",
            icon_style_classes="disk-progress-icon"
        )

        self.add(
            Box(
                orientation="h",
                spacing=6,
                h_align="center",
                h_expand=True,
                children=[
                    self.cpu_progress_bar_with_icon,
                    self.ram_progress_bar_with_icon,
                    self.disk_progress_bar_with_icon
                ]
            )
        )

    def on_psutil_value_changed(self, psutil_value):
        self.cpu_progress_bar_with_icon.set_progress_bar_value(
            psutil_value["cpu_usage"])
        self.ram_progress_bar_with_icon.set_progress_bar_value(
            psutil_value["ram_usage"])
        self.disk_progress_bar_with_icon.set_progress_bar_value(
            psutil_value["disk_usage"])
