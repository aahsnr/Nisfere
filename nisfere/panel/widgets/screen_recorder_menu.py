from gi.repository import GLib
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from services import screen_recorder_service
from shared import Button
from utils.icons import screen_recorder_icons
from fabric.core import Signal


class ScreenRecorderMenu(Box):
    @Signal
    def closed(self) -> None: ...

    def __init__(self, **kwargs):
        super().__init__(
            name="screen-recorder",
            style_classes="menu",
            **kwargs
        )

        self.screen_recorder = screen_recorder_service.build()\
            .connect('notify::is-recording', lambda *args: self.on_recording_changed())\
            .unwrap()

        self.header = Label(name="screen-recorder-menu-header",
                            label="Screen Recorder", h_align="start")

        self.start_button = Button(
            label=screen_recorder_icons['start_recording'],
            tooltip_text="Start Recording",
            on_clicked=lambda *args: self.start_recording(fullscreen=True),
            h_expand=True
        )

        self.start_area_button = Button(
            label=screen_recorder_icons['start_recording_area'],
            tooltip_text="Start Recording (select area)",
            on_clicked=lambda *args: self.start_recording(fullscreen=False),
            h_expand=True
        )

        self.stop_button = Button(
            label=screen_recorder_icons['stop_recording'],
            tooltip_text="Stop recording",
            on_clicked=lambda *args: self.stop_recording(),
            h_expand=True
        )

        self.footer = Label(name="screen-recorder-menu-footer",
                            label="Ready", h_align="start")

        self.buttons_box = Box(
            name="screen-recorder-menu-body",
            spacing=8,
            orientation="h",
            children=[self.start_button,
                      self.start_area_button, self.stop_button]
        )

        self.add(
            Box(
                style_classes="menu-inner",
                orientation="v",
                spacing=14,
                children=[
                    self.header,
                    self.buttons_box,
                    self.footer,
                ]
            )
        )

        self.stop_button.set_sensitive(False)

    def start_recording(self, fullscreen: bool):
        if self.screen_recorder.is_recording:
            return

        self.screen_recorder.start_recording(fullscreen=fullscreen)

    def stop_recording(self):
        if not self.screen_recorder.is_recording:
            return
        self.screen_recorder.stop_recording()

    def on_recording_changed(self):
        if self.screen_recorder.is_recording:
            self.start_area_button.set_sensitive(False)
            self.start_button.set_sensitive(False)
            self.stop_button.set_sensitive(True)
            self.footer.set_label(f"Recording ...")
            self.emit('closed')
        else:
            self.footer.set_label(f"Ready")
            self.start_button.set_sensitive(True)
            self.start_area_button.set_sensitive(True)
            self.stop_button.set_sensitive(False)
