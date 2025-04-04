import setproctitle
import re
from loguru import logger
from fabric import Application
from fabric.utils import get_relative_path, monitor_file, exec_shell_command
from modules.bar.bar import StatusBar
from modules.notification import Notifications
from modules.dock import Dock
from modules.launcher import Launcher
from utils.config import CONFIG_FILE_PATH, CONFIG, fabric_config


def apply_style(app: Application):
    logger.info("[Main] Applying CSS")
    app.set_stylesheet_from_file(get_relative_path("styles/style.css"))

def update_css_constants():
    css_constants = fabric_config['style']
    with open(get_relative_path("styles/constants.css"), "r") as file:
        content = file.read()

    # Replace using regex
    def replacer(match):
        name = match.group(1)
        if name in css_constants:
            return f"@define {name} {css_constants[name]};"
        return match.group(0)

    updated_content = re.sub(r"@define\s+([\w-]+)\s+[^;]+;", replacer, content)

    # Write back (or to a new file)
    with open(get_relative_path("styles/constants.css"), "w") as file:
        file.write(updated_content)

if __name__ == "__main__":
    # Create the status bar

    update_css_constants()

    launcher = Launcher()

    bar = StatusBar(launcher=launcher)

    notifications = Notifications()

    dock = Dock()

    windows = [bar, notifications, dock]

    # Initialize the application with the status bar
    app = Application("nisfere-panel", windows=windows)

    setproctitle.setproctitle("nisfere-panel")

    css_file_monitor = monitor_file(get_relative_path("./styles"))
    css_file_monitor.connect("changed", lambda *_: apply_style(app))

    config_file_monitor = monitor_file(CONFIG_FILE_PATH)
    config_file_monitor.connect(
        "changed",
        lambda *_: exec_shell_command(
            f"{CONFIG["nisfere-scripts-path"]}/init-panel.sh"
        ),
    )

    apply_style(app)
    # Run the application
    app.run()
