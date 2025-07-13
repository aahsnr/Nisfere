
Great, I’ll go through the `install.py` script line-by-line and explain every part, including imports, class definitions, and method logic, in a detailed and verbose manner so you understand exactly what each component does. I’ll get started and update you shortly.


# Nisfere Installer (`install.py`) – Detailed Line-by-Line Explanation

Below is a thorough explanation of each line of the `install.py` script, which automates setting up the Nisfere environment on Fedora Linux. We explain what each line and block of code does and why it’s needed.

## Shebang and Imports

* `#!/usr/bin/env python3`

  * This is the **shebang** line (line 0). It tells the operating system that this script should be run using Python 3. It uses `/usr/bin/env` to find the `python3` interpreter in the user's environment path. This line allows you to run the script directly (for example, with `./install.py`) if it has execute permissions.

* `import os`

  * This imports the built-in Python **os** module (line 2). The `os` module provides a way of using operating system dependent functionality, like reading environment variables, working with file paths, and executing shell commands. In this script, it will be used for file and directory operations.

* `import sys`

  * This imports the built-in Python **sys** module (line 3). The `sys` module gives access to some variables used or maintained by the Python interpreter, and functions that interact with the interpreter. In this script, `sys` is used to exit the program (`sys.exit`) and possibly for other system-related tasks.

* `import subprocess`

  * This imports the **subprocess** module (line 4). The `subprocess` module allows the script to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. Here it will be used to run shell commands (like `dnf` and `git`) from within Python.

* `import shutil`

  * This imports the **shutil** module (line 5). `shutil` provides high-level operations on files and collections of files. It is used here for copying files and directories (`shutil.copytree`, `shutil.copy2`, etc.) and checking for the existence of executables (`shutil.which`).

* `import json`

  * This imports the **json** module (line 6). The `json` module is for working with JSON data (reading, writing, parsing). In this script, it looks like it's used to initialize or write JSON content (for example, to a notifications file).

* `from pathlib import Path`

  * This line (line 7) imports the `Path` class from the built-in **pathlib** module. `Path` provides an object-oriented way to work with file system paths. Rather than using raw strings for file paths, the script uses `Path` objects which make path manipulation (like joining paths) more convenient and platform-independent.

* `from typing import List, Optional`

  * This imports the `List` and `Optional` types from the **typing** module (line 8), which are used for type annotations. `List[str]` would indicate a list of strings, and `Optional[T]` indicates a variable that could be of type `T` or `None`. This helps with documentation and can be checked by type checkers, but does not affect runtime behavior.

## `Colors` Class

* `class Colors:` (line 11)

  * This defines a class named `Colors`. It will be used to store string constants that represent ANSI color codes for colored terminal output.

* `GREEN = "\033[1;32m"` (line 12)

  * Inside the `Colors` class, this line defines a class-level constant `GREEN`. The value `"\033[1;32m"` is an ANSI escape code that changes the text color in the terminal to green and makes it bold (the `1;` means bold bright, and `32m` is the code for green). This allows colored messages to be printed.

* `BLUE = "\033[1;34m"` (line 13)

  * This defines a constant `BLUE` inside `Colors` for a blue text color (bold). The escape code `\033[1;34m` will make text appear bright blue in the terminal.

* `RED = "\033[1;31m"` (line 14)

  * This defines `RED` with the code `\033[1;31m`, which makes text bright red. This color can be used to highlight errors or warnings.

* `RESET = "\033[0m"` (line 15)

  * The `RESET` constant with code `\033[0m` resets the text color back to default. After printing colored text, adding this code returns the terminal text color to normal. Without it, all subsequent text would remain colored.

The `Colors` class is simply a namespace for these constants. It doesn’t have methods or an `__init__` method because we only use it for static color codes.

## `NisfereInstaller` Class Initialization

* `class NisfereInstaller:` (line 18)

  * This defines a class named `NisfereInstaller`. Instances of this class will perform the steps needed to install and configure the Nisfere environment. Grouping functionality in a class allows for clean organization of methods and shared data (like folder paths).

* `def __init__(self):` (line 19)

  * This is the **constructor method** of the class `NisfereInstaller`. It runs automatically when you create a new instance (like `installer = NisfereInstaller()`). This method sets up important properties (attributes) that the installer will use.

* `self.home = Path.home()` (line 20)

  * This line sets the instance variable `self.home` to the user's home directory. `Path.home()` returns a `Path` object pointing to the current user’s home directory (e.g., `/home/username`). This will be used as a base for creating and copying configuration files into the correct user locations.

* `self.script_dir = Path(__file__).parent.resolve()` (line 21)

  * `__file__` is a special variable that holds the path of the currently running script (`install.py`). `Path(__file__)` makes it a `Path` object. `.parent` gets the directory containing the script. `.resolve()` converts it to an absolute path. So `self.script_dir` is the absolute directory where `install.py` is located. This is useful for referring to files that are distributed along with the script (e.g., font files or config files in the same package).

* `self.nisfere_folder = self.home / ".nisfere"` (line 22)

  * This defines `self.nisfere_folder` as a `Path` for the directory `~/.nisfere` inside the user's home. Using `self.home / ".nisfere"` uses the `/` operator of `Path` to append a subdirectory. This is where Nisfere application files will be copied during setup.

