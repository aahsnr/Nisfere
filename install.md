# Line-by-Line Python Script Explanation

## Lines 1-8: Shebang and Imports

```python
#!/usr/bin/env python3
```

- **Shebang line**: Tells the system to use Python 3 to run this script
- The `#!` is called a "shebang" - it's a special comment that tells Unix/Linux which interpreter to use

```python
import os
import sys
import subprocess
import shutil
import tempfile
import json
from pathlib import Path
```

**Import statements**: These bring in Python modules (libraries) we'll use
- `os`: Operating system interface (check user ID, environment variables)
- `sys`: System-specific parameters (exit the program)
- `subprocess`: Run shell commands from Python
- `shutil`: High-level file operations (copy, move files)
- `tempfile`: Create temporary files and directories
- `json`: Work with JSON data (JavaScript Object Notation)
- `pathlib.Path`: Modern way to work with file paths

## Lines 10-14: Color Class Definition

```python
class Colors:
    GREEN = "\033[1;32m"
    BLUE = "\033[1;34m"
    RESET = "\033[0m"
```

**Class definition**: Creates a container for color codes
- These are ANSI escape sequences that make text colorful in the terminal
- `GREEN`: Makes text green and bold
- `BLUE`: Makes text blue and bold
- `RESET`: Returns text to normal color

## Lines 16-22: Banner Function

```python
def print_banner():
    """Print the Nisfere banner"""
    print(f"{Colors.BLUE}   N   N I   SSS  FFFFF EEEEE RRRR  EEEEE{Colors.RESET}")
    print(f"{Colors.BLUE}  N  N N I  S     F     E     R   R E     {Colors.RESET}")
    print(f"{Colors.BLUE}  N  N N I  SSS   FFFF  EEEE  RRRR  EEEE  {Colors.RESET}")
    print(f"{Colors.BLUE}  N  N N I     S  F     E     R  R  E     {Colors.RESET}")
    print(f"{Colors.BLUE}  N   N  I  SSS   F     EEEEE R   R EEEEE{Colors.RESET}")
```
- **Function definition**: `def` creates a function named `print_banner`
- **Docstring**: The text in triple quotes explains what the function does
- **f-strings**: `f"..."` allows us to insert variables into strings
- Each `print()` displays one line of ASCII art spelling "NISFERE" in blue

## Lines 24-33: Arch Linux Check

```python
def abort_if_not_arch():
    """Check if running on Arch Linux"""
    try:
        with open('/etc/os-release', 'r') as f:
            if 'arch' not in f.read().lower():
                print("This script is designed to run on Arch Linux. Exiting.")
                sys.exit(1)
    except FileNotFoundError:
        print("Cannot determine OS. This script is designed for Arch Linux. Exiting.")
        sys.exit(1)
```
- **Function definition**: Checks if we're on Arch Linux
- **try-except block**: Handle errors gracefully
- **with open()**: Opens a file safely (automatically closes it)
- `/etc/os-release`: File containing OS information
- `f.read().lower()`: Read file contents and convert to lowercase
- `'arch' not in`: Check if 'arch' is missing from the text
- `sys.exit(1)`: Exit the program with error code 1
- **FileNotFoundError**: Catches the error if file doesn't exist

## Lines 35-40: Root User Check

```python
def abort_if_root():
    """Check if running as root"""
    if os.geteuid() == 0:
        print("Please do not run this script as root. Exiting.")
        sys.exit(1)
```
- **Function definition**: Prevents running as root user
- `os.geteuid()`: Gets the effective user ID
- `== 0`: Root user always has ID 0
- Safety measure: Running as root can be dangerous

## Lines 42-45: Command Check

```python
def check_command(command):
    """Check if a command exists"""
    return shutil.which(command) is not None
```
- **Function definition**: Checks if a command is available
- `shutil.which()`: Finds the path to a command (like `which` in bash)
- `is not None`: Returns True if command exists, False if it doesn't
- **return**: Sends the result back to whoever called this function

## Lines 47-59: Command Runner

