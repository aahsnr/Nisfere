from fabric.widgets.box import Box
from fabric.widgets.label import Label

from fabric.utils.helpers import exec_shell_command
from fabric.core import Signal

from shared import Button
from utils.config import CONFIG
from utils.helpers import get_current_uptime

from fabricators.uptime_fabricator import uptime_fabricator

power_buttons = CONFIG.get('power-buttons')

class PowerMenu(Box):
    @Signal
    def closed(self) -> None: ...

    def __init__(self, **kwargs):
        super().__init__(name= "power-menu", style_classes= "menu", **kwargs)

        uptime_fabricator.build()\
            .connect("changed", lambda _, v: self.on_uptime_value_changed(v))\
        .unwrap()

        self.header = Label(name= "power-menu-header", label= "Power", h_align= "start")

        self.inner= Box(name= "power-menu-body", spacing= 6, orientation= "h", size= 25)

        self.footer= Label(name= "power-menu-footer", label= f"{get_current_uptime()}", h_align= "start")

        for index, power_button in enumerate(power_buttons):

            button= Button(label=power_button.get('icon'), tooltip_text= power_button.get('label'), h_expand= True)

            button.connect("clicked", lambda _, command=power_button.get('command'): self.exec_button_command(command))

            self.inner.add(button)

        self.add(
            Box(
                style_classes="menu-inner",
                spacing= 14,
                orientation= "v",
                children= [
                    self.header,
                    self.inner,
                    self.footer
                ]
            )
        )
            
    def exec_button_command(self, command):
        exec_shell_command(command)
        self.emit("closed")

    def on_uptime_value_changed(self, uptime_value):
        self.footer.set_label(uptime_value)