from fabric.widgets.box import Box
from fabric.utils.helpers import exec_shell_command
from shared import Button

from utils.config import CONFIG

power_buttons = CONFIG.get('power-buttons')

class PowerButtons(Box):
    def __init__(self, **kwargs):
        super().__init__(
            spacing = 8,
            orientation = "v",
            style_classes="side-panel-widget",
            name="power-buttons",
            **kwargs
        )

        for index, power_button in enumerate(power_buttons):
            
            if power_button.get('name') != "lock":

                button = Button(name= f"power-button-{index}", label= power_button.get('icon'), tooltip_text= power_button.get('label'), v_expand= True)

                button.connect("clicked", lambda _, command=power_button.get('command'): self.exec_button_command(command))

                self.add(button)

    def exec_button_command(self, command):
        exec_shell_command(command) 