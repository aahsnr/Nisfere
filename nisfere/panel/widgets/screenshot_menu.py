from fabric.widgets.box import Box
from fabric.widgets.label import Label
from fabric.core import Signal

from utils.config import CONFIG
from shared import Button
from services import screenshot_service

from gi.repository import GLib

screenshot_buttons = CONFIG['screenshot-menu-buttons']

class ScreenshotMenu(Box):
    @Signal
    def closed(self) -> None: ...

    def __init__(self, **kwargs):
        super().__init__(
            name="screenshot-menu",
            style_classes="menu",
            **kwargs
        )
        self.screenshot = screenshot_service.build()\
            .connect('screenshot-saved', lambda *args: self.on_screenshot_saved())\
        .unwrap()      
        
        self.header= Label(name= "screenshot-menu-header", label= "Screenshot", h_align= "start", h_expand= True)

        self.inner = Box(name= "screenshot-menu-body", spacing=8, orientation="h", size=25, v_align= "center")

        self.footer = Label(name="screenshot-menu-footer", label="Select action", h_align= "start")

        for button in screenshot_buttons:
            btn = Button(label= button['icon'], tooltip_text= button['label'], h_expand= True)
            action_name = button['name']  # Get the function name dynamically

            if hasattr(self, action_name):  # Check if function exists
                btn.connect("clicked", getattr(self, action_name))  # Bind to the correct function

            self.inner.add(btn)

        self.children = Box(
            style_classes="menu-inner",
            spacing=14,
            orientation="v",
            children= [
                self.header,
                self.inner,
                self.footer,
            ]
        )

    def start_countdown_and_capture(self, remaining:int):
        if remaining > 0:
            self.footer.set_label(f"Screenshot at: ({remaining}s)")
            GLib.timeout_add_seconds(1, lambda: self.start_countdown_and_capture(remaining - 1) or False)
        else:
            self.footer.set_label("Select action")
            self.screenshot.capture_desktop()  # Take screenshot when countdown reaches 0

    # Specific functions for each action
    def capture_desktop(self, *args):
        self.screenshot.capture_desktop()

    def capture_window(self, *args):
        self.screenshot.capture_window()
    
    def capture_area(self, *args):
        self.screenshot.capture_area()
    
    def capture_in_five(self, *args):
        self.start_countdown_and_capture(remaining=5)

    def capture_in_ten(self, *args):
        self.start_countdown_and_capture(remaining=10)
    
    def on_screenshot_saved(self):
        self.emit('closed')