from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.widgets.widget import Widget 

from shared import Button, ProgressBarWithIcon, PopOverWindow
from utils.helpers import get_speaker_icon 
from utils.icons import volume_icons
from services import audio_service
from widgets import VolumeMenu

class Volume(Button):
    def __init__(self, bar: Widget, **kwargs):
        super().__init__(name="volume", style_classes="bar-widget", **kwargs)

        self.add_events("scroll")

        self.audio= audio_service.build()\
          .connect("speaker-changed", lambda *args: self.on_speaker_changed())\
        .unwrap()
        
        self.popup = PopOverWindow(
            parent= bar,
            pointing_to= self,
            child= VolumeMenu()
        )

        self.progress_bar= ProgressBarWithIcon(
            progress_bar_name="volume-progress-bar",
            progress_bar_size=26,
            icon= volume_icons['default'],
            icon_style="font-size: 13px",
            icon_style_classes="volume-progress-icon"
        )
        
        self.label= Label()
        
        self.connect("clicked", lambda *args: self.popup.set_visible(not self.popup.get_visible()))
        
        self.connect("scroll-event", self.on_scroll)

        self.add(
            Box(
                name= "volume",
                spacing= 8,
                orientation= "h",
                children= [
                    self.progress_bar,
                    self.label
                ]
            )
        )

        self.on_speaker_changed()

    def on_scroll(self, _, event):
        match event.direction:
            case 0:
                self.audio.speaker.volume += 8
            case 1:
                self.audio.speaker.volume -= 8

    def on_speaker_changed(self):
        if not self.audio.speaker:
            return
            
        self.progress_bar.set_progress_bar_value(self.audio.speaker.volume)
        self.label.set_label(f"{round(self.audio.speaker.volume)}%")
        self.progress_bar.set_icon(get_speaker_icon(volume= self.audio.speaker.volume, muted= self.audio.speaker.get_muted()))

