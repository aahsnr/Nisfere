from fabric.widgets.button import Button
from fabric.utils import FormattedString

from shared import Button
from services import screen_recorder_service
from utils.icons import stop_recording as stop_recording_icon


class Recording(Button):
    def __init__(self, **kwargs):
        super().__init__(
            name="recording",
            **kwargs
        )

        self.set_label(stop_recording_icon)

        self.set_tooltip_text("Stop recording")

        self.screen_recorder = screen_recorder_service.build()\
            .connect('notify::is-recording', lambda *args: self.on_recording_changed())\
            .unwrap()

        self.connect(
            "clicked", lambda *args: self.screen_recorder.stop_recording())

        self.set_visible(False)

    def on_recording_changed(self):
        if self.screen_recorder.is_recording:
            self.set_visible(True)
        else:
            self.set_visible(False)
