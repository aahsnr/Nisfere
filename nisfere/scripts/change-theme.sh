#!/bin/bash

# Check if a theme name was provided
if [[ -z "$1" ]]; then
  echo "Usage: $0 <theme_name>"
  exit 1
fi

NEW_THEME="$1"

USER_THEMES_DIR="$HOME/.config/nisfere/themes"
NISFERE_THEMES_DIR="$HOME/.nisfere/themes"
TEMPLATES_DIR="$HOME/.nisfere/templates"
CURRENT_THEME_FILE="$HOME/.nisfere/current_theme.txt"

# Load themes directory correctly
if [[ -d "$USER_THEMES_DIR/$NEW_THEME" ]]; then
  THEME_PATH="$USER_THEMES_DIR/$NEW_THEME"
elif [[ -d "$NISFERE_THEMES_DIR/$NEW_THEME" ]]; then
  THEME_PATH="$NISFERE_THEMES_DIR/$NEW_THEME"
else
  echo "Error: Theme '$NEW_THEME' not found!"
  exit 1
fi

COLORS_FILE="$THEME_PATH/colors.sh"
ICON_FILE="$THEME_PATH/icon.txt"
WALLPAPER_FILE="$THEME_PATH/wallpaper.png"

# Ensure required files exist
if [[ ! -f "$ICON_FILE" ]]; then
  echo "Error: icon.txt not found for theme '$NEW_THEME'!"
  exit 1
fi
ICON=$(cat "$ICON_FILE")

if [[ ! -f "$COLORS_FILE" ]]; then
  echo "Error: colors.sh not found for theme '$NEW_THEME'!"
  exit 1
fi
. "$COLORS_FILE"

if [[ ! -f "$WALLPAPER_FILE" ]]; then
  echo "Error: wallpaper.png not found for theme '$NEW_THEME'!"
  exit 1
fi

# Prepare sed commands
sed_cmd=(-e "s|{background}|$background|g"
  -e "s|{background_alt}|$background_alt|g"
  -e "s|{foreground}|$foreground|g"
  -e "s|{selected}|$selected|g"
  -e "s|{wallpaper}|$WALLPAPER_FILE|g")

for i in {0..15}; do
  eval color_var=\$color$i
  sed_cmd+=(-e "s|{color$i}|$color_var|g")
done

# Function to convert colors to Hyprland-compatible format (rgb(xxxxxx))
convert_to_rgb() {
  echo "rgb(${1#'#'})"
}

# Apply colors to different applications
declare -A config_files=(
  ["$HOME/.config/alacritty/colors.toml"]="$TEMPLATES_DIR/alacritty-colors.toml"
  ["$HOME/.config/swaylock/config"]="$TEMPLATES_DIR/swaylock-config"
  ["$HOME/.themes/nisfere-gtk-theme/general/dark.css"]="$TEMPLATES_DIR/gtk.css"
  ["$HOME/.nisfere/panel/styles/colors.css"]="$TEMPLATES_DIR/panel-colors.css"
  ["$HOME/.config/bpytop/themes/nisfere.theme"]="$TEMPLATES_DIR/bpytop.theme"
)

for file in "${!config_files[@]}"; do
  template="${config_files[$file]}"
  if [[ -f "$template" ]]; then
    sed "${sed_cmd[@]}" "$template" > "$file"
    echo "✅ Colors applied to $(basename "$file")"
  else
    echo "⚠️ Warning: Template '$template' not found!"
  fi
done

# Update Hyprland with special RGB format
HYPRLAND_CONFIG_FILE="$HOME/.config/hypr/conf/colors.conf"
HYPRLAND_TEMPLATE_FILE="$TEMPLATES_DIR/hyprland-colors.conf"

hyprland_sed_cmd=(-e "s|{background}|${background#'#'}|g"
  -e "s|{background_alt}|${background_alt#'#'}|g"
  -e "s|{foreground}|${foreground#'#'}|g"
  -e "s|{selected}|${selected#'#'}|g")

for i in {0..15}; do
  eval color_var=\$color$i
  hyprland_sed_cmd+=(-e "s|{color$i}|${color_var#'#'}|g")
done

if [[ -f "$HYPRLAND_TEMPLATE_FILE" ]]; then
  sed "${hyprland_sed_cmd[@]}" "$HYPRLAND_TEMPLATE_FILE" > "$HYPRLAND_CONFIG_FILE"
  echo "✅ Colors applied to Hyprland!"
else
  echo "⚠️ Warning: Hyprland template file not found!"
fi

# Apply GTK and icon theme
gsettings set org.gnome.desktop.interface gtk-theme "nisfere-gtk-theme"
gsettings set org.gnome.desktop.interface icon-theme "$ICON"
echo "✅ Icon theme applied!"

# Apply wallpaper
swww img "$WALLPAPER_FILE" --transition-type grow
echo "✅ Wallpaper applied!"

# Update current theme file
echo "$NEW_THEME" > "$CURRENT_THEME_FILE"

# Reload Hyprland
hyprctl reload
