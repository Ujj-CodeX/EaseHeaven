#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment based on the operating system
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Activating virtual environment (Windows)..."
    source venv/Scripts/activate
else
    echo "Activating virtual environment (Linux/Mac)..."
    source venv/bin/activate
fi

# Install dependencies from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "No requirements.txt file found. Skipping dependency installation."
fi

# Run the Flask application if app.py exists
if [ -f "main.py" ]; then
    echo "Running the application..."
    python main.py
else
    echo "No main.py file found. Please check your project."
fi
