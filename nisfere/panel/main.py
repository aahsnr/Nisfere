import setproctitle
from loguru import logger
from fabric import Application
from fabric.utils import get_relative_path, monitor_file, exec_shell_command
from modules.bar.bar import StatusBar
from modules.notification import Notifications
from modules.dock import Dock
from modules.launcher import Launcher
from utils.config import CONFIG_FILE_PATH, CONFIG


def apply_style(app: Application):
    logger.info("[Main] Applying CSS")
    app.set_stylesheet_from_file(get_relative_path("styles/style.css"))


if __name__ == "__main__":
    # Create the status bar
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
