#!/bin/bash

# Function to gracefully exit
cleanup() {
    echo "Exiting script..."
    # Kill background processes
    pkill -P $$
    exit 0
}

# Trap SIGINT signal (Ctrl+C) and call cleanup function
trap cleanup SIGINT

# Run the first command in the background
python3 readSensorValue.py &

# Run the second command in the background with sudo
sudo python3 cameraThread.py &

# Wait for any key press to exit
echo "Press any key to exit..."
read -n 1 -s

# Call cleanup function to terminate background processes
cleanup