* `self.scripts_folder = self.nisfere_folder / "scripts"` (line 23)

  * This sets `self.scripts_folder` to `~/.nisfere/scripts`. It is likely where additional scripts related to Nisfere (provided by the installer) will be placed. It uses the previously defined `self.nisfere_folder` path as a base.

* **Comment:** `# Package list` (line 25)

  * This comment indicates that the next lines will define a list of packages to install.

* `self.packages = [` (line 26)

  * This begins defining `self.packages`, a list of package names needed for Nisfere. Each string in this list corresponds to a software package that should be installed via Fedora's package manager (DNF). Each package will be installed to ensure all dependencies and utilities Nisfere needs are present. The list continues from lines 27 through 64.

  The items in `self.packages` (lines 27-64) include:

  * `"fastfetch"`: a tool similar to neofetch for system info display.
  * `"btop"`: a resource monitor (CPU, memory, etc.).
  * `"pipewire"`: a multimedia (audio/video) framework.
  * `"playerctl"`: a command-line utility to control media players.
  * `"NetworkManager"`: network configuration service.
  * `"brightnessctl"`: controls brightness of monitors.
  * `"pkgconf"`: a package configuration tool.
  * `"wf-recorder"`: screen recording for Wayland.
  * `"thunar"`: a file manager for Xfce (lightweight file manager).
  * `"thunar-archive-plugin"`: plugin to archive files in Thunar.
  * `"file-roller"`: an archive manager (for compressing/extracting).
  * `"zip"`, `"unzip"`: utilities for handling zip archives.
  * `"gvfs"`: virtual filesystem service used by desktop environments.
  * `"swww"`: a tool for setting wallpapers on Wayland.
  * `"zsh"`: the Z shell, an alternative to bash.
  * `"kitty"`: a GPU-based terminal emulator.
  * `"libnotify"`: desktop notifications library.
  * `"python3"`, `"python3-pip"`: ensure Python3 and pip are installed (though the script runs with Python, installing these ensures Python3 and pip are recognized by the system).
  * `"gtk3"`, `"cairo"`, `"gtk-layer-shell"`, `"gobject-introspection"`, `"gobject-introspection-runtime"`: these are libraries for creating GUI applications and integrating with GTK and Wayland.
  * `"python3-gobject"`, `"python3-psutil"`, `"python3-cairo"`, `"python3-dbus"`, `"python3-loguru"`, `"python3-setproctitle"`: Python libraries needed by the Nisfere application.
  * `"grim"`, `"swappy"`, `"slurp"`: screenshot and annotation tools (common in Wayland setups).
  * `"hyprlock"`, `"hypridle"`: tools related to Hyprland (a Wayland compositor).
  * `"gnome-bluetooth"`: Bluetooth support for GNOME (may be needed for Bluetooth on Wayland).
  * `"ImageMagick"`: an image processing suite (might be used for wallpapers or screenshots).

  Each package is needed to ensure the environment has all required tools and libraries. If any package is missing, parts of Nisfere might not work properly.

* **Comment:** `# COPR repositories to enable` (line 67)

  * This comment signals that the following code sets up a list of COPR (Cool Other Package Repo) repositories, which are community builds for Fedora. This list can contain additional software repos to enable.

* `self.copr_repos = [` (line 68)

  * This starts defining `self.copr_repos`, a list of COPR repository names and descriptions to enable. It's currently mostly commented out examples. If a user needed additional software not in official Fedora repos, they could specify COPR repos here. Each item can be a string (repo name) or a tuple of (name, description).

  The commented-out lines 70-74 show example COPR repo entries (commented with `#`):

  * `("solopasha/hyprland", "Latest Hyprland compositor")`
  * `("alebastr/waybar", "Enhanced Waybar builds")`
  * `("erikreider/SwayNotificationCenter", "Notification center for sway")`
  * `("wezfurlong/wezterm-nightly", "WezTerm terminal emulator")`

  Since they are commented out, `self.copr_repos` ends up being an empty list `[]`.

## `print_colored` Method

* `def print_colored(self, message: str, color: str = Colors.RESET) -> None:` (line 77)

  * This line defines a method called `print_colored` inside `NisfereInstaller`. It takes `message` (a string to print) and `color` (another string, defaulting to `Colors.RESET`). The `-> None` indicates it returns nothing. This method will print messages to the console using a given color, making the script’s output more user-friendly.

* `"""Print colored message to stdout"""` (line 78)

  * This is a **docstring** for the `print_colored` method, explaining that its purpose is to print colored messages to standard output (the console).

* `print(f"{color}{message}{Colors.RESET}")` (line 79)

  * This line prints the message in color. It uses an f-string to format the output: it first outputs the color code (e.g., `\033[1;32m` for green), then the message text, and then `Colors.RESET` to reset the color after the message. This ensures only the message is colored, not subsequent text. If `color` was not provided, it defaults to `Colors.RESET` which is no color (just default text).

This method allows other parts of the script to call `self.print_colored("some text", Colors.RED)` to get red output, or use `self.print_colored("OK", Colors.GREEN)` for green success messages.

## `print_banner` Method

* `def print_banner(self) -> None:` (line 81)

  * This defines the `print_banner` method. It takes only `self` and returns nothing. Its job is to print a large ASCII-art banner for Nisfere when the installation starts.

* `"""Print the installation banner"""` (line 82)

  * Docstring explaining that this method prints a banner at the start of the script.

