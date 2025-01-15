#!/bin/sh

# Check if requirements.txt exists and is not empty
if [ -s ./agent/requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install --user --no-cache-dir -r ./agent/requirements.txt
else
    echo "No dependencies to install or requirements.txt is empty."
fi

# Execute the CMD passed to the container
exec "$@"
