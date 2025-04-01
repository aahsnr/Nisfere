import os
import time

from fabric.widgets.box import Box
from fabric.widgets.label import Label

class UserHeader(Box):
    def __init__(self, **kwargs):
        super().__init__(
            spacing= 8,
            orientation= "v",
            style_classes="side-panel-widget",
            h_expand= True,
            **kwargs
        )

        self.add(
            Label(
                name= "user-header-label", label= f"Good {'Morning' if time.localtime().tm_hour < 12 else 'Afternoon'}, {os.getlogin().title()}!"
            )
        )