```python
def run_command(cmd, shell=False, check=True, capture_output=False):
    """Run a command with error handling"""
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, check=check, 
                                  capture_output=capture_output, text=True)
        else:
            result = subprocess.run(cmd, check=check, 
                                  capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        if not check:
            return e
        sys.exit(1)
```
- **Function definition**: Runs shell commands from Python
- **Parameters**: `cmd` (command), `shell` (run in shell), `check` (exit on error), `capture_output` (save output)
- **try-except**: Handle command failures
- `subprocess.run()`: Execute the command
- `shell=True`: Run command through shell (like typing in terminal)
- `check=True`: Exit if command fails
- `capture_output=True`: Save command output to variable
- `text=True`: Return output as text (not bytes)
- **CalledProcessError**: Error when command fails

## Lines 61-76: Yay Installation

```python
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
```
- **Function definition**: Installs yay (AUR helper for Arch Linux)
- `Path() / "yay"`: Creates a path by joining folder + "yay"
- **Git clone**: Downloads yay source code
- `str(yay_dir)`: Converts Path object to string
- `os.getcwd()`: Get current working directory
- `os.chdir()`: Change to different directory
- **try-finally**: Ensures we return to original directory even if build fails
- `makepkg -si --noconfirm`: Build and install package without prompts

## Lines 78-98: Package Installation

```python
def install_packages():
    """Install required packages"""
    print("Installing required packages...")
    
    # Pacman packages
    pacman_packages = [
        "fastfetch", "bpytop", "pipewire", "playerctl", "networkmanager", 
        "brightnessctl", "pkgconf", "wf-recorder", "thunar", "thunar-archive-plugin", 
        "xarchiver", "zip", "unzip", "gvfs", "swww", "zsh", "alacritty", 
        "libnotify", "python", "gtk3", "cairo", "gtk-layer-shell", 
        "libgirepository", "gobject-introspection", "gobject-introspection-runtime", 
        "python-pip", "python-gobject", "python-psutil", "python-cairo", 
        "python-dbus", "python-pydbus", "python-loguru", "python-setproctitle", 
        "grim", "swappy", "code"
    ]
    
    pacman_cmd = ["sudo", "pacman", "-Syu", "--noconfirm", "--needed"] + pacman_packages
    run_command(pacman_cmd)
    
    # Yay packages
    yay_packages = [
        "python-fabric", "swaylock-effects-git", "swayidle", 
        "gnome-bluetooth-3.0", "fabric-cli-git", "slurp", "imagemagick"
    ]
    
    yay_cmd = ["yay", "-S", "--noconfirm", "--needed"] + yay_packages
    run_command(yay_cmd)
    
    print(f"{Colors.GREEN}✔ Packages installed.{Colors.RESET}")
```
- **List definition**: Creates lists of package names
- **List concatenation**: `+` joins the command with package list
- `pacman -Syu`: Update system and install packages
- `--noconfirm`: Don't ask for confirmation
- `--needed`: Only install if not already installed
- **Yay packages**: AUR packages not in official repos

## Lines 100-134: VSCode Configuration

```python
def install_vscode_extension(script_dir):
    """Configure VSCode with Nisfere theme"""
    print("Configuring VSCode...")
    
    # Define paths
    vscode_extensions_dir = Path.home() / ".vscode-oss" / "extensions"
    vscode_settings_file = Path.home() / ".config" / "Code - OSS" / "User" / "settings.json"
    
    # Ensure extensions directory exists
    vscode_extensions_dir.mkdir(parents=True, exist_ok=True)
```
- **Path.home()**: Gets user's home directory
- **Path joining**: `/` operator joins path components
- `mkdir(parents=True, exist_ok=True)`: Create directory and all parent directories, don't error if exists

```python
    # Copy theme extension
    vscode_source = Path(script_dir) / "vscode"
    if vscode_source.exists():
        for item in vscode_source.iterdir():
            if item.is_dir():
                shutil.copytree(item, vscode_extensions_dir / item.name, dirs_exist_ok=True)
            else:
                shutil.copy2(item, vscode_extensions_dir)
```
- **Path.exists()**: Check if path exists
- **iterdir()**: Loop through all items in directory
- **is_dir()**: Check if item is a directory
- **copytree()**: Copy entire directory tree
- **copy2()**: Copy file with metadata
- `dirs_exist_ok=True`: Don't error if directory already exists

```python
    # Ensure settings.json exists
    vscode_settings_file.parent.mkdir(parents=True, exist_ok=True)
    if not vscode_settings_file.exists():
        with open(vscode_settings_file, 'w') as f:
            json.dump({}, f)
```
- **parent**: Get parent directory of the file
- **json.dump()**: Write empty dictionary `{}` to file as JSON

