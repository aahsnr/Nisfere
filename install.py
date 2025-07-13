#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class Colors:
    GREEN = "\033[1;32m"
    BLUE = "\033[1;34m"
    RED = "\033[1;31m"
    RESET = "\033[0m"


class NisfereInstaller:
    def __init__(self):
        self.home = Path.home()
        self.script_dir = Path(__file__).parent.resolve()
        self.nisfere_folder = self.home / ".nisfere"
        self.scripts_folder = self.nisfere_folder / "scripts"

        # Package list
        self.packages = [
            "fastfetch",
            "btop",
            "pipewire",
            "playerctl",
            "NetworkManager",
            "brightnessctl",
            "pkgconf",
            "wf-recorder",
            "thunar",
            "thunar-archive-plugin",
            "file-roller",
            "zip",
            "unzip",
            "gvfs",
            "swww",
            "zsh",
            "kitty",
            "libnotify",
            "python3",
            "gtk3",
            "cairo",
            "gtk-layer-shell",
            "gobject-introspection",
            "gobject-introspection-runtime",
            "python3-pip",
            "python3-gobject",
            "python3-psutil",
            "python3-cairo",
            "python3-dbus",
            "python3-loguru",
            "python3-setproctitle",
            "grim",
            "swappy",
            "hyprlock",
            "hypridle",
            "gnome-bluetooth",
            "slurp",
            "ImageMagick",
        ]

        # COPR repositories to enable
        self.copr_repos = [
            # Example repositories - uncomment and modify as needed
            # ("solopasha/hyprland", "Latest Hyprland compositor"),
            # ("alebastr/waybar", "Enhanced Waybar builds"),
            # ("erikreider/SwayNotificationCenter", "Notification center for sway"),
            # ("wezfurlong/wezterm-nightly", "WezTerm terminal emulator"),
        ]

    def print_colored(self, message: str, color: str = Colors.RESET) -> None:
        """Print colored message to stdout"""
        print(f"{color}{message}{Colors.RESET}")

    def print_banner(self) -> None:
        """Print the installation banner"""
        banner_lines = [
            "   N   N I   SSS  FFFFF EEEEE RRRR  EEEEE",
            "  N  N N I  S     F     E     R   R E     ",
            "  N  N N I  SSS   FFFF  EEEE  RRRR  EEEE  ",
            "  N  N N I     S  F     E     R  R  E     ",
            "  N   N  I  SSS   F     EEEEE R   R EEEEE",
        ]

        for line in banner_lines:
            self.print_colored(line, Colors.BLUE)

    def check_fedora(self) -> None:
        """Check if running on Fedora Linux"""
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read()
                if "fedora" not in content.lower():
                    self.print_colored(
                        "This script is designed to run on Fedora Linux. Exiting.",
                        Colors.RED,
                    )
                    sys.exit(1)
        except FileNotFoundError:
            self.print_colored(
                "Cannot determine OS. This script is designed for Fedora Linux.",
                Colors.RED,
            )
            sys.exit(1)

    def run_command(
        self, command: List[str], check: bool = True, capture_output: bool = False
    ) -> subprocess.CompletedProcess:
        """Run a system command with error handling"""
        try:
            result = subprocess.run(
                command, check=check, capture_output=capture_output, text=True
            )
            return result
        except subprocess.CalledProcessError as e:
            self.print_colored(f"Command failed: {' '.join(command)}", Colors.RED)
            if check:
                raise
            return e

    def command_exists(self, command: str) -> bool:
        """Check if a command exists in the system PATH"""
        return shutil.which(command) is not None

    def install_packages(self) -> None:
        """Install required packages using DNF"""
        self.print_colored("Installing required packages...")

        # Update system first
        self.print_colored("Updating system packages...")
        self.run_command(["sudo", "dnf", "update", "-y"])

        # Install dnf-plugins-core first for COPR support
        self.print_colored("Installing dnf-plugins-core for COPR support...")
        self.run_command(["sudo", "dnf", "install", "-y", "dnf-plugins-core"])

        # Install all packages at once
        self.print_colored("Installing application packages...")
        install_cmd = ["sudo", "dnf", "install", "-y"] + self.packages
        self.run_command(install_cmd)

        self.print_colored("✔ Packages installed.", Colors.GREEN)

    def enable_copr_repositories(self) -> None:
        """Enable COPR repositories"""
        if not self.copr_repos:
            self.print_colored("No COPR repositories configured to enable.")
            return

        self.print_colored("Enabling COPR repositories...")

        for repo_info in self.copr_repos:
            if isinstance(repo_info, tuple):
                repo_name, description = repo_info
                self.print_colored(
                    f"Enabling COPR repository: {repo_name} ({description})"
                )
            else:
                repo_name = repo_info
                self.print_colored(f"Enabling COPR repository: {repo_name}")

            result = self.run_command(
                ["sudo", "dnf", "copr", "enable", "-y", repo_name], check=False
            )

            if result.returncode == 0:
                self.print_colored(f"✔ Successfully enabled: {repo_name}", Colors.GREEN)
            else:
                self.print_colored(f"✗ Failed to enable: {repo_name}", Colors.RED)

        self.print_colored("✔ COPR repositories processed.", Colors.GREEN)

    def copy_files(self) -> None:
        """Copy configuration files to appropriate locations"""
        self.print_colored("Copying configuration files...")

        # Create necessary directories
        directories = [
            self.home / ".fonts",
            self.home / ".themes",
            self.home / ".icons",
            self.home / ".config",
            self.home / ".cache" / "nisfere",
            self.home / "Videos" / "records",
            self.home / "Pictures" / "screenshots",
            self.home / ".config" / "nisfere" / "themes",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        # Copy files if source directories exist
        file_mappings = [
            (self.script_dir / "fonts", self.home / ".fonts"),
            (self.script_dir / "gtk-themes", self.home / ".themes"),
            (self.script_dir / "dotfiles", self.home / ".config"),
        ]

        for source, destination in file_mappings:
            if source.exists():
                shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                self.print_colored(
                    f"Warning: Source directory {source} not found", Colors.RED
                )

        # Create notifications file
        notifications_file = self.home / ".cache" / "nisfere" / "notifications.json"
        notifications_file.write_text("[]")

        # Copy panel config if it exists
        panel_config_source = self.script_dir / "nisfere" / "panel" / "config.json"
        panel_config_dest = self.home / ".config" / "nisfere" / "panel-config.json"

        if panel_config_source.exists():
            shutil.copy2(panel_config_source, panel_config_dest)
        else:
            self.print_colored(
                f"Warning: Panel config {panel_config_source} not found", Colors.RED
            )

        self.print_colored("✔ Configuration files copied.", Colors.GREEN)

    def setup_icons_and_cursor(self) -> None:
        """Setup icons and cursor theme"""
        self.print_colored("Setting up icons and cursor...")

        icons_dest = self.home / ".icons"
        cursor_repo = icons_dest / "Breeze-Adapta-Cursor"

        # Clone cursor repository if it doesn't exist
        if not cursor_repo.exists():
            self.run_command(
                [
                    "git",
                    "clone",
                    "https://github.com/mustafaozhan/Breeze-Adapta-Cursor",
                    str(cursor_repo),
                ]
            )

        # Set cursor for Hyprland if available
        if self.command_exists("hyprctl"):
            self.run_command(
                ["hyprctl", "setcursor", "Breeze-Adapta-Cursor", "17"], check=False
            )
        else:
            self.print_colored(
                "Warning: hyprctl not found, skipping cursor setup for Hyprland"
            )

        # Set cursor for GNOME if available
        if self.command_exists("gsettings"):
            self.run_command(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.interface",
                    "cursor-theme",
                    "Breeze-Adapta-Cursor",
                ],
                check=False,
            )
            self.run_command(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.interface",
                    "cursor-size",
                    "17",
                ],
                check=False,
            )
        else:
            self.print_colored(
                "Warning: gsettings not found, skipping GNOME cursor setup"
            )

        self.print_colored("✔ Icons and cursor setup complete.", Colors.GREEN)

    def setup_nisfere(self) -> None:
        """Setup Nisfere application"""
        self.print_colored("Setting up Nisfere...")

        # Create nisfere directory
        self.nisfere_folder.mkdir(parents=True, exist_ok=True)

        # Copy nisfere files if they exist
        nisfere_source = self.script_dir / "nisfere"
        if nisfere_source.exists():
            shutil.copytree(nisfere_source, self.nisfere_folder, dirs_exist_ok=True)
        else:
            self.print_colored(
                f"Warning: Nisfere source directory {nisfere_source} not found",
                Colors.RED,
            )

        self.print_colored("✔ Nisfere setup complete.", Colors.GREEN)

    def setup_scripts(self) -> None:
        """Setup and execute initialization scripts"""
        self.print_colored("Setting up scripts...")

        # Scripts to make executable and run
        scripts_to_setup = [
            ("change-theme.sh", ["dracula"]),
            ("init-swww.sh", []),
            ("init-panel.sh", []),
        ]

        for script_name, args in scripts_to_setup:
            script_path = self.scripts_folder / script_name

            if script_path.exists():
                # Make executable
                script_path.chmod(0o755)

                # Execute script
                cmd = [str(script_path)] + args
                result = self.run_command(cmd, check=False, capture_output=True)

                if result.returncode != 0:
                    self.print_colored(
                        f"Warning: {script_name} execution failed", Colors.RED
                    )
            else:
                self.print_colored(
                    f"Warning: {script_name} not found, skipping", Colors.RED
                )

        self.print_colored("✔ Scripts executed.", Colors.GREEN)

    def run_installation(self) -> None:
        """Run the complete installation process"""
        try:
            self.print_banner()
            self.check_fedora()

            # Run installation steps
            self.install_packages()
            self.enable_copr_repositories()
            self.copy_files()
            self.setup_icons_and_cursor()
            self.setup_nisfere()
            self.setup_scripts()

            self.print_colored("✔ Installation complete!", Colors.GREEN)

        except KeyboardInterrupt:
            self.print_colored("\n✗ Installation interrupted by user.", Colors.RED)
            sys.exit(1)
        except Exception as e:
            self.print_colored(f"✗ Installation failed: {str(e)}", Colors.RED)
            sys.exit(1)


def main():
    """Main entry point"""
    installer = NisfereInstaller()
    installer.run_installation()


if __name__ == "__main__":
    main()