* `banner_lines = [` (line 83)

  * This creates a list of strings called `banner_lines`. Each string is a line of ASCII art spelling out "NISFERE". The art is arranged so that when printed, it forms a stylized banner.

* The lines 84-88 in `banner_lines`:

  ```
  "   N   N I   SSS  FFFFF EEEEE RRRR  EEEEE",
  "  N  N N I  S     F     E     R   R E     ",
  "  N  N N I  SSS   FFFF  EEEE  RRRR  EEEE  ",
  "  N  N N I     S  F     E     R  R  E     ",
  "  N   N  I  SSS   F     EEEEE R   R EEEEE",
  ```

  Each string here corresponds to one row of the banner.

* `for line in banner_lines:` (line 91)

  * This loop goes through each line of the banner.

* `self.print_colored(line, Colors.BLUE)` (line 92)

  * For each line in the banner, this prints the line in blue color. It calls the `print_colored` method defined earlier, passing `line` as the message and `Colors.BLUE` as the color. This results in the entire ASCII banner being printed in blue text.

The banner visually identifies Nisfere to the user at the start of the installation process.

## `check_fedora` Method

* `def check_fedora(self) -> None:` (line 94)

  * This line defines the `check_fedora` method. It checks whether the operating system is Fedora Linux, since the script is designed specifically for Fedora. It returns nothing.

* `"""Check if running on Fedora Linux"""` (line 95)

  * Docstring describing the purpose of the method.

* `try:` (line 96)

  * The script tries to open the file `/etc/os-release` to read system information. The `try` block is used because on some systems this file might not exist.

* `with open("/etc/os-release", "r") as f:` (line 97)

  * This line attempts to open the file `/etc/os-release`, which is a standard file on Linux systems containing OS identification information (like name, version, ID). It's opened in read mode (`"r"`). The `with` statement ensures the file will be closed automatically after reading.

* `content = f.read()` (line 98)

  * Reads the entire content of `/etc/os-release` into the variable `content` as a string.

* `if "fedora" not in content.lower():` (line 99)

  * Checks if the word `"fedora"` (case-insensitive) does not appear in the OS release information. `content.lower()` converts the content to lowercase, so the check is case-insensitive. If `"fedora"` is not found, then the system is not Fedora or not recognized as Fedora.

