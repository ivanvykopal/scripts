#!/bin/bash

# Check if Selenium is installed
if ! python -c "import selenium" 2>/dev/null; then
    echo "Selenium not installed. Installing..."
    pip install selenium

    if [ $? -ne 0 ]; then
        echo "Failed to install Selenium. Exiting..."
        exit 1
    fi

    echo "Selenium installed successfully."
fi

# Run the Python script
python run_cesnet.py
