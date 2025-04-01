#!/bin/bash

killall nisfere-panel 2>/dev/null || true

# Define the panel path
PANEL_PATH="$HOME/.nisfere/panel"

# Navigate to the panel directory
cd "$PANEL_PATH" || { echo "Error: Directory $PANEL_PATH does not exist."; exit 1; }

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv

    # Activate the virtual environment
    source venv/bin/activate

    # Install requirements if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    else
        echo "Warning: No requirements.txt found."
    fi
else
    echo "Virtual environment found. Activating..."
    source venv/bin/activate
fi

# Run the Python script
python main.py > /dev/null 2>&1 & disown
