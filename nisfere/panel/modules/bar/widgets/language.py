from shared import ButtonWithIcon
from services import hyprland_language_service
from utils.icons import keyboard_layout as kb_icon

class Language(ButtonWithIcon):
    def __init__(self,**kwargs):
        super().__init__(
            name="language",
            style_classes="bar-widget",
            **kwargs
        )

        self.set_icon(kb_icon)

        self.hyprland_language = hyprland_language_service.build()\
            .connect("language-changed", lambda *args: self.set_text(self.hyprland_language.language))\
        .unwrap()

        self.connect("clicked", lambda *args: self.hyprland_language.change_language())

        self.set_text(self.hyprland_language.language)