```python
    # Update settings.json with theme
    try:
        with open(vscode_settings_file, 'r') as f:
            settings = json.load(f)
        
        settings["workbench.colorTheme"] = "Nisfere"
        
        with open(vscode_settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
    except (json.JSONDecodeError, FileNotFoundError):
        # If file is corrupted or missing, create new one
        with open(vscode_settings_file, 'w') as f:
            json.dump({"workbench.colorTheme": "Nisfere"}, f, indent=2)
```
- **json.load()**: Read JSON from file into Python dictionary
- **Dictionary access**: `settings["key"]` sets a value
- `indent=2`: Makes JSON pretty-printed with 2-space indentation
- **Multiple exceptions**: Catches JSON errors or missing file

## Lines 136-170: Zsh Configuration

```python
def install_zsh(script_dir, nisfere_installation_folder):
    """Configure Zsh with plugins"""
    print("Configuring Zsh...")
    
    # Copy .zshrc
    zshrc_source = Path(script_dir) / "zsh" / ".zshrc"
    zshrc_dest = Path.home() / ".zshrc"
    if zshrc_source.exists():
        shutil.copy2(zshrc_source, zshrc_dest)
```
- **File copying**: Copy Zsh configuration file to home directory

```python
    # Setup plugins
    zsh_folder = Path(nisfere_installation_folder) / "zsh"
    plugins_folder = zsh_folder / "plugins"
    plugins_folder.mkdir(parents=True, exist_ok=True)
    
    plugins = [
        "zsh-syntax-highlighting",
        "zsh-autosuggestions", 
        "zsh-history-substring-search"
    ]
    
    for plugin in plugins:
        plugin_dir = plugins_folder / plugin
        if not plugin_dir.exists():
            repo_url = f"https://github.com/zsh-users/{plugin}.git"
            run_command(["git", "clone", repo_url, str(plugin_dir)])
```
- **For loop**: Iterate through each plugin name
- **f-string**: Insert plugin name into GitHub URL
- **Git clone**: Download each plugin

```python
    # Ensure Zsh history file exists
    history_file = Path.home() / ".zsh_history"
    if not history_file.exists():
        history_file.touch()
        os.chmod(history_file, 0o600)
```
- **touch()**: Create empty file
- **chmod()**: Set file permissions
- `0o600`: Octal notation for read/write by owner only

```python
    # Change default shell to zsh
    username = os.getenv("USER")
    run_command(["sudo", "chsh", "-s", "/bin/zsh", username])
```
- **os.getenv()**: Get environment variable value
- **chsh**: Change user's default shell

## Lines 172-217: File Copying

```python
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
        home / ".config" / "nisfere" / "themes"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
```
- **List of paths**: Create all needed directories
- **Loop**: Create each directory

```python
    # Copy files
    copy_mappings = [
        ("fonts", home / ".fonts"),
        ("gtk-themes", home / ".themes"), 
        ("dotfiles", home / ".config")
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
```
- **Tuple unpacking**: `source_dir, dest_dir` gets both values from tuple
- **Nested loops**: Outer loop for mappings, inner loop for files

```python
    # Create notifications file
    notifications_file = home / ".cache" / "nisfere" / "notifications.json"
    with open(notifications_file, 'w') as f:
        json.dump([], f)
```
- **json.dump()**: Write empty list `[]` to file

```python
    # Copy panel config
    panel_config_source = script_path / "nisfere" / "panel" / "config.json"
    panel_config_dest = home / ".config" / "nisfere" / "panel-config.json"
    if panel_config_source.exists():
        shutil.copy2(panel_config_source, panel_config_dest)
```
- **Conditional copy**: Only copy if source file exists

## Lines 219-290: Icons and Cursor Setup

