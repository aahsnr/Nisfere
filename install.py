#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# Colors for output
class Colors:
    GREEN = "\033[1;32m"
    BLUE = "\033[1;34m"
    RESET = "\033[0m"


def print_banner():
    """Print the Nisfere banner"""
    print(f"{Colors.BLUE}   N   N I   SSS  FFFFF EEEEE RRRR  EEEEE{Colors.RESET}")
    print(f"{Colors.BLUE}  N  N N I  S     F     E     R   R E     {Colors.RESET}")
    print(f"{Colors.BLUE}  N  N N I  SSS   FFFF  EEEE  RRRR  EEEE  {Colors.RESET}")
    print(f"{Colors.BLUE}  N  N N I     S  F     E     R  R  E     {Colors.RESET}")
    print(f"{Colors.BLUE}  N   N  I  SSS   F     EEEEE R   R EEEEE{Colors.RESET}")


def abort_if_not_arch():
    """Check if running on Arch Linux"""
    try:
        with open("/etc/os-release", "r") as f:
            if "arch" not in f.read().lower():
                print("This script is designed to run on Arch Linux. Exiting.")
                sys.exit(1)
    except FileNotFoundError:
        print("Cannot determine OS. This script is designed for Arch Linux. Exiting.")
        sys.exit(1)


def abort_if_root():
    """Check if running as root"""
    if os.geteuid() == 0:
        print("Please do not run this script as root. Exiting.")
        sys.exit(1)


def check_command(command):
    """Check if a command exists"""
    return shutil.which(command) is not None


def run_command(cmd, shell=False, check=True, capture_output=False):
    """Run a command with error handling"""
    try:
        if shell:
            result = subprocess.run(
                cmd, shell=True, check=check, capture_output=capture_output, text=True
            )
        else:
            result = subprocess.run(
                cmd, check=check, capture_output=capture_output, text=True
            )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        if not check:
            return e
        sys.exit(1)


def install_yay(nisfere_installation_folder):
    """Install yay AUR helper"""
    print("Installing yay...")
    yay_dir = Path(nisfere_installation_folder) / "yay"

    # Clone yay repository
    run_command(["git", "clone", "https://aur.archlinux.org/yay.git", str(yay_dir)])

    # Change to yay directory and build
    original_cwd = os.getcwd()
    os.chdir(yay_dir)

    try:
        run_command(["makepkg", "-si", "--noconfirm"])
    finally:
        os.chdir(original_cwd)

    print(f"{Colors.GREEN}✔ Yay installed successfully.{Colors.RESET}")


def install_packages():
    """Install required packages"""
    print("Installing required packages...")

    # Pacman packages
    pacman_packages = [
        "fastfetch",
        "bpytop",
        "pipewire",
        "playerctl",
        "networkmanager",
        "brightnessctl",
        "pkgconf",
        "wf-recorder",
        "thunar",
        "thunar-archive-plugin",
        "xarchiver",
        "zip",
        "unzip",
        "gvfs",
        "swww",
        "zsh",
        "alacritty",
        "libnotify",
        "python",
        "gtk3",
        "cairo",
        "gtk-layer-shell",
        "libgirepository",
        "gobject-introspection",
        "gobject-introspection-runtime",
        "python-pip",
        "python-gobject",
        "python-psutil",
        "python-cairo",
        "python-dbus",
        "python-pydbus",
        "python-loguru",
        "python-setproctitle",
        "grim",
        "swappy",
        "code",
    ]

    pacman_cmd = ["sudo", "pacman", "-Syu", "--noconfirm", "--needed"] + pacman_packages
    run_command(pacman_cmd)

    # Yay packages
    yay_packages = [
        "python-fabric",
        "swaylock-effects-git",
        "swayidle",
        "gnome-bluetooth-3.0",
        "fabric-cli-git",
        "slurp",
        "imagemagick",
    ]

    yay_cmd = ["yay", "-S", "--noconfirm", "--needed"] + yay_packages
    run_command(yay_cmd)

    print(f"{Colors.GREEN}✔ Packages installed.{Colors.RESET}")


