from fabric.widgets.box import Box
from fabric.widgets.overlay import Overlay
from fabric.widgets.label import Label
from fabric.widgets.circularprogressbar import CircularProgressBar


class ProgressBarWithIcon(Box):
    """A progress bar widget with icon inside."""
    
    def __init__(
        self,
        progress_bar_name: str = "progress-bar",
        progress_bar_size: int = 64,
        progress_bar_style_calesses= "progress-bar",
        icon: str= "",
        icon_style: str= "",
        icon_style_classes: str= "progress-icon",
        **kwargs
    ):
        super().__init__(
            orientation = "h",
            **kwargs
        )

        self.progress_bar = self.bake_progress_bar(name=progress_bar_name, size =progress_bar_size, style_classes= progress_bar_style_calesses, **kwargs)

        self.icon_label = self.bake_progress_icon(label=icon, style=icon_style, style_classes=icon_style_classes)
        
        self.add(
            Overlay(
                child = self.progress_bar,
                overlays = [
                    self.icon_label
                ],
            )
        )

    def set_progress_bar_value(self, value: float):
        self.progress_bar.value = value

    def set_icon(self, icon: str):
        self.icon_label.set_label(icon)

    @staticmethod
    def bake_progress_bar(name: str, size: int, **kwargs):
        return CircularProgressBar(
            name = name, min_value = 0, max_value = 100, size = size,line_width=3, **kwargs
        )

    @staticmethod
    def bake_progress_icon(label: str, style: str, **kwargs):
        return Label(label = label, style = style, **kwargs)