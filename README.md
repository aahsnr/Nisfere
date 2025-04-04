# Nisfere Arch Installer

![Nisfere Logo](https://img.shields.io/badge/Nisfere-Arch%20Dotfiles-blueviolet)

Nisfere is a setup script and dotfiles collection tailored for Arch Linux users. It includes tools, themes, fonts, and Hyprland configuration to get a beautiful and functional desktop environment quickly.

---

## 🔧 Requirements
- Arch Linux
- Internet connection
- A non-root user

## 🚀 Features
- Automatic installation of required packages
- ZSH setup with plugins
- Fonts, GTK themes, icons, and cursors
- Hyprland default keybindings
- Panel and theming powered by [Fabric](https://github.com/Fabric-Development/fabric)

---

## 📦 What gets installed?

### Pacman Packages
Essential utilities and dependencies for the Nisfere setup:

```
fastfetch, bpytop, pipewire, playerctl, networkmanager, brightnessctl, 
pkgconf, wf-recorder, thunar, thunar-archive-plugin, xarchiver, zip, unzip, 
gvfs, swww, zsh, alacritty, libnotify, python, gtk3, cairo, gtk-layer-shell, 
libgirepository, gobject-introspection, gobject-introspection-runtime, 
python-pip, python-gobject, python-psutil, python-cairo, python-dbus, 
python-pydbus, python-loguru, python-setproctitle, grim, swappy
```

### AUR Packages
These will be installed via `yay`:

```
python-fabric, swaylock-effects-git, swayidle, gnome-bluetooth-3.0, 
fabric-cli-git, slurp, imagemagick
```

---

## 🎨 Themes, Fonts, Icons
- Fonts copied to `~/.fonts`
- GTK themes to `~/.themes`
- Icons to `~/.icons`
- Cursor set to `Breeze-Adapta-Cursor`

---

## 🧠 Panel Notes
Nisfere's panel is powered by [Fabric](https://github.com/Fabric-Development/fabric). Please ensure it's installed and accessible from your system PATH.

Panel config is stored in:
```
~/.config/nisfere/panel-config.json
```

---

## 🔧 Installation

```bash
# Clone this repository
git clone https://github.com/yourusername/nisfere-dotfiles.git
cd nisfere-dotfiles

# Make the install script executable
chmod +x install.sh

# Run the installer (do NOT use sudo)
./install.sh
```

---

## ❌ Uninstallation

There is no automated uninstall script yet, but you can manually remove installed content:

```bash
# Delete nisfere content
rm -rf ~/.nisfere
rm -rf ~/.config/nisfere
rm -rf ~/.fonts/*
rm -rf ~/.themes/*
rm -rf ~/.icons/*
rm -rf ~/.zshrc

# (Optional) Reset shell to bash
chsh -s /bin/bash
```

---


## ⌨️ Hyprland Default Keybindings

### General Actions

| Keybind               | Action                                            |
|----------------------|---------------------------------------------------|
| SUPER + Return       | Open terminal                                     |
| SUPER + Q            | Kill active window                                |
| SUPER + R            | Restart Nisfere panel                             |
| SUPER + M            | Exit Hyprland                                     |
| SUPER + E            | Open file manager                                 |
| SUPER + V            | Open Firefox                                      |
| SUPER + X            | Open power menu via panel                         |
| SUPER + T            | Open theme switcher via panel                     |
| SUPER + SPACE        | Open launcher/menu                                |
| SUPER + F            | Toggle fullscreen                                 |
| SUPER + S            | Toggle floating                                   |

### Focus & Resize

| Keybind                       | Action                                      |
|------------------------------|---------------------------------------------|
| SUPER + Arrow Keys           | Move focus                                   |
| SUPER + SHIFT + Arrows       | Resize active window                         |
| SUPER + P                    | Toggle pseudo-mode (dwindle)                 |
| SUPER + J                    | Toggle split (dwindle)                       |

### Workspaces

| Keybind                     | Action                                        |
|----------------------------|-----------------------------------------------|
| SUPER + [1-0]              | Switch to workspace 1–10                      |
| SUPER + SHIFT + [1-0]      | Move active window to workspace 1–10         |
| SUPER + Tab                | Next workspace                                |
| SUPER + SHIFT + Tab        | Previous workspace                            |

### Special Workspace

| Keybind                | Action                                          |
|------------------------|-------------------------------------------------|
| SUPER + S              | Toggle scratchpad                               |
| SUPER + SHIFT + S      | Move window to scratchpad                       |

### Mouse & Movement

| Keybind                | Action                                          |
|------------------------|-------------------------------------------------|
| SUPER + Mouse Down     | Next workspace                                  |
| SUPER + Mouse Up       | Previous workspace                              |
| SUPER + LMB            | Move window                                     |
| SUPER + RMB            | Resize window                                   |

### Multimedia Keys

| Keybind                         | Action                                    |
|--------------------------------|-------------------------------------------|
| XF86AudioRaiseVolume           | Increase volume                           |
| XF86AudioLowerVolume           | Decrease volume                           |
| XF86AudioMute                  | Toggle mute                               |
| XF86AudioMicMute               | Toggle microphone mute                    |
| XF86MonBrightnessUp            | Increase brightness                       |
| XF86MonBrightnessDown          | Decrease brightness                       |
| XF86Lock                       | Lock screen                               |

### Media Playback

| Keybind        | Action                    |
|----------------|---------------------------|
| XF86AudioNext  | Next track (playerctl)    |
| XF86AudioPause | Play/pause (playerctl)    |
| XF86AudioPrev  | Previous track (playerctl)|
| F3/F2/F4       | Volume control            |
| F8/F7/F6       | Media playback control    |

---

## 📁 Folder Structure

- `~/.nisfere`: Nisfere's internal files
- `~/.config/nisfere`: Configuration and themes
- `~/.cache/nisfere`: Panel notifications cache
- `~/Pictures/screenshots`: Screenshot save folder
- `~/Videos/records`: Screen recordings save folder

---

## 📜 License
MIT License

