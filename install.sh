#!/bin/bash

set -euo pipefail # Enable strict error handling

# Colors for output
green="\033[1;32m"
blue="\033[1;34m"
reset="\033[0m"

print_banner() {
    echo -e "${blue}   N   N I   SSS  FFFFF EEEEE RRRR  EEEEE${reset}"
    echo -e "${blue}  N  N N I  S     F     E     R   R E     ${reset}"
    echo -e "${blue}  N  N N I  SSS   FFFF  EEEE  RRRR  EEEE  ${reset}"
    echo -e "${blue}  N  N N I     S  F     E     R  R  E     ${reset}"
    echo -e "${blue}  N   N  I  SSS   F     EEEEE R   R EEEEE${reset}"
}

abort_if_not_arch() {
    if ! grep -q "arch" /etc/os-release; then
        echo "This script is designed to run on Arch Linux. Exiting."
        exit 1
    fi
}

abort_if_root() {
    if [ "$(id -u)" -eq 0 ]; then
        echo "Please do not run this script as root. Exiting."
        exit 1
    fi
}

check_command() {
    command -v "$1" &>/dev/null
}

install_yay() {
    echo "Installing yay..."
    git clone https://aur.archlinux.org/yay.git "$nisfere_installation_folder/yay"
    cd "$nisfere_installation_folder/yay"
    makepkg -si --noconfirm
    cd - &>/dev/null
    echo -e "${green}✔ Yay installed successfully.${reset}"
}

install_packages() {
    echo "Installing required packages..."
    sudo pacman -Syu --noconfirm --needed \
        fastfetch bpytop pipewire playerctl networkmanager brightnessctl pkgconf \
        wf-recorder thunar thunar-archive-plugin xarchiver zip unzip gvfs swww zsh \
        alacritty libnotify python gtk3 cairo gtk-layer-shell libgirepository \
        gobject-introspection gobject-introspection-runtime python-pip python-gobject \
        python-psutil python-cairo python-dbus python-pydbus python-loguru \
        python-setproctitle grim swappy

    yay -S --noconfirm --needed \
        python-fabric swaylock-effects-git swayidle gnome-bluetooth-3.0 fabric-cli-git slurp imagemagick
    
    echo -e "${green}✔ Packages installed.${reset}"
}

install_zsh() {
    echo "Configuring Zsh..."
    cp "$script_dir/zsh/.zshrc" "$HOME/.zshrc"
    zsh_folder="$nisfere_installation_folder/zsh"
    plugins_folder="$zsh_folder/plugins"
    mkdir -p "$plugins_folder"
    
    for plugin in zsh-syntax-highlighting zsh-autosuggestions zsh-history-substring-search; do
        if [ ! -d "$plugins_folder/$plugin" ]; then
            git clone "https://github.com/zsh-users/$plugin.git" "$plugins_folder/$plugin"
        fi
    done
    # Ensure Zsh history file exists
	history_file=$HOME/.zsh_history
	if [ ! -f "$history_file" ]; then
		touch "$history_file"
		chmod 600 "$history_file"
	fi

    chsh -s /bin/zsh
    echo -e "${green}✔ Zsh configured.${reset}"
}

copy_files() {
    echo "Copying configuration files..."
    
    mkdir -p "$HOME/.fonts" "$HOME/.themes" "$HOME/.icons" "$HOME/.config" "$HOME/.cache/nisfere"
    cp -r "$script_dir/fonts/"* "$HOME/.fonts/"
    cp -r "$script_dir/gtk-themes/"* "$HOME/.themes/"
    cp -r "$script_dir/dotfiles/"* "$HOME/.config/"
    echo '[]' > "$HOME/.cache/nisfere/notifications.json"
    
    echo -e "${green}✔ Configuration files copied.${reset}"
}

setup_icons_and_cursor() {
    echo "Setting up icons and cursor..."
    icons_dest="$HOME/.icons"
    if [ ! -d "$icons_dest/dracula-icons" ]; then
        git clone https://github.com/m4thewz/dracula-icons "$icons_dest/dracula-icons"
    fi
    
    if [ ! -d "$icons_dest/Grade-circle-dark" ]; then
        temp_dir=$(mktemp -d)
        git clone https://github.com/mayur-m-zambare/Grade-icon-theme.git "$temp_dir"
        cp -r "$temp_dir/Grade-circle-dark" "$icons_dest/"
        rm -rf "$temp_dir"
    fi
    
    if [ ! -d "$icons_dest/Breeze-Adapta-Cursor" ]; then
        git clone https://github.com/mustafaozhan/Breeze-Adapta-Cursor "$icons_dest/Breeze-Adapta-Cursor"
    fi
    
    hyprctl setcursor "Breeze-Adapta-Cursor" 17
    gsettings set org.gnome.desktop.interface cursor-theme "Breeze-Adapta-Cursor"
    gsettings set org.gnome.desktop.interface cursor-size 17
    echo -e "${green}✔ Icons and cursor setup complete.${reset}"
}

setup_nisfere() {
    echo "Setting up Nisfere..."
    cp -r "$script_dir/nisfere/"* "$nisfere_installation_folder/"
    echo -e "${green}✔ Nisfere setup complete.${reset}"
}

setup_scripts() {
    echo "Setting up scripts..."
    chmod +x "$scripts_folder/change-theme.sh" "$scripts_folder/init-swww.sh" "$scripts_folder/init-panel.sh"
    "$scripts_folder/change-theme.sh" dracula
    "$scripts_folder/init-panel.sh" > /dev/null 2>&1
    "$scripts_folder/init-swww.sh" > /dev/null 2>&1
    echo -e "${green}✔ Scripts executed.${reset}"
}

# Main Execution
print_banner
abort_if_not_arch
abort_if_root
nisfere_installation_folder="$HOME/.nisfere"
script_dir="$(dirname "$(realpath "$0")")"
scripts_folder="$nisfere_installation_folder/scripts"
mkdir -p "$nisfere_installation_folder"

sudo pacman -Sy

if check_command "yay"; then
    echo "Yay is already installed."
else
    install_yay
fi

install_packages
install_zsh
copy_files
setup_icons_and_cursor
setup_nisfere
setup_scripts

echo -e "${green}✔ Installation complete!${reset}"
