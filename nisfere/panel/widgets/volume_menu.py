from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.scale import Scale

from shared import Button
from utils.helpers import get_microphone_icon, get_speaker_icon
from services import audio_service


class VolumeMenu(Box):
    def __init__(self, **kwargs):
        super().__init__(name="volume-menu", style_classes="menu", **kwargs)
        
        # Header
        self.header = Label(name="volume-menu-header", label="Volume", h_align="start")

        # Containers for conditional UI
        self.dynamic_container = Box(
            name="volume-menu-body",
            style_classes="menu-inner",
            spacing=14,
            orientation="v",
            children=[self.header]
        )

        self.add(self.dynamic_container)

        # Pre-define but don't add these yet
        self.speaker_box = None
        self.microphone_box = None

        # Connect to audio events
        self.audio = audio_service.build()\
            .connect("speaker_changed", lambda *args:  self.on_speaker_changed())\
            .connect("microphone_changed", lambda *args:  self.on_microphone_changed())\
            .unwrap()


    def build_speaker_box(self):
        label = Label(name="speaker-box-label")
        mute_btn = Button(name="speaker-mute-btn", on_clicked=lambda *args: self.toggle_speaker_mute(), h_expand=False)
        scale = Scale(name="speaker-scale", style_classes="scale", min_value=0, max_value=100, value=50, h_expand=True)
        vol_label = Label(name="speaker-volume-label", label="", h_align="end")

        scale.connect("value-changed", self.on_speaker_scale_changed)

        mgmt_box = Box(name="speaker-mgmt-box", spacing=12, size=25, children=[mute_btn, scale, vol_label])
        box = Box(name="speaker-box", orientation="v", children=[label, mgmt_box])

        self.speaker_label = label
        self.speaker_mute_btn = mute_btn
        self.speaker_scale = scale
        self.speaker_volume_label = vol_label

        return box

    def build_microphone_box(self):
        label = Label(name="microphone-box-label")
        mute_btn = Button(name="microphone-mute-btn", on_clicked=lambda *args: self.toggle_microphone_mute(), h_expand=False)
        scale = Scale(name="microphone-scale", style_classes="scale", min_value=0, max_value=100, value=50, h_expand=True)
        vol_label = Label(name="microphone-volume-label", label="", h_align="end")

        scale.connect("value-changed", self.on_microphone_scale_changed)

        mgmt_box = Box(name="microphone-mgmt-box", spacing=12, size=25, children=[mute_btn, scale, vol_label])
        box = Box(name="microphone-box", orientation="v", children=[label, mgmt_box])

        self.microphone_label = label
        self.microphone_mute_btn = mute_btn
        self.microphone_scale = scale
        self.microphone_volume_label = vol_label

        return box


    def on_speaker_changed(self):
        if not self.audio.speaker:
            return

        if not self.speaker_box:
            self.speaker_box = self.build_speaker_box()
            self.dynamic_container.add(self.speaker_box)

        self.speaker_label.set_label(self.audio.speaker.name[:20])

        self.speaker_scale.value = self.audio.speaker.volume

        self.speaker_volume_label.set_label(
            f"{round(self.audio.speaker.volume)}%")

        self.speaker_mute_btn.set_label(
            get_speaker_icon(
                volume=self.audio.speaker.volume,
                muted=self.audio.speaker.get_muted()
            )
        )

    def toggle_speaker_mute(self):
        if not self.audio.speaker:
            return

        self.audio.speaker.set_muted(not self.audio.speaker.get_muted())

    def on_speaker_scale_changed(self, scale):
        value = scale.get_value()
        self.audio.speaker.volume = value

    def on_microphone_changed(self):
        if not self.audio.microphone:
            return

        if not self.microphone_box:
            self.microphone_box = self.build_microphone_box()
            self.dynamic_container.add(self.microphone_box)

        self.microphone_label.set_label(self.audio.microphone.name[:20])

        self.microphone_scale.value = self.audio.microphone.volume

        self.microphone_volume_label.set_label(
            f"{round(self.audio.microphone.volume)}%")

        self.microphone_mute_btn.set_label(get_microphone_icon(
            muted=self.audio.microphone.get_muted()))

    def toggle_microphone_mute(self):
        if not self.audio.microphone:
            return
        self.audio.microphone.set_muted(not self.audio.microphone.get_muted())

    def on_microphone_scale_changed(self, scale):
        value = scale.get_value()
        self.audio.microphone.volume = value
