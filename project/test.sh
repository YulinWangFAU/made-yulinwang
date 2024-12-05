#!/bin/bash

# Exit on error
set -e

# Navigate directory
cd "$(dirname "$0")"

# Run the tests
echo "Running tests..."
python -m unittest test.py

echo "All tests passed successfully!"