```python
def setup_icons_and_cursor():
    """Setup icons and cursor themes"""
    print("Setting up icons and cursor...")
    
    icons_dest = Path.home() / ".icons"
    icons_dest.mkdir(exist_ok=True)
    
    # Icon repositories to clone
    icon_repos = [
        ("dracula-icons", "https://github.com/m4thewz/dracula-icons"),
        ("Zafiro-Nord-Dark", "https://github.com/zayronxio/Zafiro-Nord-Dark.git"),
        ("Breeze-Adapta-Cursor", "https://github.com/mustafaozhan/Breeze-Adapta-Cursor")
    ]
    
    for icon_name, repo_url in icon_repos:
        icon_path = icons_dest / icon_name
        if not icon_path.exists():
            run_command(["git", "clone", repo_url, str(icon_path)])
```
- **List of tuples**: Each tuple contains (name, URL)
- **Simple cloning**: Clone if directory doesn't exist

```python
    # Special handling for Catppuccin icons
    catppuccin_path = icons_dest / "Catppuccin-Mocha"
    if not catppuccin_path.exists():
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_url = "https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme.git"
            run_command(["git", "clone", repo_url, temp_dir])
            source_path = Path(temp_dir) / "icons" / "Catppuccin-Mocha"
            if source_path.exists():
                shutil.copytree(source_path, catppuccin_path)
```
- **TemporaryDirectory**: Creates temp folder, automatically deletes it
- **with statement**: Ensures cleanup even if error occurs
- **Selective copying**: Only copy specific subfolder from repo

```python
    # Set cursor theme
    run_command(["hyprctl", "setcursor", "Breeze-Adapta-Cursor", "17"], check=False)
    run_command(["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", "Breeze-Adapta-Cursor"], check=False)
    run_command(["gsettings", "set", "org.gnome.desktop.interface", "cursor-size", "17"], check=False)
```
- `check=False`: Don't exit if these commands fail
- **hyprctl**: Hyprland window manager command
- **gsettings**: GNOME settings database

## Lines 292-306: Nisfere Setup

```python
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
```
- **Recursive copying**: Copy entire nisfere directory structure

## Lines 308-332: Scripts Setup

```python
def setup_scripts(scripts_folder):
    """Setup and execute scripts"""
    print("Setting up scripts...")
    
    scripts_path = Path(scripts_folder)
    
    # Make scripts executable
    scripts_to_chmod = [
        "change-theme.sh",
        "init-swww.sh", 
        "init-panel.sh"
    ]
    
    for script in scripts_to_chmod:
        script_path = scripts_path / script
        if script_path.exists():
            os.chmod(script_path, 0o755)
```
- **chmod 755**: Make files executable (read/write/execute for owner, read/execute for others)

```python
    # Execute scripts
    run_command([str(scripts_path / "change-theme.sh"), "dracula"], check=False)
    run_command([str(scripts_path / "init-panel.sh")], 
               capture_output=True, check=False)
    run_command([str(scripts_path / "init-swww.sh")], 
               capture_output=True, check=False)
```
- **Script execution**: Run the setup scripts
- `capture_output=True`: Don't show output to user
- `check=False`: Don't exit if scripts fail

## Lines 334-369: Main Function

```python
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
```
- **Main function**: Orchestrates the entire installation
- **__file__**: Special variable containing current script path
- **parent**: Get directory containing the script
- **resolve()**: Get absolute path

```python
    # Update package database
    run_command(["sudo", "pacman", "-Sy"])
    
    # Install yay if not present
    if check_command("yay"):
        print("Yay is already installed.")
    else:
        install_yay(nisfere_installation_folder)
```
- **Conditional installation**: Only install yay if not present

```python
    # Run installation steps
    install_packages()
    install_zsh(script_dir, nisfere_installation_folder)
    install_vscode_extension(script_dir)
    copy_files(script_dir, nisfere_installation_folder)
    setup_icons_and_cursor()
    setup_nisfere(script_dir, nisfere_installation_folder)
    setup_scripts(scripts_folder)
    
    print(f"{Colors.GREEN}✔ Installation complete!{Colors.RESET}")
```
- **Sequential execution**: Call each setup function in order

## Lines 371-373: Script Entry Point

```python
if __name__ == "__main__":
    main()
```
- **Entry point**: Only run main() if script is executed directly
- **__name__**: Special variable that's "__main__" when script is run directly
- This prevents main() from running if script is imported as a module

## Summary

This Python script is a comprehensive installer that:
1. Checks system compatibility
2. Installs required packages
3. Configures development environment
4. Sets up themes and icons
5. Configures shell and applications
6. Runs initialization scripts

The script uses modern Python practices like pathlib, context managers, and proper error handling to create a robust installer for the Nisfere desktop environment.
