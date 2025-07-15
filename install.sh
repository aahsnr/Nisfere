#!/bin/bash

set -euo pipefail # Enable strict error handling

# Colors for output
green="\033[1;32m"
blue="\033[1;34m"
red="\033[1;31m"
yellow="\033[1;33m"
reset="\033[0m"

print_banner() {
  echo -e "${blue}   N   N I   SSS  FFFFF EEEEE RRRR  EEEEE${reset}"
  echo -e "${blue}  N  N N I  S     F     E     R   R E     ${reset}"
  echo -e "${blue}  N  N N I  SSS   FFFF  EEEE  RRRR  EEEE  ${reset}"
  echo -e "${blue}  N  N N I     S  F     E     R  R  E     ${reset}"
  echo -e "${blue}  N   N  I  SSS   F     EEEEE R   R EEEEE${reset}"
}

abort_if_not_fedora() {
  if ! grep -q "fedora" /etc/os-release; then
    echo -e "${red}This script is designed to run on Fedora Linux. Exiting.${reset}"
    exit 1
  fi
}

check_command() {
  command -v "$1" &>/dev/null
}

initial_setup() {
  echo -e "${blue}Starting initial setup...${reset}"

  # Copy preconfigured files if they exist
  if [ -d "$HOME/fedora-setup/preconfigured-files" ]; then
    echo "Copying preconfigured files..."
    sudo cp -R "$HOME/fedora-setup/preconfigured-files/dnf.conf" /etc/dnf/ 2>/dev/null || echo -e "${yellow}Warning: dnf.conf not found, skipping${reset}"
    sudo cp -R "$HOME/fedora-setup/preconfigured-files/variables.sh" /etc/profile.d/ 2>/dev/null || echo -e "${yellow}Warning: variables.sh not found, skipping${reset}"
  fi

  # Add RPM Fusion repositories
  echo "Adding RPM Fusion repositories..."
  sudo dnf install -y \
    "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm" \
    "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"

  # Enable cisco openh264 repository
  sudo dnf config-manager --set-enabled fedora-cisco-openh264

  # Enable COPR repositories
  echo "Enabling COPR repositories..."
  sudo dnf copr enable -y solopasha/hyprland
  sudo dnf copr enable -y petersen/nix
  sudo dnf copr enable -y wehagy/protonplus
  sudo dnf copr enable -y sneexy/zen-browser
  sudo dnf copr enable -y lukenukem/asus-linux

  # Set timezone to Asia/Dhaka
  echo "Setting timezone to Asia/Dhaka..."
  sudo ln -sf /usr/share/zoneinfo/Asia/Dhaka /etc/localtime

  # Update system
  echo "Updating system..."
  sudo dnf update -y

  echo -e "${green}✔ Initial setup complete.${reset}"
}

install_packages() {
  echo -e "${blue}Installing required packages...${reset}"

  # Install packages from official repositories
  sudo dnf install -y fastfetch btop pipewire playerctl NetworkManager brightnessctl pkgconf wf-recorder thunar thunar-archive-plugin xarchiver zip unzip gvfs swww zsh kitty libnotify python3 gtk3-devel cairo-devel gtk-layer-shell-devel libgirepository1.0-dev gobject-introspection-devel python3-pip python3-gobject qt6ct-kde python3-psutil python3-cairo python3-dbus python3-loguru grim swappy hyprland zen-browser protonplus gnome-bluetooth slurp

  echo -e "${green}✔ Packages installed.${reset}"
}

copy_files() {
  echo -e "${blue}Copying configuration files...${reset}"

  # Using home-manager to source all dotfiles
  # mkdir -p "$HOME/.fonts" "$HOME/.themes" "$HOME/.icons" "$HOME/.config" "$HOME/.cache/nisfere" "$HOME/.vscode/extensions/"
  #
  # # Copy files if they exist
  # [ -d "$script_dir/fonts/" ] && cp -r "$script_dir/fonts/"* "$HOME/.fonts/"
  # [ -d "$script_dir/gtk-themes/" ] && cp -r "$script_dir/gtk-themes/"* "$HOME/.themes/"
  # [ -d "$script_dir/dotfiles/" ] && cp -r "$script_dir/dotfiles/"* "$HOME/.config/"
  #
  # Create notifications cache file
  echo '[]' >"$HOME/.cache/nisfere/notifications.json"

  # Create media directories
  mkdir -p "$HOME/Videos/records"
  mkdir -p "$HOME/Pictures/screenshots"

  # Create nisfere config directory and copy panel config
  mkdir -p "$HOME/.config/nisfere/themes"
  if [ -f "$script_dir/nisfere/panel/config.json" ]; then
    cp "$script_dir/nisfere/panel/config.json" "$HOME/.config/nisfere/panel-config.json"
  fi

  echo -e "${green}✔ Configuration files copied.${reset}"
}

setup_nisfere() {
  echo -e "${blue}Setting up Nisfere...${reset}"

  if [ -d "$script_dir/nisfere/" ]; then
    cp -r "$script_dir/nisfere/"* "$nisfere_installation_folder/"
  fi

  echo -e "${green}✔ Nisfere setup complete.${reset}"
}

setup_scripts() {
  echo -e "${blue}Setting up scripts...${reset}"

  # Make scripts executable if they exist
  if [ -f "$scripts_folder/change-theme.sh" ]; then
    chmod +x "$scripts_folder/change-theme.sh"
  fi
  if [ -f "$scripts_folder/init-swww.sh" ]; then
    chmod +x "$scripts_folder/init-swww.sh"
  fi
  if [ -f "$scripts_folder/init-panel.sh" ]; then
    chmod +x "$scripts_folder/init-panel.sh"
  fi

  # Execute scripts if they exist
  if [ -f "$scripts_folder/change-theme.sh" ]; then
    "$scripts_folder/change-theme.sh" dracula
  fi
  if [ -f "$scripts_folder/init-panel.sh" ]; then
    "$scripts_folder/init-panel.sh" >/dev/null 2>&1 &
  fi
  if [ -f "$scripts_folder/init-swww.sh" ]; then
    "$scripts_folder/init-swww.sh" >/dev/null 2>&1 &
  fi

  echo -e "${green}✔ Scripts executed.${reset}"
}

cleanup() {
  echo -e "${blue}Cleaning up...${reset}"

  # Clean dnf cache
  sudo dnf clean all

  # Update font cache
  fc-cache -fv

  echo -e "${green}✔ Cleanup complete.${reset}"
}

# Main Execution
main() {
  print_banner

  abort_if_not_fedora

  # Set up variables
  nisfere_installation_folder="$HOME/.nisfere"
  script_dir="$(dirname "$(realpath "$0")")"
  scripts_folder="$nisfere_installation_folder/scripts"

  # Create installation directory
  mkdir -p "$nisfere_installation_folder"

  # Execute installation steps
  echo -e "${blue}Starting Nisfere installation for Fedora...${reset}"

  initial_setup
  install_packages
  install_zsh
  install_vscode_extension
  copy_files
  setup_icons_and_cursor
  setup_nisfere
  setup_scripts
  cleanup

  echo -e "${green}✔ Installation complete!${reset}"
  echo -e "${yellow}Please reboot your system to ensure all changes take effect.${reset}"
  echo -e "${yellow}After reboot, you may need to log out and log back in to use Zsh as your default shell.${reset}"
}

# Run main function
main "$@"