def install_vscode_extension(script_dir):
    """Configure VSCode with Nisfere theme"""
    print("Configuring VSCode...")

    # Define paths
    vscode_extensions_dir = Path.home() / ".vscode-oss" / "extensions"
    vscode_settings_file = (
        Path.home() / ".config" / "Code - OSS" / "User" / "settings.json"
    )

    # Ensure extensions directory exists
    vscode_extensions_dir.mkdir(parents=True, exist_ok=True)

    # Copy theme extension
    vscode_source = Path(script_dir) / "vscode"
    if vscode_source.exists():
        for item in vscode_source.iterdir():
            if item.is_dir():
                shutil.copytree(
                    item, vscode_extensions_dir / item.name, dirs_exist_ok=True
                )
            else:
                shutil.copy2(item, vscode_extensions_dir)

    # Ensure settings.json exists
    vscode_settings_file.parent.mkdir(parents=True, exist_ok=True)
    if not vscode_settings_file.exists():
        with open(vscode_settings_file, "w") as f:
            json.dump({}, f)

    # Update settings.json with theme
    try:
        with open(vscode_settings_file, "r") as f:
            settings = json.load(f)

        settings["workbench.colorTheme"] = "Nisfere"

        with open(vscode_settings_file, "w") as f:
            json.dump(settings, f, indent=2)
    except (json.JSONDecodeError, FileNotFoundError):
        # If file is corrupted or missing, create new one
        with open(vscode_settings_file, "w") as f:
            json.dump({"workbench.colorTheme": "Nisfere"}, f, indent=2)

    print(f"{Colors.GREEN}✔ VSCode configured with theme 'Nisfere'.{Colors.RESET}")


def install_zsh(script_dir, nisfere_installation_folder):
    """Configure Zsh with plugins"""
    print("Configuring Zsh...")

    # Copy .zshrc
    zshrc_source = Path(script_dir) / "zsh" / ".zshrc"
    zshrc_dest = Path.home() / ".zshrc"
    if zshrc_source.exists():
        shutil.copy2(zshrc_source, zshrc_dest)

    # Setup plugins
    zsh_folder = Path(nisfere_installation_folder) / "zsh"
    plugins_folder = zsh_folder / "plugins"
    plugins_folder.mkdir(parents=True, exist_ok=True)

    plugins = [
        "zsh-syntax-highlighting",
        "zsh-autosuggestions",
        "zsh-history-substring-search",
    ]

    for plugin in plugins:
        plugin_dir = plugins_folder / plugin
        if not plugin_dir.exists():
            repo_url = f"https://github.com/zsh-users/{plugin}.git"
            run_command(["git", "clone", repo_url, str(plugin_dir)])

    # Ensure Zsh history file exists
    history_file = Path.home() / ".zsh_history"
    if not history_file.exists():
        history_file.touch()
        os.chmod(history_file, 0o600)

    # Change default shell to zsh
    username = os.getenv("USER")
    run_command(["sudo", "chsh", "-s", "/bin/zsh", username])

    print(f"{Colors.GREEN}✔ Zsh configured.{Colors.RESET}")


def copy_files(script_dir, nisfere_installation_folder):
    """Copy configuration files"""
    print("Copying configuration files...")

    home = Path.home()

    # Create directories
    directories = [
        home / ".fonts",
        home / ".themes",
        home / ".icons",
        home / ".config",
        home / ".cache" / "nisfere",
        home / ".vscode-oss" / "extensions",
        home / "Videos" / "records",
        home / "Pictures" / "screenshots",
        home / ".config" / "nisfere" / "themes",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    # Copy files
    copy_mappings = [
        ("fonts", home / ".fonts"),
        ("gtk-themes", home / ".themes"),
        ("dotfiles", home / ".config"),
    ]

    script_path = Path(script_dir)
    for source_dir, dest_dir in copy_mappings:
        source_path = script_path / source_dir
        if source_path.exists():
            for item in source_path.iterdir():
                if item.is_dir():
                    shutil.copytree(item, dest_dir / item.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest_dir)

    # Create notifications file
    notifications_file = home / ".cache" / "nisfere" / "notifications.json"
    with open(notifications_file, "w") as f:
        json.dump([], f)

    # Copy panel config
    panel_config_source = script_path / "nisfere" / "panel" / "config.json"
    panel_config_dest = home / ".config" / "nisfere" / "panel-config.json"
    if panel_config_source.exists():
        shutil.copy2(panel_config_source, panel_config_dest)

    print(f"{Colors.GREEN}✔ Configuration files copied.{Colors.RESET}")


def setup_icons_and_cursor():
    """Setup icons and cursor themes"""
    print("Setting up icons and cursor...")

    icons_dest = Path.home() / ".icons"
    icons_dest.mkdir(exist_ok=True)

    # Icon repositories to clone
    icon_repos = [
        ("dracula-icons", "https://github.com/m4thewz/dracula-icons"),
        ("Zafiro-Nord-Dark", "https://github.com/zayronxio/Zafiro-Nord-Dark.git"),
        (
            "Breeze-Adapta-Cursor",
            "https://github.com/mustafaozhan/Breeze-Adapta-Cursor",
        ),
    ]

    for icon_name, repo_url in icon_repos:
        icon_path = icons_dest / icon_name
        if not icon_path.exists():
            run_command(["git", "clone", repo_url, str(icon_path)])

    # Special handling for Catppuccin icons
    catppuccin_path = icons_dest / "Catppuccin-Mocha"
    if not catppuccin_path.exists():
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_url = "https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme.git"
            run_command(["git", "clone", repo_url, temp_dir])
            source_path = Path(temp_dir) / "icons" / "Catppuccin-Mocha"
            if source_path.exists():
                shutil.copytree(source_path, catppuccin_path)

    # Special handling for Solarized icons
    solarized_path = icons_dest / "Solarized-Deluxe-Iconpack"
    if not solarized_path.exists():
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_url = "https://github.com/rtlewis88/rtl88-Themes.git"
            run_command(
                [
                    "git",
                    "clone",
                    "--branch",
                    "Solarized-Deluxe-Icons-and-Animated-Cursors",
                    "--single-branch",
                    repo_url,
                    temp_dir,
                ]
            )
            source_path = Path(temp_dir) / "Solarized-Deluxe-Iconpack"
            if source_path.exists():
                shutil.copytree(source_path, solarized_path)

    # Special handling for Gruvbox icons
    gruvbox_path = icons_dest / "Gruvbox-Plus-Dark"
    if not gruvbox_path.exists():
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_url = "https://github.com/SylEleuth/gruvbox-plus-icon-pack.git"
            run_command(["git", "clone", repo_url, temp_dir])
            source_path = Path(temp_dir) / "Gruvbox-Plus-Dark"
            if source_path.exists():
                shutil.copytree(source_path, gruvbox_path)

    # Special handling for Grade icons
    grade_path = icons_dest / "Grade-circle-dark"
    if not grade_path.exists():
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_url = "https://github.com/mayur-m-zambare/Grade-icon-theme.git"
            run_command(["git", "clone", repo_url, temp_dir])
            source_path = Path(temp_dir) / "Grade-circle-dark"
            if source_path.exists():
                shutil.copytree(source_path, grade_path)

    # Set cursor theme
    run_command(["hyprctl", "setcursor", "Breeze-Adapta-Cursor", "17"], check=False)
    run_command(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.interface",
            "cursor-theme",
            "Breeze-Adapta-Cursor",
        ],
        check=False,
    )
    run_command(
        ["gsettings", "set", "org.gnome.desktop.interface", "cursor-size", "17"],
        check=False,
    )

    print(f"{Colors.GREEN}✔ Icons and cursor setup complete.{Colors.RESET}")


