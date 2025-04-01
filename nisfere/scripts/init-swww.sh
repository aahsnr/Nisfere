#!/bin/bash

THEMES_DIR="$HOME/.config/nisfere/themes/"
CURRENT_THEME_FILE="$HOME/.nisfere/current_theme.txt"
CURRENT_THEME=$(cat $CURRENT_THEME_FILE)
WALLPAPER_FILE="$THEMES_DIR/$CURRENT_THEME/wallpaper.png"
# Check swww daemon
swww query
if [ $? -eq 1 ]; then
    swww init
fi
swww img $WALLPAPER_FILE
