#!/bin/bash

set -e          # Exit immediately if a command exits with a non-zero status
set -u          # Treat unset variables as an error
set -o pipefail # Prevent errors in a pipeline from being masked

echo -e "\033[1;34m   N   N I   SSS  FFFFF EEEEE RRRR  EEEEE\033[0m"
echo -e "\033[1;34m  N  N N I  S     F     E     R   R E     \033[0m"
echo -e "\033[1;34m  N  N N I  SSS   FFFF  EEEE  RRRR  EEEE  \033[0m"
echo -e "\033[1;34m  N  N N I     S  F     E     R  R  E     \033[0m"
echo -e "\033[1;34m  N   N  I  SSS   F     EEEEE R   R EEEEE\033[0m"

# Ensure running on Arch Linux
if ! grep -q "arch" /etc/os-release; then
	echo "This script is designed to run on Arch Linux."
	exit 1
fi

# Prevent running as root
if [ "$(id -u)" -eq 0 ]; then
	echo "Please do not run this script as root."
	exit 1
fi

# install yay if needed
installYay() {
    _installPackages "base-devel"
    SCRIPT=$(realpath "$0")
    temp_path=$(dirname "$SCRIPT")
    git clone https://aur.archlinux.org/yay.git $download_folder/yay
    cd $download_folder/yay
    makepkg -si
    cd $temp_path
    echo ":: yay has been installed successfully."
}

# Check if command exists
checkCommandExists() {
    package="$1"
    if ! command -v $package >/dev/null; then
        return 1
    else
        return 0
    fi
}

install_packages() {
	echo "Installing the pre-requisites, may take a while...."

	# Install pacman packages 
	pacman_deps=(
		fastfetch
		bpytop
		pipewire
		playerctl
		networkmanager
		brightnessctl
		pkgconf
		wf-recorder
		thunar
		thunar-archive-plugin
		xarchiver
		zip
		unzip
		gvfs
		swww
		alacritty
		libnotify
		python
		gtk3
		cairo
		gtk-layer-shell
		libgirepository
		gobject-introspection
		gobject-introspection-runtime
		python-pip
		python-gobject
		python-psutil
		python-cairo
		python-dbus
        	python-pydbus
		python-loguru
		python-setproctitle
        	grim
        	swappy
	)

	aur_deps=(
		python-fabric
		swaylock-effects-git
		swayidle
		gnome-bluetooth-3.0
		fabric-cli-git
		slurp
		imagemagick
	)


	sudo pacman -S --noconfirm --needed "${pacman_deps[@]}"  || true

	# Install aur packages

	yay --noconfirm --needed "${aur_deps[@]}"  || true

}

# Synchronizing package databases
echo "Updating Arch..."
sudo pacman -Sy

# Install yay if needed
if checkCommandExists "yay"; then
    echo "yay is already installed"
else
    echo "The installer requires yay. yay will be installed now"
    installYay
fi

install_packages

# Get the directory where the script is located
script_dir="$(dirname "$(realpath "$0")")"

fonts_folder="$script_dir/fonts"
fonts_destination_folder="$HOME/.fonts"
mkdir -p "$fonts_destination_folder"
cp -r "$fonts_folder/"* "$fonts_destination_folder/"
echo "✅ Fonts copied"

gtk_themes_folder="$script_dir/gtk-themes"
gtk_themes_destination_folder="$HOME/.themes"
mkdir -p "$gtk_themes_destination_folder"
cp -r "$gtk_themes_folder/"* "$gtk_themes_destination_folder/"
echo "✅ Gtk themes copied"

icons_destination_folder="$HOME/.icons"
mkdir -p "$icons_destination_folder"

if [ ! -d "$icons_destination_folder/dracula-icons" ]; then
    git clone https://github.com/m4thewz/dracula-icons "$icons_destination_folder/dracula-icons"
fi

if [ ! -d "$icons_destination_folder/Grade-circle-dark" ]; then
    temp_dir=$(mktemp -d)
	git clone https://github.com/mayur-m-zambare/Grade-icon-theme.git "$temp_dir"
	cp -r "$temp_dir/Grade-circle-dark" "$icons_destination_folder/"
	rm -rf "$temp_dir"
fi

echo "✅ Gtk icons imported"

if [ ! -d "$icons_destination_folder/Breeze-Adapta-Cursor" ]; then
   git clone https://github.com/mustafaozhan/Breeze-Adapta-Cursor ~/.icons/Breeze-Adapta-Cursor/

fi

echo "✅ Gtk cursor imported"

hyprctl setcursor "Breeze-Adapta-Cursor" 17
gsettings set org.gnome.desktop.interface cursor-theme "Breeze-Adapta-Cursor"
gsettings set org.gnome.desktop.interface cursor-size 17

echo "✅ Cursor theme updated to Breeze-Adapta-Cursor"

config_folder="$script_dir/dotfiles"
config_destination_folder="$HOME/.config"
mkdir -p "$config_destination_folder"
cp -r "$config_folder/"* "$config_destination_folder/"
echo "✅ Config folders copied"

mkdir -p "$config_destination_folder/nisfere"
mkdir -p "$config_destination_folder/nisfere/themes"
cp "$script_dir/nisfere/panel/config.json" "$config_destination_folder/nisfere/panel-config.json" 

nisfere_installation_folder="$HOME/.nisfere"
nisfere_folder="$script_dir/nisfere"
mkdir -p "$nisfere_installation_folder"
cp -r "$nisfere_folder/"* "$nisfere_installation_folder/"
echo "✅ Nisfere project copied"

echo "Initializing nisfere-panel..."

cache_folder="$HOME/.cache"
mkdir -p "$cache_folder"
nisfere_cache_folder="$cache_folder/nisfere"
mkdir -p "$nisfere_cache_folder"
notifications_file="$nisfere_cache_folder/notifications.json"
echo '[]' > "$notifications_file"
echo "✅ Created cache notifications file"

pictures_folder="$HOME/Pictures"
mkdir -p "$pictures_folder"
screenshots_folder="$pictures_folder/screenshots"
mkdir -p "$screenshots_folder"
echo "✅ Created screenshots folder inside Pictures"

videos_folder="$HOME/Videos"
mkdir -p "$videos_folder"
records_folder="$videos_folder/records"
mkdir -p "$records_folder"
echo "✅ Created records folder inside Videos"

echo "Initializing nisfere theme and panel..."

scripts_folder="$nisfere_installation_folder/scripts"

# Ensure the scripts directory exists
if [ ! -d "$scripts_folder" ]; then
    echo "Error: Scripts folder not found at $scripts_folder"
    exit 1
fi

# Navigate to the scripts folder
cd "$scripts_folder" || { echo "Failed to enter directory $scripts_folder"; exit 1; }

chmod +x change-theme.sh init-swww.sh init-panel.sh

"$scripts_folder/change-theme.sh" dracula

echo "Applied dracula theme"

"$scripts_folder/init-panel.sh" > /dev/null 2>&1
echo "Panel running"

"$scripts_folder/init-swww.sh" > /dev/null 2>&1
echo "Wallpaper changed"

echo "Installation finished!!!!!"