def setup_nisfere(script_dir, nisfere_installation_folder):
    """Setup Nisfere files"""
    print("Setting up Nisfere...")

    nisfere_source = Path(script_dir) / "nisfere"
    nisfere_dest = Path(nisfere_installation_folder)

    if nisfere_source.exists():
        for item in nisfere_source.iterdir():
            if item.is_dir():
                shutil.copytree(item, nisfere_dest / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, nisfere_dest)

    print(f"{Colors.GREEN}✔ Nisfere setup complete.{Colors.RESET}")


def setup_scripts(scripts_folder):
    """Setup and execute scripts"""
    print("Setting up scripts...")

    scripts_path = Path(scripts_folder)

    # Make scripts executable
    scripts_to_chmod = ["change-theme.sh", "init-swww.sh", "init-panel.sh"]

    for script in scripts_to_chmod:
        script_path = scripts_path / script
        if script_path.exists():
            os.chmod(script_path, 0o755)

    # Execute scripts
    run_command([str(scripts_path / "change-theme.sh"), "dracula"], check=False)
    run_command([str(scripts_path / "init-panel.sh")], capture_output=True, check=False)
    run_command([str(scripts_path / "init-swww.sh")], capture_output=True, check=False)

    print(f"{Colors.GREEN}✔ Scripts executed.{Colors.RESET}")


def main():
    """Main execution function"""
    print_banner()
    abort_if_not_arch()
    abort_if_root()

    # Setup paths
    nisfere_installation_folder = Path.home() / ".nisfere"
    script_dir = Path(__file__).parent.resolve()
    scripts_folder = nisfere_installation_folder / "scripts"

    # Create installation folder
    nisfere_installation_folder.mkdir(exist_ok=True)

    # Update package database
    run_command(["sudo", "pacman", "-Sy"])

    # Install yay if not present
    if check_command("yay"):
        print("Yay is already installed.")
    else:
        install_yay(nisfere_installation_folder)

    # Run installation steps
    install_packages()
    install_zsh(script_dir, nisfere_installation_folder)
    install_vscode_extension(script_dir)
    copy_files(script_dir, nisfere_installation_folder)
    setup_icons_and_cursor()
    setup_nisfere(script_dir, nisfere_installation_folder)
    setup_scripts(scripts_folder)

    print(f"{Colors.GREEN}✔ Installation complete!{Colors.RESET}")


if __name__ == "__main__":
    main()
