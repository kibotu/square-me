#!/bin/bash
set -e

echo "Installing dependencies..."

uv pip install --system --break-system-packages Pillow opencv-python-headless

echo "Installation complete."
