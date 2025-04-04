#!/bin/bash

USER_THEMES_DIR="$HOME/.config/nisfere/themes"
NISFERE_THEMES_DIR="$HOME/.nisfere/themes"
CURRENT_THEME_FILE="$HOME/.nisfere/current_theme.txt"
CURRENT_THEME=$(cat $CURRENT_THEME_FILE)

# Load themes directory correctly
if [[ -d "$USER_THEMES_DIR/$CURRENT_THEME" ]]; then
  THEME_PATH="$USER_THEMES_DIR/$CURRENT_THEME"
elif [[ -d "$NISFERE_THEMES_DIR/$CURRENT_THEME" ]]; then
  THEME_PATH="$NISFERE_THEMES_DIR/$CURRENT_THEME"
else
  echo "Error: Theme '$CURRENT_THEME' not found!"
  exit 1
fi

WALLPAPER_FILE="$THEME_PATH/wallpaper.png"
# Check swww daemon
swww query
if [ $? -eq 1 ]; then
    swww init
fi
swww img $WALLPAPER_FILE
