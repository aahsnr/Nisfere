from fabric.widgets.box import Box
from fabric.widgets.label import Label

from shared.button import ButtonWidget as Button

class ButtonWithIcon(Button):
    def __init__(
        self,
        icon: str = "",
        text: str = "",
        *args,
        **kwargs
    ):
        super().__init__(
            **kwargs
        )
        
        self.icon_label = Label(
            label= icon,
            style_classes= "icon-button-icon",
            h_align="start"
        )
        self.text_label = Label(label= text,
            style_classes= "icon-button-label",
            v_align="center",
            h_align="center",
        )

        self.add(Box(
            orientation="h",
            spacing=4,
            style_classes="icon-button",
            children=[
                self.icon_label,
                self.text_label
            ],
        ))

    def set_icon(self, icon: str):
        self.icon_label.set_label(icon)

    def set_text(self, icon_label: str):
        self.text_label.set_label(icon_label)

    def get_text(self):
        return self.text_label.get_label()
    
    def get_icon(self):
        return self.icon_label.get_label()