* `self.print_colored(..., Colors.RED)` (lines 100-104)

  * If the above `if` condition is true (meaning it's not Fedora), the script prints an error message in red: `"This script is designed to run on Fedora Linux. Exiting."` and then exits. The message is split across lines 100-102 for readability, but it prints as one line. The exit (`sys.exit(1)`) on line 105 stops the script with an error code.

* `sys.exit(1)` (line 105)

  * Exits the program with a status code `1`, indicating an error. This happens if the OS is not Fedora (as determined above).

* `except FileNotFoundError:` (line 106)

  * This catches the case where opening `/etc/os-release` fails because the file is not found. Some unusual systems might not have this file.

* `self.print_colored(..., Colors.RED)` (lines 107-110)

  * If the file could not be opened, the script prints a red error: `"Cannot determine OS. This script is designed for Fedora Linux."` to inform the user.

* `sys.exit(1)` (line 112)

  * After catching the exception, it exits with status 1, just like the other branch, because if the OS can't be determined it should not proceed.

The `check_fedora` method ensures early on that the script is running on a compatible system. This prevents potentially breaking another system with Fedora-specific commands.

## `run_command` Method

* `def run_command(self, command: List[str], check: bool = True, capture_output: bool = False) -> subprocess.CompletedProcess:` (line 114-117)

  * This defines `run_command`, a helper method to execute shell commands. It takes:

    * `command`: a list of strings, where the first is the command and the rest are arguments (e.g., `["sudo", "dnf", "update", "-y"]`).
    * `check`: a boolean (default `True`) that, if `True`, tells `subprocess.run` to raise an error if the command fails.
    * `capture_output`: a boolean (default `False`) that, if `True`, captures the output of the command instead of letting it go to the console.
  * The method returns a `subprocess.CompletedProcess` object which contains the command’s exit status, stdout, and stderr.

* `"""Run a system command with error handling"""` (line 118)

  * Docstring explaining that this method wraps command execution with error handling.

* `try:` (line 119)

  * The method tries to run the command and capture the result. Any exceptions (like the command failing) are handled below.

* `result = subprocess.run(command, check=check, capture_output=capture_output, text=True)` (line 120-122)

  * Calls `subprocess.run` to execute the command.

    * `command` is the list of command parts.
    * `check=check` means if `check` is `True` and the command exits with a non-zero status, `subprocess.run` will raise a `CalledProcessError`.
    * `capture_output=capture_output` decides whether to capture stdout/stderr (if `True`, the output is stored in the `result` object; if `False`, output goes directly to the console).
    * `text=True` makes the output text (string) instead of bytes.
  * The result of this run (exit code, output) is stored in `result`.

* `return result` (line 123)

  * If the command runs successfully (or if `check=False` so errors are allowed), the method returns the `CompletedProcess` object which contains details like `result.returncode`.

* `except subprocess.CalledProcessError as e:` (line 124)

  * If `subprocess.run` raises a `CalledProcessError` (which happens if `check=True` and the command failed), we enter this exception block.

* `self.print_colored(f"Command failed: {' '.join(command)}", Colors.RED)` (lines 125-126)

  * Prints an error message in red showing the command that failed. It joins the list `command` into a string for display.

* `if check:` (line 127)

  * Checks if `check` was True (which means a failure should stop execution).

* `raise` (line 128)

  * If `check` is True, re-raise the exception so that it will propagate and probably stop the script (since unhandled exception leads to program exit).

* `return e` (line 129)

  * If `check` was False (so command failures were tolerated), the method returns the exception object `e` as if it were a result. This allows the caller to examine `e.returncode` or other details.

The `run_command` method centralizes running shell commands and handling errors, so the rest of the script can just call this method and not worry about try/except each time. It also uniformly prints an error if a command fails.

## `command_exists` Method

* `def command_exists(self, command: str) -> bool:` (line 131)

  * This defines `command_exists`, a helper method that checks if a given command is available on the system. It returns `True` if the command is found in the system's PATH, or `False` otherwise.

* `"""Check if a command exists in the system PATH"""` (line 132)

  * Docstring describing the method’s purpose.

* `return shutil.which(command) is not None` (line 133)

  * Uses `shutil.which(command)` to check for an executable in the PATH. If the command is found, `which` returns its path; if not, it returns `None`. So if the result is not `None`, the command exists. This is used later, for example, to check if `hyprctl` or `gsettings` commands are available before using them.

## `install_packages` Method

* `def install_packages(self) -> None:` (line 135)

  * Defines the `install_packages` method. This method installs all required packages listed in `self.packages` using Fedora’s package manager (DNF). It returns nothing.

* `"""Install required packages using DNF"""` (line 136)

  * Docstring describing the purpose of this method.

* `self.print_colored("Installing required packages...")` (line 137)

  * Prints a status message (in default color) saying it is starting the package installation.

* **Update system** (comment at line 139)

  * The script updates the system before installing new packages. Keeping packages up-to-date is a good practice.

* `self.print_colored("Updating system packages...")` (line 140)

  * Prints a message "Updating system packages..." to inform the user.

* `self.run_command(["sudo", "dnf", "update", "-y"])` (line 141)

  * Runs the system update command via DNF: `sudo dnf update -y`. This updates all installed packages to their latest versions. `-y` means it will automatically answer "yes" to any prompts. It uses `run_command` to handle execution and errors.

* **Install dnf-plugins-core** (comment line 143)

  * DNF needs `dnf-plugins-core` package to enable adding COPR repos.

* `self.print_colored("Installing dnf-plugins-core for COPR support...")` (line 144)

  * Prints that it’s installing the DNF plugins core package.

* `self.run_command(["sudo", "dnf", "install", "-y", "dnf-plugins-core"])` (line 145)

  * Runs `sudo dnf install -y dnf-plugins-core` to install DNF plugin support. This is required to enable COPR repos later.

* **Install all packages** (comment line 147)

  * Now install the rest of the needed packages in one command.

* `self.print_colored("Installing application packages...")` (line 148)

  * Prints "Installing application packages..." to let user know it's installing the listed packages.

* `install_cmd = ["sudo", "dnf", "install", "-y"] + self.packages` (line 149)

  * Builds the command to run. It starts with `["sudo", "dnf", "install", "-y"]` and then appends the list of all package names (`self.packages`). The result is a single list of strings like `["sudo", "dnf", "install", "-y", "fastfetch", "btop", ...]`.

* `self.run_command(install_cmd)` (line 150)

  * Executes the DNF install command with all packages. If any package fails to install, because `check=True` by default, the method will raise an error and likely exit the script.

* `self.print_colored("✔ Packages installed.", Colors.GREEN)` (line 152)

  * After installing packages, it prints a success message "✔ Packages installed." in green color (using the green checkmark and text). This indicates completion of this step.

This method ensures the system has all the required software installed.

## `enable_copr_repositories` Method

* `def enable_copr_repositories(self) -> None:` (line 154)

  * This method enables the COPR repositories listed in `self.copr_repos`. COPR repos are special Fedora community repositories that may contain additional or newer software. It returns nothing.

* `"""Enable COPR repositories"""` (line 155)

  * Docstring for the method.

* `if not self.copr_repos:` (line 156)

  * Checks if the `copr_repos` list is empty. If there are no repositories listed, there's nothing to do.

* `self.print_colored("No COPR repositories configured to enable.")` (line 157)

  * If `self.copr_repos` is empty, it prints "No COPR repositories configured to enable." and does nothing else. (Note: this message prints in default color because no color is specified.)

* `return` (line 158)

  * Exits the method early if there are no repositories to enable.

* `self.print_colored("Enabling COPR repositories...")` (line 160)

  * If there are repositories to enable, it prints "Enabling COPR repositories..." to notify the user.

* `for repo_info in self.copr_repos:` (line 162)

  * Iterates over each entry in `self.copr_repos`. Each entry might be a tuple (repo name, description) or a single string name.

* `if isinstance(repo_info, tuple):` (line 163)

  * Checks if the current `repo_info` is a tuple. The list might allow either `("repo/name", "Description")` or just `"repo/name"`.

* `repo_name, description = repo_info` (line 164)

  * If it's a tuple, unpack it into `repo_name` and `description`.

* `self.print_colored(f"Enabling COPR repository: {repo_name} ({description})")` (lines 165-166)

  * Prints a colored message (default color since none specified) stating the repository name and description.

* `else:` (line 168)

  * If `repo_info` is not a tuple (i.e., just a string)...

* `repo_name = repo_info` (line 169)

  * Use the string itself as the `repo_name`.

* `self.print_colored(f"Enabling COPR repository: {repo_name}")` (line 170)

  * Prints a message with just the repo name.

* `result = self.run_command(["sudo", "dnf", "copr", "enable", "-y", repo_name], check=False)` (line 172-173)

  * Runs `sudo dnf copr enable -y <repo_name>` to enable the repository. `check=False` means it won't raise an exception if this fails; the script can handle failure gracefully.

* `if result.returncode == 0:` (line 176)

  * After running the command, check if its `returncode` is 0 (which means success).

* `self.print_colored(f"✔ Successfully enabled: {repo_name}", Colors.GREEN)` (line 177-178)

  * If enabling succeeded, print a green success message.

* `else:` (line 179)

  * If the return code was not 0 (indicating failure)…

* `self.print_colored(f"✗ Failed to enable: {repo_name}", Colors.RED)` (line 180-181)

  * Print a red error message showing that enabling the repository failed.

* `self.print_colored("✔ COPR repositories processed.", Colors.GREEN)` (line 183)

  * After the loop, print a green message "✔ COPR repositories processed." to indicate this step is done (even if some failed, we still finish the process).

This method handles enabling any extra Fedora repositories specified by the user to get up-to-date or special packages not in the main Fedora repos.

## `copy_files` Method

* `def copy_files(self) -> None:` (line 185)

  * Defines `copy_files`, a method that copies configuration and resource files from the installer’s directory into the user’s home directory. It returns nothing.

* `"""Copy configuration files to appropriate locations"""` (line 186)

  * Docstring explaining the purpose.

* `self.print_colored("Copying configuration files...")` (line 187)

  * Prints a message indicating that the script is about to copy config files.

* **Create necessary directories** (comment line 189)

  * The script ensures that certain directories exist before copying files into them.

* `directories = [` (line 190)

  * This defines a list of directories (`Path` objects) that need to exist in the user’s home.

* The list items (lines 191-198):

  * `self.home / ".fonts"` (line 191): `~/.fonts` directory, often used to store custom font files.
  * `self.home / ".themes"` (line 192): `~/.themes`, for custom GTK or desktop themes.
  * `self.home / ".icons"` (line 193): `~/.icons`, for icon themes.
  * `self.home / ".config"` (line 194): `~/.config`, a common directory for configuration files and subdirectories.
  * `self.home / ".cache" / "nisfere"` (line 195): `~/.cache/nisfere`, presumably to store some cache or data for Nisfere.
  * `self.home / "Videos" / "records"` (line 196): `~/Videos/records`, maybe for recorded videos (since `wf-recorder` is installed).
  * `self.home / "Pictures" / "screenshots"` (line 197): `~/Pictures/screenshots`, for storing screenshots.
  * `self.home / ".config" / "nisfere" / "themes"` (line 198): `~/.config/nisfere/themes`, likely where Nisfere theme config files will go.

* `for directory in directories:` (line 201)

  * Loop through each directory path in the `directories` list.

* `directory.mkdir(parents=True, exist_ok=True)` (line 202)

  * For each directory path, call `mkdir()` on the Path object.

    * `parents=True` means it will create any necessary parent directories (like creating `.config` if `.config/nisfere/themes` is specified).
    * `exist_ok=True` means it won't raise an error if the directory already exists.
  * This ensures all those directories exist after this loop, without error if they already did.

* **Copy files if source directories exist** (comment line 204)

  * Next, the script copies files from the installer’s repository into the user’s directories, if the source files are available.

* `file_mappings = [` (line 205)

  * Defines `file_mappings`, a list of tuples. Each tuple maps a source directory in the installer to a destination directory in the home folder. The script will copy the entire content of the source to the destination.

* The mappings (lines 206-208):

  * `(self.script_dir / "fonts", self.home / ".fonts")` (line 206): copy the "fonts" directory from the script’s location into `~/.fonts`.
  * `(self.script_dir / "gtk-themes", self.home / ".themes")` (line 207): copy "gtk-themes" to `~/.themes`.
  * `(self.script_dir / "dotfiles", self.home / ".config")` (line 208): copy "dotfiles" into `~/.config`.
    These source directories (fonts, gtk-themes, dotfiles) are assumed to exist in the directory where `install.py` is located.

* `for source, destination in file_mappings:` (line 211)

  * Loop over each (source, destination) pair in `file_mappings`.

* `if source.exists():` (line 212)

  * Check if the source directory actually exists on the filesystem.

* `shutil.copytree(source, destination, dirs_exist_ok=True)` (line 213)

  * If the source exists, copy it to the destination using `shutil.copytree`.

    * This recursively copies the entire directory tree from `source` to `destination`.
    * `dirs_exist_ok=True` allows the destination directory to already exist; it will merge contents instead of erroring. Note: this is a Python 3.8+ feature.

* `else:` (line 214)

  * If the source directory does not exist…

* `self.print_colored(f"Warning: Source directory {source} not found", Colors.RED)` (lines 215-217)

  * Print a red warning saying that the source directory was not found, and that copying is skipped. This is to inform the user that maybe some resources are missing in the installer’s package.

* **Create notifications file** (comment line 219)

  * Next the script sets up a notifications file.

* `notifications_file = self.home / ".cache" / "nisfere" / "notifications.json"` (line 220-221)

  * This defines `notifications_file` as the path `~/.cache/nisfere/notifications.json`.

* `notifications_file.write_text("[]")` (line 222)

  * This writes `"[]"` (an empty JSON array) into the `notifications.json` file, creating it if it doesn't exist. It initializes the notifications file so that Nisfere starts with an empty list of notifications.

* **Copy panel config if it exists** (comment line 224)

  * The script then tries to copy a panel configuration file.

* `panel_config_source = self.script_dir / "nisfere" / "panel" / "config.json"` (line 225-226)

  * Defines `panel_config_source` as the path to `config.json` inside `nisfere/panel` in the script directory (`install.py`’s folder).

* `panel_config_dest = self.home / ".config" / "nisfere" / "panel-config.json"` (line 227-228)

  * Defines `panel_config_dest` as `~/.config/nisfere/panel-config.json`. This is the target location for the panel configuration file.

* `if panel_config_source.exists():` (line 230)

  * Checks if the source config file exists.

* `shutil.copy2(panel_config_source, panel_config_dest)` (line 231)

  * If it exists, use `shutil.copy2` to copy the file to the destination. `copy2` copies metadata like permissions along with the file contents.

* `else:` (line 232)

  * If the source file is not found…

* `self.print_colored(f"Warning: Panel config {panel_config_source} not found", Colors.RED)` (lines 233-235)

  * Print a red warning that the panel config file wasn’t found, so the user knows the panel might not be set up.

* `self.print_colored("✔ Configuration files copied.", Colors.GREEN)` (line 238)

  * Finally, after copying files and setting up directories, it prints a green message "✔ Configuration files copied." indicating this step is complete.

The `copy_files` method sets up user configuration directories and copies over any provided fonts, themes, dotfiles, and panel config for Nisfere.

## `setup_icons_and_cursor` Method

* `def setup_icons_and_cursor(self) -> None:` (line 240)

  * Defines `setup_icons_and_cursor`. This method sets up the icon themes and cursor theme, particularly for use with Hyprland or GNOME desktops. It returns nothing.

* `"""Setup icons and cursor theme"""` (line 241)

  * Docstring describing the purpose.

* `self.print_colored("Setting up icons and cursor...")` (line 242)

  * Prints that the script is setting up icons and cursor.

* `icons_dest = self.home / ".icons"` (line 244)

  * Sets `icons_dest` to the path `~/.icons`. This is where icon and cursor themes are typically stored.

* `cursor_repo = icons_dest / "Breeze-Adapta-Cursor"` (line 245)

  * Sets `cursor_repo` to the path `~/.icons/Breeze-Adapta-Cursor`. This is a directory name (the user’s icons folder with a subfolder "Breeze-Adapta-Cursor"). It looks like the script wants to clone a GitHub repo of a cursor theme into this directory.

* **Clone cursor repository if it doesn't exist** (comment line 247)

  * The next step is to clone a cursor theme repository if not already present.

* `if not cursor_repo.exists():` (line 248)

  * Checks if the `cursor_repo` directory does not exist (meaning the cursor theme hasn’t been cloned yet).

* `self.run_command([` (lines 249-255)

  * If the directory doesn't exist, run the following git clone command:
  * `git clone https://github.com/mustafaozhan/Breeze-Adapta-Cursor <destination>`
  * The command is built as a list of arguments:

    * `"git"`, `"clone"`, the repository URL, and `str(cursor_repo)` which is the target directory.
  * This clones the "Breeze-Adapta-Cursor" theme repository into `~/.icons/Breeze-Adapta-Cursor`.

* **Set cursor for Hyprland if available** (comment line 258)

  * Now it sets the cursor theme for the Hyprland compositor, if the `hyprctl` command is available.

* `if self.command_exists("hyprctl"):` (line 259)

  * Uses the previously defined `command_exists` method to check if the command `hyprctl` is found on the system (meaning Hyprland's command-line tool is installed).

* `self.run_command(["hyprctl", "setcursor", "Breeze-Adapta-Cursor", "17"], check=False)` (lines 260-262)

  * If `hyprctl` exists, run the command `hyprctl setcursor Breeze-Adapta-Cursor 17`. This presumably sets the cursor theme to "Breeze-Adapta-Cursor" with size 17 in Hyprland. `check=False` means that if this command fails (maybe because Hyprland isn't running), the script will not crash.

* `else:` (line 264)

  * If the `hyprctl` command does not exist…

* `self.print_colored("Warning: hyprctl not found, skipping cursor setup for Hyprland")` (lines 265-267)

  * Print a warning in default color (because no color is given) that `hyprctl` is not found and skip Hyprland cursor setup.

* **Set cursor for GNOME if available** (comment line 269)

  * Next, the script attempts to set the cursor theme for GNOME desktops, if possible.

* `if self.command_exists("gsettings"):` (line 270)

  * Check if the `gsettings` command is available. `gsettings` is a command-line tool to change settings in GNOME.

* The lines 271-288:

  * If `gsettings` exists, the script runs two commands to set the cursor theme and size in GNOME:

    * `gsettings set org.gnome.desktop.interface cursor-theme Breeze-Adapta-Cursor`
      (lines 272-278) sets the cursor theme to "Breeze-Adapta-Cursor".
    * `gsettings set org.gnome.desktop.interface cursor-size 17`
      (lines 281-287) sets the cursor size to 17.
    * Both commands use `self.run_command(...)` with `check=False`, so errors won't crash the script.

* `else:` (line 291)

  * If `gsettings` is not available…

* `self.print_colored("Warning: gsettings not found, skipping GNOME cursor setup")` (lines 292-294)

  * Print a warning that it could not set the GNOME cursor.

* `self.print_colored("✔ Icons and cursor setup complete.", Colors.GREEN)` (line 296)

  * Finally, print a green success message "✔ Icons and cursor setup complete.".

This method ensures the cursor theme is available and configured for either Hyprland or GNOME if possible.

## `setup_nisfere` Method

* `def setup_nisfere(self) -> None:` (line 298)

  * Defines `setup_nisfere`. This method sets up the main Nisfere application files. It returns nothing.

* `"""Setup Nisfere application"""` (line 299)

  * Docstring describing the method.

* `self.print_colored("Setting up Nisfere...")` (line 300)

  * Prints "Setting up Nisfere..." to indicate the start of this step.

* `self.nisfere_folder.mkdir(parents=True, exist_ok=True)` (line 303)

  * Ensures that the `~/.nisfere` directory exists by creating it (and parents if needed). This was defined earlier as `self.nisfere_folder`. `exist_ok=True` means it won't error if it already exists.

* `nisfere_source = self.script_dir / "nisfere"` (line 305-306)

  * Sets `nisfere_source` to the path of a folder named "nisfere" inside the script’s directory. This likely contains the application files for Nisfere.

* `if nisfere_source.exists():` (line 307)

  * Checks if this `nisfere_source` folder exists in the script directory.

* `shutil.copytree(nisfere_source, self.nisfere_folder, dirs_exist_ok=True)` (line 308-309)

  * If the source exists, it copies the entire contents of that directory into `~/.nisfere` (the `self.nisfere_folder` path). `dirs_exist_ok=True` means it will merge into the existing `~/.nisfere` directory if it already exists (instead of failing).

* `else:` (line 310)

  * If the source directory does not exist…

* `self.print_colored(f"Warning: Nisfere source directory {nisfere_source} not found", Colors.RED)` (lines 311-313)

  * Print a red warning that the Nisfere source directory wasn’t found. This would indicate a problem with the installer distribution (maybe the user didn’t run it from the correct place).

* `self.print_colored("✔ Nisfere setup complete.", Colors.GREEN)` (line 316)

  * After copying (or skipping with a warning), it prints "✔ Nisfere setup complete." in green to show the step is done.

This method places the Nisfere application’s files into the user’s home directory.

## `setup_scripts` Method

* `def setup_scripts(self) -> None:` (line 318)

  * Defines `setup_scripts`. This method makes certain provided scripts executable and runs them as part of initialization. It returns nothing.

* `"""Setup and execute initialization scripts"""` (line 319)

  * Docstring explaining the purpose.

* `self.print_colored("Setting up scripts...")` (line 320)

  * Prints "Setting up scripts..." to indicate the beginning of this step.

* `# Scripts to make executable and run` (comment line 322)

  * Introduces the list of script files to process.

* `scripts_to_setup = [` (line 323)

  * Defines a list `scripts_to_setup`. Each item is a tuple of `(script_name, args)` where:

    * `script_name` is the name of a script file inside `~/.nisfere/scripts` directory.
    * `args` is a list of arguments to pass when running the script.

* The scripts list (lines 324-327):

  * `("change-theme.sh", ["dracula"])` (line 324): script `change-theme.sh` with argument `["dracula"]`.
  * `("init-swww.sh", [])` (line 325): script `init-swww.sh` with no arguments.
  * `("init-panel.sh", [])` (line 326): script `init-panel.sh` with no arguments.
  * (Note: These scripts must exist in the `~/.nisfere/scripts` directory. They are presumably provided as part of Nisfere to initialize theme, wallpaper service, panel, etc.)

* `for script_name, args in scripts_to_setup:` (line 329)

  * Loop over each tuple in `scripts_to_setup`.

* `script_path = self.scripts_folder / script_name` (line 330)

  * Compute `script_path` as the full path to the script: for example, `~/.nisfere/scripts/change-theme.sh`.

* `if script_path.exists():` (line 332)

  * Check if the script file actually exists.

* `script_path.chmod(0o755)` (line 334)

  * If it exists, change its mode (permissions) to `0o755`. This makes the script executable by the owner, group, and others. (In Unix permissions, `7` is read/write/execute, `5` is read/execute.)

* `cmd = [str(script_path)] + args` (line 337)

  * Build the command to execute: a list where the first element is the script file path (as a string) and then any arguments. For example, `["/home/user/.nisfere/scripts/change-theme.sh", "dracula"]`.

* `result = self.run_command(cmd, check=False, capture_output=True)` (line 338)

  * Run the script with `run_command`, but with `check=False` (so errors don’t halt the script) and `capture_output=True` (so we capture the script’s output instead of printing it). This will execute the script.

* `if result.returncode != 0:` (line 340)

  * After running the script, check if its return code is non-zero (i.e., it failed).

* `self.print_colored(f"Warning: {script_name} execution failed", Colors.RED)` (lines 341-343)

  * If the script failed, print a red warning that execution of that script failed.

* `else:` (line 344)

  * If the script file does not exist…

* `self.print_colored(f"Warning: {script_name} not found, skipping", Colors.RED)` (lines 345-347)

  * Print a red warning that the script file wasn’t found, so it was skipped.

* `self.print_colored("✔ Scripts executed.", Colors.GREEN)` (line 349)

  * After the loop, print "✔ Scripts executed." in green to indicate this step is done.

This method ensures any provided initialization scripts are made executable and run. These scripts likely perform environment-specific setup like changing theme or starting services.

## `run_installation` Method

* `def run_installation(self) -> None:` (line 351)

  * Defines `run_installation`, which orchestrates the whole installation process by calling the other methods in order. It returns nothing, but it wraps the process in error handling.

* `"""Run the complete installation process"""` (line 352)

  * Docstring describing the method.

* `try:` (line 353)

  * The installation process is wrapped in a `try` block to catch `KeyboardInterrupt` (Ctrl+C) or other exceptions and handle them gracefully.

* `self.print_banner()` (line 354)

  * Calls the method that prints the banner at the start.

* `self.check_fedora()` (line 355)

  * Calls `check_fedora()` to ensure the OS is Fedora, exiting if not.

* `# Run installation steps` (comment line 357)

  * The script then runs each step in sequence:

* `self.install_packages()` (line 358)

  * Installs all required packages.

* `self.enable_copr_repositories()` (line 359)

  * Enables any COPR repos specified (though the list is empty by default).

* `self.copy_files()` (line 360)

  * Copies config files and directories.

* `self.setup_icons_and_cursor()` (line 361)

  * Sets up icon and cursor themes.

* `self.setup_nisfere()` (line 362)

  * Copies the Nisfere application files.

* `self.setup_scripts()` (line 363)

  * Runs any provided initialization scripts.

* `self.print_colored("✔ Installation complete!", Colors.GREEN)` (line 365)

  * If all steps succeed without raising exceptions, print a green "✔ Installation complete!" message at the end.

* `except KeyboardInterrupt:` (line 367)

  * If the user interrupts the script with Ctrl+C, this exception is caught.

* `self.print_colored("\n✗ Installation interrupted by user.", Colors.RED)` (line 368)

  * Prints a red error message indicating that the installation was interrupted by the user.

* `sys.exit(1)` (line 370)

  * Exits with status code 1.

* `except Exception as e:` (line 371)

  * Catches any other exception that was not specifically a `KeyboardInterrupt`.

* `self.print_colored(f"✗ Installation failed: {str(e)}", Colors.RED)` (line 372)

  * Prints a red message including the exception message, indicating failure.

* `sys.exit(1)` (line 373)

  * Exits with status code 1.

The `run_installation` method ties everything together, providing a clear sequence and handling unexpected issues.

## `main` Function and Script Entry Point

* `def main():` (line 376)

  * Defines a top-level function `main`. This is a common Python convention for the main entry point of a script.

* `"""Main entry point"""` (line 377)

  * Docstring (brief description) for the `main` function.

* `installer = NisfereInstaller()` (line 378)

  * Inside `main`, this creates a new `NisfereInstaller` instance and assigns it to the variable `installer`. This calls the `__init__` method, setting up the initial attributes (like `home`, `script_dir`, etc.).

* `installer.run_installation()` (line 379)

  * Calls the `run_installation` method on the installer object. This starts the installation process described above.

* `if __name__ == "__main__":` (line 382)

  * This checks if the script is being run as the main program. In Python, `__name__` is set to `"__main__"` when the script is executed directly (e.g. `python install.py` or `./install.py`). If the script were imported as a module in another script, this block would not run.

* `main()` (line 383)

  * If the check is true (script is run directly), it calls the `main()` function, which starts the installation. This is the typical Python idiom to allow a script to be importable without executing its main functionality immediately.

## Summary of Control Flow

1. **Script Start:** When the script runs, Python executes the top-level code. Because of the `if __name__ == "__main__": main()` block at the end, the `main()` function gets called.
2. **`main()` Function:** Creates an instance of `NisfereInstaller` and calls `run_installation`.
3. **`run_installation`:**

   * Prints the banner.
   * Calls `check_fedora` to ensure the OS is Fedora.
   * Calls each setup method in turn:

     * `install_packages` (updates the system, installs packages).
     * `enable_copr_repositories` (enables any COPR repos listed).
     * `copy_files` (creates directories, copies config files).
     * `setup_icons_and_cursor` (clones cursor repo, sets cursor themes).
     * `setup_nisfere` (creates `.nisfere` and copies Nisfere files).
     * `setup_scripts` (makes scripts executable, runs them).
   * If all steps succeed, prints "Installation complete" in green.
   * If any step raises an exception or the user interrupts, prints an error and exits.

Throughout the script, `print_colored` is used to give colored status messages. Each method prints its own start message and a success or failure message. If any subprocess command fails and `check=True`, an exception is raised and the installation is aborted.

This completes the detailed walkthrough of each line and block in `install.py`. The script is structured to methodically prepare a Fedora environment with all the necessary dependencies, configurations, and Nisfere-specific files.
